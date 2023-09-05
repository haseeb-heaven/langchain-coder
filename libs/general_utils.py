# general_utils.py
import os
import tempfile
from libs.logger import logger
import subprocess
import traceback
import dotenv
import streamlit as st
from libs.lang_codes import LangCodes

class GeneralUtils:
    
    def execute_code(self,compiler_mode: str):
        logger.info(f"Executing code: {st.session_state.generated_code[:100]} in language: {st.session_state.code_language} with Compiler Mode: {compiler_mode}")

        try:
            if compiler_mode.lower() == "online":
                html_template = self.generate_dynamic_html(st.session_state.code_language, st.session_state.generated_code)
                st.components.v1.html(html_template, width=720, height=800, scrolling=True)
                logger.info(f"HTML Template: {html_template}")

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

                #st.code(st.session_state.generated_code,language=st.session_state.code_language.lower())
                st.write("Execution Output:")
                st.write(output)
                logger.info(f"Execution Output: {output}")

        except Exception as e:
            st.write("Error in code execution:")
            # Output the stack trace
            st.write(traceback.format_exc())
            logger.error(f"Error in code execution: {traceback.format_exc()}")
    
        # Generate Dynamic HTML for JDoodle Compiler iFrame Embedding.
    def generate_dynamic_html(self,language, code_prompt):
        logger.info("Generating dynamic HTML for language: %s", language)
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Python App with JavaScript</title>
        </head>
        <body>
            <div data-pym-src='https://www.jdoodle.com/plugin' data-language="{language}"
                data-version-index="0" data-libs="">
                {script_code}
            </div>
            <script src="https://www.jdoodle.com/assets/jdoodle-pym.min.js" type="text/javascript"></script>
        </body>
        </html>
        """.format(language=LangCodes()[language], script_code=code_prompt)
        return html_template
    
    def run_code(self,code, language):
        logger.info(f"Running code: {code} in language: {language}")

        if language == "Python":
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=True) as f:
                f.write(code)
                f.flush()

                logger.info(f"Input file: {f.name}")
                output = subprocess.run(
                    ["python", f.name], capture_output=True, text=True)
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
            with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=True) as f:
                f.write(code)
                f.flush()

                logger.info(f"Input file: {f.name}")
                output = subprocess.run(
                    ["node", f.name], capture_output=True, text=True)
                logger.info(f"Runner Output execution: {output.stdout + output.stderr}")
                return output.stdout + output.stderr

        else:
            return "Unsupported language."

    def save_code(self,file_name):
        try:
            logger.info(f"Saving code to file: {file_name}")
            if file_name:
                with open(file_name, "w") as file:
                    file.write(st.session_state.generated_code)
                st.success(f"Code saved to file {file_name}")
                logger.info(f"Code saved to file {file_name}")
            #st.code(st.session_state.generated_code,language=st.session_state.code_language.lower())

        except Exception as e:
            st.write(traceback.format_exc())
            logger.error(f"Error in code saving: {traceback.format_exc()}")


    # # Initialize Vertex AI
    def load_enviroment_variables(self,credentials_file_path, project, region):
        """
        Consider running `gcloud config set project` or setting the GOOGLE_CLOUD_PROJECT environment variable
        """
        if credentials_file_path:
            logger.info(f"Loading credentials from {credentials_file_path}")
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_file_path
        if project:
            logger.info(f"Setting project to {project}")
            os.environ["GOOGLE_CLOUD_PROJECT"] = project
        if region:
            logger.info(f"Setting region to {region}")
            os.environ["GOOGLE_CLOUD_REGION"] = region
        
        if not credentials_file_path and not project and not region:
            logger.info("Loading credentials from .env file")
            dotenv.load_dotenv()
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT")
            os.environ["GOOGLE_CLOUD_REGION"] = os.getenv("GOOGLE_CLOUD_REGION")