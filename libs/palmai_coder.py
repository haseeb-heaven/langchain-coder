import logging
import pprint
import os
import traceback
import google.generativeai as palm
from dotenv import load_dotenv
from libs.logger import logger
import streamlit as st


# Set up logging
logging.basicConfig(filename='palm-coder.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PalmAI:
    def __init__(self, model="models/text-bison-001", temperature=0.3, max_output_tokens=2048, mode="balanced"):
        """
        Initialize the PalmAI class with the given parameters.
        """
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.mode = mode
        self.api_key = None
        self.top_k = 20
        self.top_p = 0.85
        self._configure_api()
        
        # Dynamically construct guidelines based on session state
        self.guidelines_list = []

        if st.session_state["coding_guidelines"]["modular_code"]:
            self.guidelines_list.append("- Ensure the method is modular in its approach.")
        if st.session_state["coding_guidelines"]["exception_handling"]:
            self.guidelines_list.append("- Integrate robust exception handling.")
        if st.session_state["coding_guidelines"]["error_handling"]:
            self.guidelines_list.append("- Add error handling to each module.")
        if st.session_state["coding_guidelines"]["efficient_code"]:
            self.guidelines_list.append("- Optimize the code to ensure it runs efficiently.")
        if st.session_state["coding_guidelines"]["robust_code"]:
            self.guidelines_list.append("- Ensure the code is robust against potential issues.")
        if st.session_state["coding_guidelines"]["naming_conventions"]:
            self.guidelines_list.append("- Follow standard naming conventions.")

        # Convert the list to a string
        self.guidelines = "\n".join(self.guidelines_list)

    def _configure_api(self):
        """
        Configure the palm API with the API key from the environment.
        """
        try:
            load_dotenv()
            self.api_key = os.getenv('PALMAI_API_KEY')
            palm.configure(api_key=self.api_key)
            logger.info("Palm API configured successfully.")
        except Exception as e:
            logger.error(f"Error occurred while configuring Palm API: {e}")

    def extract_code(self, code):
        """
        Extracts the code from the provided string.
        If the string contains '```', it extracts the code between them.
        Otherwise, it returns the original string.
        """
        try:
            if '```' in code:
                start = code.find('```') + len('```\n')
                end = code.find('```', start)
                # Skip the first line after ```
                start = code.find('\n', start) + 1
                extracted_code = code[start:end]
                logger.info("Code extracted successfully.")
                return extracted_code
            else:
                logger.info("No special characters found in the code. Returning the original code.")
                return code
        except Exception as e:
            logger.error(f"Error occurred while extracting code: {e}")
            return None
    
    def generate_code(self, code_prompt,code_language):
        """
        Function to generate text using the palm API.
        """
        try:
            # Define top_k and top_p based on the mode
            if self.mode == "precise":
                top_k = 40
                top_p = 0.95
                self.temprature = 0
            elif self.mode == "balanced":
                top_k = 20
                top_p = 0.85
                self.temprature = 0.3
            elif self.mode == "creative":
                top_k = 10
                top_p = 0.75
                self.temprature = 1
            else:
                raise ValueError("Invalid mode. Choose from 'precise', 'balanced', 'creative'.")

            logger.info(f"Generating code with mode: {self.mode}, top_k: {top_k}, top_p: {top_p}")

            
            # check for valid prompt and language
            if not code_prompt or len(code_prompt) == 0:
                st.toast("Error in code generation: Please enter a valid prompt.", icon="❌")
                logger.error("Error in code generation: Please enter a valid prompt.")
                return
            
            logger.info(f"Generating code for prompt: {code_prompt} in language: {code_language}")
            if code_prompt and len(code_prompt) > 0 and code_language and len(code_language) > 0:
                logger.info(f"Generating code for prompt: {code_prompt} in language: {code_language}")
                
            # Construct the prompt
            prompt = f"""
            Task: Design a program {code_prompt} with the following guidelines and
            make sure the output is printed on the screen.
            And make sure the output contains only the code and nothing else.

            Guidelines:
            {self.guidelines}
            """

            palm_completion = palm.generate_text(
                model=self.model,
                prompt=prompt,
                candidate_count=4,
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
                top_k=top_k,
                top_p=top_p,
                stop_sequences=[],
                safety_settings=[{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
            )
            logger.info("Text generation completed successfully.")
            
            # extract the code from the palm completion
            code = palm_completion.result
                        
            if palm_completion:
                logger.info(f"Palm coder is initialized.")
                logger.info(f"Generated code: {code[:100]}...")
                        
            return self.extract_code(code)
        except Exception as e:
            st.toast(f"Error in code generation: {e}", icon="❌")
            logger.error(f"Error in code generation: {traceback.format_exc()}")

    def fix_generated_code(self, code):
        """
        Function to fix the generated code using the palm API.
        """
        try:
            # Check for valid code
            if not code or len(code) == 0:
                logger.error("Error in code fixing: Please enter a valid code.")
                return
            
            logger.info(f"Fixing code")
            if code and len(code) > 0:
                logger.info(f"Fixing code")
                
                # This template is used to generate the prompt for fixing the code
                template = f"""
                Task: Fix the following program {{code}}.
                Make sure the output is printed on the screen.
                And make sure the output contains the full fixed code.
                Add comments in that line where you fixed and what you fixed.
                """
                
                # Prompt Templates
                code_template = template.format(code=code)
                
                # LLM Chains definition
                # Create a chain that generates the code
                completion = palm.generate_text(
                    model=self.model,
                    prompt=code_template,
                    candidate_count=4,
                    temperature=self.temperature,
                    max_output_tokens=self.max_output_tokens,
                    top_k=self.top_k,
                    top_p=self.top_p,
                    stop_sequences=[],
                    safety_settings=[{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
                )
                logger.info("Code fixing completed successfully.")
                
                return self.extract_code(code)

            else:
                st.toast("Error in code fixing: Please enter a valid code and language.", icon="❌")
                logger.error("Error in code fixing: Please enter a valid code and language.")
        except Exception as e:
            st.toast(f"Error in code fixing: {e}", icon="❌")
            logger.error(f"Error in code fixing: {traceback.format_exc()}")