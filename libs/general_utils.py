# general_utils.py
import base64
import os
import tempfile
from libs.logger import logger
import subprocess
import traceback
import streamlit as st
from libs.lang_codes import LangCodes

# Import the service_account module
from google.oauth2 import service_account
from google.auth import exceptions
from google.auth.transport import requests

class GeneralUtils:
    
    def execute_code(self,compiler_mode: str):
        logger.info(f"Executing code: {st.session_state.generated_code[:100]} in language: {st.session_state.code_language} with Compiler Mode: {compiler_mode}")

        try:
            if len(st.session_state.generated_code) == 0 or st.session_state.generated_code == "":
                st.toast("Generated code is empty. Cannot execute an empty code.", icon="❌")
                return
            
            if compiler_mode.lower() == "online":
                html_content = self.generate_dynamic_html(st.session_state.code_language, st.session_state.generated_code)
                logger.info(f"HTML Template: {html_content[:100]}")
                return html_content

            else:
                output = self.run_code(st.session_state.generated_code,st.session_state.code_language)
                logger.info(f"Output execution: {output}")

                if "error" in output.lower() or "exception" in output.lower() or "SyntaxError" in output.lower() or "NameError" in output.lower():

                    logger.error(f"Error in code execution: {output}")
                    response = st.session_state.sequential_chain({'code_topic': st.session_state.generated_code})
                    fixed_code = response['code_fix']
                    st.code(fixed_code, language=st.session_state.code_language.lower())

                    with st.expander('Message History'):
                        st.info(st.session_state.memory.buffer)
                    logger.warning(f"Trying to run fixed code: {fixed_code}")
                    output = GeneralUtils.run_code(fixed_code, st.session_state.code_language)
                    logger.warning(f"Fixed code output: {output}")

                st.toast("Execution Output:\n" + output, icon="🔥")
                logger.info(f"Execution Output: {output}")

        except Exception as e:
            st.toast("Error in code execution:",icon="❌")
            # Output the stack trace
            st.toast(traceback.format_exc(), icon="❌")
            logger.error(f"Error in code execution: {traceback.format_exc()}")
    
    # Generate Dynamic HTML for JDoodle Compiler iFrame Embedding.
    def generate_dynamic_html(self,language, code_prompt):
        logger.info("Generating dynamic HTML for language: %s", language)
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Online JDoodle Compiler</title>
        </head>
        <body>
            <div data-pym-src='https://www.jdoodle.com/plugin' data-language="{language}"
                data-version-index="0" data-libs="" >{script_code}
            </div>
            <script src="https://www.jdoodle.com/assets/jdoodle-pym.min.js" type="text/javascript"></script>
        </body>
        </html>
        """.format(language=LangCodes()[language], script_code=code_prompt)
        return html_template
    
    # Method to check if compilers are installed on the system or not
    def check_compilers(self):
        # check for python,nodejs,c,c++,c#,go,ruby,java,kotlin,scala,swift compilers
        python_compiler = subprocess.run(["python", "--version"], capture_output=True, text=True)
        if python_compiler.returncode != 0:
            logger.error("Python compiler not found.")
            st.toast("Python compiler not found.", icon="❌")
            return False
        
        # check for nodejs compiler
        nodejs_compiler = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if nodejs_compiler.returncode != 0:
            logger.error("NodeJS compiler not found.")
            st.toast("NodeJS compiler not found.", icon="❌")
            return False
        
        # check for c compiler
        c_compiler = subprocess.run(["gcc", "--version"], capture_output=True, text=True)
        if c_compiler.returncode != 0:
            logger.error("C compiler not found.")
            st.toast("C compiler not found.", icon="❌")
            return False
        
        # check for c++ compiler
        cpp_compiler = subprocess.run(["g++", "--version"], capture_output=True, text=True)
        if cpp_compiler.returncode != 0:
            logger.error("C++ compiler not found.")
            st.toast("C++ compiler not found.", icon="❌")
            return False
        
        # check for c# compiler
        csharp_compiler = subprocess.run(["csc", "--version"], capture_output=True, text=True)
        if csharp_compiler.returncode != 0:
            logger.error("C# compiler not found.")
            st.toast("C# compiler not found.", icon="❌")
            return False
        
        # check for go compiler
        go_compiler = subprocess.run(["go", "version"], capture_output=True, text=True)
        if go_compiler.returncode != 0:
            logger.error("Go compiler not found.")
            st.toast("Go compiler not found.", icon="❌")
            return False
        
        # check for ruby compiler
        ruby_compiler = subprocess.run(["ruby", "--version"], capture_output=True, text=True)
        if ruby_compiler.returncode != 0:
            logger.error("Ruby compiler not found.")
            st.toast("Ruby compiler not found.", icon="❌")
            return False
        
        # check for java compiler
        java_compiler = subprocess.run(["java", "--version"], capture_output=True, text=True)
        if java_compiler.returncode != 0:
            logger.error("Java compiler not found.")
            st.toast("Java compiler not found.", icon="❌")
            return False
        
        # check for kotlin compiler
        kotlin_compiler = subprocess.run(["kotlinc", "--version"], capture_output=True, text=True)
        if kotlin_compiler.returncode != 0:
            logger.error("Kotlin compiler not found.")
            st.toast("Kotlin compiler not found.", icon="❌")
            return False
        
        # check for scala compiler
        scala_compiler = subprocess.run(["scala", "--version"], capture_output=True, text=True)
        if scala_compiler.returncode != 0:
            logger.error("Scala compiler not found.")
            st.toast("Scala compiler not found.", icon="❌")
            return False
        
        # check for swift compiler
        swift_compiler = subprocess.run(["swift", "--version"], capture_output=True, text=True)
        if swift_compiler.returncode != 0:
            logger.error("Swift compiler not found.")
            st.toast("Swift compiler not found.", icon="❌")
            return False
        
        return True
    
    def run_code(self,code, language):
        logger.info(f"Running code: {code[:100]} in language: {language}")

        # Check for code and language validity
        if not code or len(code.strip()) == 0:
            return "Code is empty. Cannot execute an empty code."
        
        # Check for compilers on the system
        compilers_status = self.check_compilers()
        if not compilers_status:
            return "Compilers not found. Please install compilers on your system."
        
        if language == "Python":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=True) as file:
                file.write(code)
                file.flush()

                logger.info(f"Input file: {file.name}")
                output = subprocess.run(
                    ["python", file.name], capture_output=True, text=True)
                logger.info(f"Runner Output execution: {output.stdout + output.stderr}")
                return output.stdout + output.stderr

        elif language == "C" or language == "C++":
            ext = ".c" if language == "C" else ".cpp"
            with tempfile.NamedTemporaryFile(mode="w", suffix=ext, delete=True) as src_file:
                src_file.write(code)
                src_file.flush()

                logger.info(f"Input file: {src_file.name}")

                with tempfile.NamedTemporaryFile(mode="w", suffix="", delete=True) as exec_file:
                    compile_output = subprocess.run(
                        ["gcc" if language == "C" else "g++", "-o", exec_file.name, src_file.name], capture_output=True, text=True)

                    if compile_output.returncode != 0:
                        return compile_output.stderr

                    logger.info(f"Output file: {exec_file.name}")
                    run_output = subprocess.run(
                        [exec_file.name], capture_output=True, text=True)
                    logger.info(f"Runner Output execution: {run_output.stdout + run_output.stderr}")
                    return run_output.stdout + run_output.stderr

        elif language == "JavaScript":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=True) as file:
                file.write(code)
                file.flush()

                logger.info(f"Input file: {file.name}")
                output = subprocess.run(
                    ["node", file.name], capture_output=True, text=True)
                logger.info(f"Runner Output execution: {output.stdout + output.stderr}")
                return output.stdout + output.stderr
            
        elif language == "Java":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".java", delete=True) as file:
                    file.write(code)
                    file.flush()
                    classname = "Main"  # Assuming the class name is Main, adjust if needed
                    compile_output = subprocess.run(["javac", file.name], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return compile_output.stderr
                    run_output = subprocess.run(["java", "-cp", tempfile.gettempdir(), classname], capture_output=True, text=True)
                    return run_output.stdout + run_output.stderr

        elif language == "Swift":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".swift", delete=True) as file:
                    file.write(code)
                    file.flush()
                    output = subprocess.run(["swift", file.name], capture_output=True, text=True)
                    return output.stdout + output.stderr

        elif language == "C#":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".cs", delete=True) as file:
                    file.write(code)
                    file.flush()
                    compile_output = subprocess.run(["csc", file.name], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return compile_output.stderr
                    exe_name = file.name.replace(".cs", ".exe")
                    run_output = subprocess.run([exe_name], capture_output=True, text=True)
                    return run_output.stdout + run_output.stderr

        elif language == "Scala":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".scala", delete=True) as file:
                    file.write(code)
                    file.flush()
                    output = subprocess.run(["scala", file.name], capture_output=True, text=True)
                    return output.stdout + output.stderr

        elif language == "Ruby":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".rb", delete=True) as file:
                    file.write(code)
                    file.flush()
                    output = subprocess.run(["ruby", file.name], capture_output=True, text=True)
                    return output.stdout + output.stderr

        elif language == "Kotlin":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".kt", delete=True) as file:
                    file.write(code)
                    file.flush()
                    compile_output = subprocess.run(["kotlinc", file.name, "-include-runtime", "-d", "output.jar"], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return compile_output.stderr
                    run_output = subprocess.run(["java", "-jar", "output.jar"], capture_output=True, text=True)
                    return run_output.stdout + run_output.stderr

        elif language == "Go":
                with tempfile.NamedTemporaryFile(mode="w", suffix=".go", delete=True) as file:
                    file.write(code)
                    file.flush()
                    compile_output = subprocess.run(["go", "build", "-o", "output.exe", file.name], capture_output=True, text=True)
                    if compile_output.returncode != 0:
                        return compile_output.stderr
                    run_output = subprocess.run(["./output.exe"], capture_output=True, text=True)
                    return run_output.stdout + run_output.stderr
        else:
            return "Unsupported language."

    def save_code(self, file_name):
        try:
            # Check for empty file name
            if not file_name or len(file_name) == 0:
                st.toast("Please enter a valid file name.", icon="❌")
                logger.error("Error in code saving: Please enter a valid file name.")
                return
            
            file_extension = file_name.split(".")[-1]
            logger.info(f"Saving code to file: {file_name} with extension: {file_extension}")
            
            # Create directory if it doesn't exist
            if not os.path.exists(file_extension):
                os.makedirs(file_extension)
                logger.info(f"Directory {file_extension} created successfully")
            
            # Check for empty code
            if not st.session_state.generated_code or len(st.session_state.generated_code.strip()) == 0:
                st.toast("Generated code is empty. Cannot save an empty file.", icon="❌")
                logger.error("Error in code saving: Generated code is empty.")
                return
            
            with open(f"{file_extension}/{file_name}", "w") as file:
                file.write(st.session_state.generated_code)
            
            st.toast(f"Code saved to file {file_name}", icon="✅")
            logger.info(f"Code saved to file {file_name}")
            
        except Exception as e:
            st.toast(traceback.format_exc())
            logger.error(f"Error in code saving: {traceback.format_exc()}")

    def generate_download_link(self, data=None, filename="download.txt",file_extension="text/plain",auto_click=False):
        try:
            # Check for empty file name
            if not filename or len(filename) == 0:
                st.toast("Please enter a valid file name.", icon="❌")
                logger.error("Error in code downloading: Please enter a valid file name.")
                return
            
            # Check for empy data
            if not data or len(data.strip()) == 0:
                st.toast("Data is empty. Cannot download an empty file.", icon="❌")
                logger.error("Error in code downloading: Data is empty.")
                return
            
            # Get the file extension if not provided
            if not file_extension or len(file_extension) == 0:
                file_extension = filename.split(".")[-1]
            
            logger.info(f"Downloading code to file: {filename} with extension: {file_extension}")
            b64 = base64.b64encode(data.encode()).decode()  # encode the data to base64
            href = f"data:text/plain;charset=utf-8;base64,{b64}"  # creating the href for anchor tag
            link = f'<a id="download_link" href="{href}" download="{filename}">Download Code</a>'  # creating the anchor tag
            # JavaScript code to automatically click the link
            auto_click_js = "<script>document.getElementById('download_link').click();</script>"
            
            if auto_click:
                st.components.v1.html(st.session_state.download_link, height=0, scrolling=False)
                
            return link + auto_click_js  # return the anchor tag and JavaScript code
            
        except Exception as e:
            st.toast(traceback.format_exc())
            logger.error(f"Error in code downloading: {traceback.format_exc()}")



    # # Initialize Vertex AI
    def load_enviroment_variables(self, credentials_file_path, project, region):
        """
        Consider running `gcloud config set project` or setting the GOOGLE_CLOUD_PROJECT environment variable
        """
        """Load environment variables"""
        if credentials_file_path:
            logger.info(f"Loading credentials from {credentials_file_path}")
            try:
                credentials = service_account.Credentials.from_service_account_file(credentials_file_path)
                session = requests.AuthorizedSession(credentials)
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = session.credentials.refresh(requests.Request()).token
            except exceptions.GoogleAuthError as e:
                logger.error(f"Failed to load the service account key: {e}")
                st.toast(f"Failed to load the service account key: {e}", icon="❌")
                return False
        else:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            logger.info("Loading credentials from .env file")
            
        
        if project:
            logger.info(f"Setting project to {project}")
            os.environ["GOOGLE_CLOUD_PROJECT"] = project
        else:
            os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT")
            logger.info("Loading project from .env file")
        
        if region:
            logger.info(f"Setting region to {region}")
            os.environ["GOOGLE_CLOUD_REGION"] = region
        else:
            os.environ["GOOGLE_CLOUD_REGION"] = os.getenv("GOOGLE_CLOUD_REGION")
            logger.info("Loading region from .env file")
            
    # Create method which takes string and calulate its number of words,letter count and for each 1000 characters in that string it will multiply with $0.0005 and return the cost, cost per whole string and total cost..
    def calculate_code_generation_cost(self,string,price=0.0005):
        # Calculate number of words
        number_of_words = len(string.split())
        
        # Calculate number of letters
        number_of_letters = len(string)
        
        # Calculate cost
        cost = price * (number_of_letters / 1000)
        
        # Calculate cost per whole string
        cost_per_whole_string = price * (len(string) / 1000)
        
        # Calculate total cost
        total_cost = cost * number_of_words
        
        # Return the cost, cost per whole string and total cost
        return cost, cost_per_whole_string, total_cost

    def codey_generation_cost(self,string):
        codey_price = 0.0005
        return self.calculate_code_generation_cost(string,codey_price)

    def gpt_3_generation_cost(self,string):
        chatgpt_price = 0.0002
        return self.calculate_code_generation_cost(string,chatgpt_price)

    def gpt_3_5_turbo_generation_costself(self,string):
        chatgpt_price = 0.0080
        return self.calculate_code_generation_cost(string,chatgpt_price)

    def gpt_4_generation_cost(self,string):
        chatgpt_price = 0.06
        return self.calculate_code_generation_cost(string,chatgpt_price)
    
    def gpt_text_davinci_generation_cost(self,string):
        chatgpt_price = 0.0060
        return self.calculate_code_generation_cost(string,chatgpt_price)