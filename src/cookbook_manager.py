from utils import json_config

import os
import shutil

from cookbook import Cookbook


class CookbookManager(object):

    def __init__(self):
        # Read Config
        self.config = json_config.parse_json('config.json')
        self.folder = self.config['Cookbook Folder']

    def __folder_path(self, cookbook_name):
        return os.path.join(self.folder, cookbook_name)

    def __create_cookbook_folder(self, cookbook_name):
        path = self.__folder_path(cookbook_name)

        # Check the folder is existing
        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def list(self):
        names = os.listdir(self.folder)

        return map(lambda name: Cookbook(name, self.__folder_path(name)), names)

    def update(self, cookbook_name, content=None):
        self.__create_cookbook_folder(cookbook_name)

        cookbook = self.get(cookbook_name)

        if content:
            cookbook.content = content

    def rename(self, old_name, new_name):
        old_path = self.__folder_path(old_name)
        new_path = self.__folder_path(new_name)

        return os.rename(old_path, new_path)

    def get(self, cookbook_name):
        folder_path = self.__folder_path(cookbook_name)

        return Cookbook(cookbook_name, folder_path)

    def delete(self, cookbook_name):
        folder_path = self.__folder_path(cookbook_name)
        return shutil.rmtree(folder_path)
