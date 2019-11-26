import os
import json

from os import path
from config import Config

class Util:
    
    @staticmethod
    def rel2abs(rel: str) -> str:
        dirname = path.dirname(__file__)
        file_path = dirname + '/' + rel
        return file_path
    
    @staticmethod
    def load_json():
        """Loads exploit.json if it exists
        
        Returns:
            dict: exploit documents
        """
        file_path = Util.rel2abs(Config.PATH_EXPLOITS)
        print(file_path)
        if path.exists(file_path):
            with open(file_path) as json_file:
                return json.load(json_file)
        else:
            return dict()
        
    @staticmethod
    def save_json(rel, json_data):
        file_path = Util.rel2abs(rel)
     
        with open(file_path, 'w') as output_file:
            json.dump(json_data, output_file)
        