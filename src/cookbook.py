import StringIO

import sys
import mistune

class Cookbook(object):

    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.md = mistune.Markdown()

    def gcode(self):
        tokens = self.md.block(self.content) 

        block_start = 0
        block_end = 0
        
        tree = Heading.heading_tree(tokens)
        steps = map(lambda item: Step(item), tree)


    # Save the cookbook script to file and generate a gcode file
    # This function is used by Octoprint file manager
    def save(self, path):
        with open(path, "w") as file:
            file.write(self.content)

class Heading(object):

    @staticmethod
    def heading_tree(tokens):
        return map(lambda block: Heading(block, 1), split_heading(tokens, 1))

    def __init__(self, tokens, level=1):
        self.title = ""
        self.content = None 
        self.sub_headings = []
        self.level = level

        # Find self heading content 
        end = 0
        for index, token in enumerate(tokens):
            if token["type"] == "heading" and token["level"] > self.level:
                end = index
                break

        self.title = tokens[0]["text"]
        if end:
            self.content = tokens[1:end]
            self.sub_headings = map(lambda block: Heading(block, self.level + 1), split_heading(tokens[end:], self.level + 1))
        else:
            self.content = tokens[1:]

class Step(object):
    def __init__(self, heading):
        self.__heading = heading
        self.name = heading.title
        
        self.processes = map(lambda item: Process(item), self.__heading.sub_headings)

class Process(object):
    def __init__(self, heading):
        self.__heading = heading
        self.name = heading.title

        self.params = {}
        for block in heading.content:
            if block["type"] == "code": 
                self.params.update(self.__parse_code(block))

    def __parse_code(self, code_block):
        self.lang = code_block["lang"]

        params = {}
        for line in code_block["text"].split("\n"):
            key, value = line.split(":")            
            params[key.strip()] = value.strip()

        return params
                
def split_block(compare_func, items):
    block_start = 0
    blocks = []

    for index, item in enumerate(items):
        if compare_func(item):
            if block_start != index:
                blocks.append(items[block_start:index])

            block_start = index

    blocks.append(items[block_start:])

    return blocks

def split_heading(tokens, level):
    return split_block(lambda token: token["type"] == "heading" and token["level"] == level, tokens)

if __name__ == "__main__":
    with open("test.md", "r") as data:
        content = data.read()

    cookbook = Cookbook("test", content)
    cookbook.gcode()
