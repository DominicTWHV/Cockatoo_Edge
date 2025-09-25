import aiofiles

import json
import ast
import os

class FileHandler:
    @staticmethod
    async def read(file_path: str) -> str:
        if not os.path.exists(file_path):
            return None
        
        async with aiofiles.open(file_path, 'r') as file:
            content = await file.read()
        return content
    
    @staticmethod
    async def fetch_latest_git_commit() -> str:
        git_file_path = ".git/refs/heads/main"
        commit_id = await FileHandler.read(git_file_path)
        return commit_id.strip()[:7] if commit_id else "N/A"
    
class JSONHandler:
    @staticmethod
    async def read_json(file_path: str) -> dict:
        content = await FileHandler.read(file_path)
        return json.loads(content)

    @staticmethod
    async def str_to_json(data: str) -> dict:
        if isinstance(data, dict):
            return data
        
        #if not str, return None
        if not isinstance(data, str):
            return None

        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            pass
        
        try:
            parsed_data = ast.literal_eval(data)
            if isinstance(parsed_data, dict):
                return parsed_data
        except (ValueError, SyntaxError):
            pass

        return data #probably just a string, return as is