# general_utils.py
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
    
    def run_code(self,code, language):
        logger.info(f"Running code: {code} in language: {language}")

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