import StringIO

import sys
import mistune

from process import circle
from process import operations
from process import spiral
from process import fixed_point
from process import heat

class Cookbook(object):

    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.md = mistune.Markdown()

    def steps(self):
        tokens = self.md.block(self.content)

        block_start = 0
        block_end = 0

        tree = Heading.heading_tree(tokens)
        steps = map(lambda item: Step(item), tree)

        return steps

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

        self.blocks = []
        for block in heading.content:
            if block["type"] == "code":
                self.blocks.append(self.__parse_code(block))

    def __parse_code(self, code_block):
        params = []

        for line in code_block["text"].split("\n"):
            if ":" in line:
                key, value = line.split(":")
                params.append((key.strip(), value.strip()))
            else:
                params.append((line.strip(), None))

        return CodeBlock(code_block["lang"], params)

class CodeBlock(object):
    lang_map = {
        "circle": circle.Circle,
        "spiral": spiral.Spiral,
        "fixed_point": fixed_point.FixedPoint,
        "operations": operations.Operations,
        "heat": heat.Heat
    }

    def __init__(self, lang, params):
        self.lang = lang
        self.params = params

    def gcode(self):
        return self.lang_map[self.lang](self.params)

    def __str__(self):
        return "{} => {}".format(self.lang, self.params)

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
