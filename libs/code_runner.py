"""
This is code runner plugin developed by HeavenHM.
This plugin is used to run code on the server using the JDoodle API.
You get 200 free credits per month so API is already configured from HeavenHM.

Features:
- Run and Execute Code.
- Show Code Snippet.
- Create Quick Chart.
- Upload and Download Files. (Database is MongoDB Atlas)
- Get Help Information.

Privacy Policy: 
The Plugin uses the JDoodle Compiler API (https://www.jdoodle.com/compiler-api) to compile and run your code. 
The JDoodle Compiler API is a third-party service that provides online code execution for various programming languages. 
The JDoodle Compiler API may collect and use your code and other information in accordance with their own terms and conditions (https://www.jdoodle.com/terms) and privacy policy (https://www.jdoodle.com/privacy).
https://code-runner-plugin.vercel.app/privacy
Date : 01-01-2024
"""

import requests
import json
from libs.logger import logger

lang_codes = {
  'c': 'c',
  'c++': 'cpp17',
  'cpp': 'cpp17',
  'python': 'python3',
  'go lang': 'go',
  'scala': 'scala',
  'bash shell': 'bash',
  'c#': 'csharp',
  'vb.net': 'vbn',
  'objectivec': 'objc',
  'swift': 'swift',
  'r language': 'r',
  'free basic': 'freebasic',
  'nodejs': 'nodejs',
  'java': 'java',
  'javascript': 'nodejs',
}

class CodeRunner:
    # Code Runner Server URL.
    server_url = 'https://code-runner-plugin.vercel.app'

    def __init__(self):
        self.logger = logger
    
    def get_lang_code(self, lang):
        self.logger.info(f"Getting language code for {lang}")
        if lang in lang_codes:
            return lang_codes[lang]
        else:
            self.logger.error(f"Language {lang} not found")
            return None

    def run_code(self, code, language,code_input=None,compile_only=False):
        try:
            if not code or not language:
                self.logger.error("Code or language is not provided.")
                return None

            language = language.lower()
            language = self.get_lang_code(language)

            if language is None:
                self.logger.error(f"Language '{language}' not found in JDoodle API")
                return None

            self.logger.info(f"Running code {code[:20]}... in {language}")

            # Replace escape sequences with empty characters
            code = code.replace("\\n", "").replace("\\t", "").replace("\\r", "").replace("\"", "\"")
            data = {"code": code, "language": language,"input" : code_input,"compileOnly" : compile_only}

            self.logger.info(f"Sending request to {self.server_url}/run_code and data is '{data}'")
            response = requests.post(f"{self.server_url}/run_code", json=data)

            if response.status_code != 200:
                self.logger.error(f"Request to {self.server_url}/run_code failed with status code {response.status_code}")
                return None

            response.raise_for_status()
            output = response.json()
            code_output = None

            if output:
                code_output = output.get("output", None)

            if not code_output:
                self.logger.error("No output from the code execution.")
                return None

            return code_output
        except requests.exceptions.RequestException as request_exception:
            self.logger.error(f"Error running code: {request_exception}")
            raise
        except Exception as general_exception:
            self.logger.error(f"An unexpected error occurred: {general_exception}")
            raise

    def save_code(self, filename, code):
        try:
            data = {"filename": filename, "code": code}
            response = requests.post(f"{self.server_url}/save_code", json=data)
            response.raise_for_status()
            return response.json()["download_link"]
        except requests.exceptions.RequestException as exception:
            self.logger.error(f"Error saving code: {exception}")
            raise

    def download_file(self, filename):
        try:
            response = requests.get(f"{self.server_url}/download/{filename}")
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as exception:
            self.logger.error(f"Error downloading file: {exception}")
            raise

    def help(self):
        try:
            response = requests.get(f"{self.server_url}/help")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            self.logger.error(f"Error getting help information: {exception}")
            raise

    def credit_limit(self):
        try:
            response = requests.get(f"{self.server_url}/credit_limit")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            self.logger.error(f"Error getting credit limit: {exception}")
            raise

    def upload_file(self, filename, data):
        try:
            data = {"filename": filename, "data": data}
            response = requests.post(f"{self.server_url}/upload", json=data)
            response.raise_for_status()
            return response.json()["download_link"]
        except requests.exceptions.RequestException as exception:
            self.logger.error(f"Error uploading file: {exception}")
            raise

    def quick_chart(self, chart_type, labels, datasets):
        try:
            data = {"chart_type": chart_type, "labels": labels, "datasets": datasets}
            response = requests.post(f"{self.server_url}/quick_chart", json=data)
            response.raise_for_status()
            return response.json()["chart_link"]
        except requests.exceptions.RequestException as exception:
            self.logger.error(f"Error creating quick chart: {exception}")
            raise

    def show_snippet(self, code, title, theme, language, opacity, blurLines, showNums):
        try:
            data = {
                "code": code,
                "title": title,
                "theme": theme,
                "language": language,
                "opacity": opacity,
                "blurLines": blurLines,
                "showNums": showNums,
            }
            response = requests.post(f"{self.server_url}/show_snippet", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exception:
            self.logger.error(f"Error showing code snippet: {exception}")
            raise
