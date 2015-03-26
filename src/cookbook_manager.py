from utils import json_config

import os
import shutil

class CookbookManager(object):
    
    def __init__(self): 
        # Read Config
        self.config = json_config.parse_json("config.json")
        self.folder = self.config["Cookbook Folder"]

    def __folder_path(self, cookbook_name):
        return os.path.join(self.folder, cookbook_name)

    def __file_path(self, cookbook_name):
        return os.path.join(self.folder, cookbook_name, cookbook_name + ".md")

    def __create_cookbook_folder(self, cookbook_name):
        path = self.__folder_path(cookbook_name)

        # Check the folder is existing
        if not os.path.exists(path):
            os.makedirs(path)

    def update(self, cookbook_name, content):
        self.__create_cookbook_folder(cookbook_name) 

        file_path = self.__file_path(cookbook_name)
        
        # Content
        with open(file_path, "w") as f:
            f.write(content)

        # @ToDo SVG file
        
    def read(self, cookbook_name):
        file_path = self.__file_path(cookbook_name)

        with open(file_path, "r") as f:
            content = f.read()

        return content

    def delete(self, cookbook_name):
        folder_path = self.__folder_path(cookbook_name)
        return shutil.rmtree(folder_path)

