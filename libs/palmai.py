import os
import traceback
import google.generativeai as palm
from dotenv import load_dotenv
from libs.logger import logger
import streamlit as st
import libs.general_utils

class PalmAI:
    def __init__(self,api_key, model="text-bison-001", temperature=0.3, max_output_tokens=2048, mode="balanced"):
        """
        Initialize the PalmAI class with the given parameters.
        """
        self.model = "models/" + model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.mode = mode
        self.api_key = None
        self.top_k = 20
        self.top_p = 0.85
        self._configure_api(api_key)
        self.utils = libs.general_utils.GeneralUtils()
        
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

    def _configure_api(self,api_key=None):
        """
        Configure the palm API with the API key from the environment.
        """
        try:
            if api_key is None or len(api_key) == 0:
                load_dotenv()
                self.api_key = os.getenv('PALMAI_API_KEY')
                logger.warn("API value is {}".format(self.api_key))
                if self.api_key is None or len(self.api_key) == 0:
                    raise Exception("API key not found in environment variables.")
                else:
                    st.toast("API key loaded from environment variables.", icon="✅")
            else:
                self.api_key = api_key
                st.toast("API key provided from settings.", icon="✅")
            palm.configure(api_key=self.api_key)
            logger.info("Palm API configured successfully.")
        except Exception as exception:
            logger.error(f"Error occurred while configuring Palm API: {exception}")
            st.toast(f"Error occurred while configuring Palm API: {exception}", icon="❌")

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
                
            # Plain and Simple Coding Task Prompt
            prompt = f"""
            Task: You're an experienced developer. Your mission is to create a program for {code_prompt} in {code_language} that takes {st.session_state.code_input} as input.

            Your goal is clear: Craft a solution that showcases your expertise as a coder and problem solver.

            Ensure that the program's output contains only the code you've written, with no extraneous information.

            Show your skills and solve this challenge with confidence!
            
            And follow the proper coding guidelines and dont add comment unless instructed to do so.
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
                #safety_settings=[{"category":"HARM_CATEGORY_DEROGATORY","threshold":1},{"category":"HARM_CATEGORY_TOXICITY","threshold":1},{"category":"HARM_CATEGORY_VIOLENCE","threshold":2},{"category":"HARM_CATEGORY_SEXUAL","threshold":2},{"category":"HARM_CATEGORY_MEDICAL","threshold":2},{"category":"HARM_CATEGORY_DANGEROUS","threshold":2}],
            )
            logger.info("Text generation completed successfully.")
            
            code = None
            if palm_completion:
                # extract the code from the palm completion
                code = palm_completion.result
                logger.info(f"Palm coder is initialized.")
                logger.info(f"Generated code: {code[:100]}...")
            
            if palm_completion:
                # Extracted code from the palm completion
                extracted_code = self.utils.extract_code(code)
                
                # Check if the code or extracted code is not empty or null
                if not code or not extracted_code:
                    raise Exception("Error: Generated code or extracted code is empty or null.")
                
                return extracted_code
            else:
                raise Exception("Error in code generation: Please enter a valid code.")
            
        except Exception as exception:
            st.toast(f"Error in code generation: {exception}", icon="❌")
            logger.error(f"Error in code generation: {traceback.format_exc()}")

    def fix_generated_code(self, code, code_language, fix_instructions=""):
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
                logger.info(f"Fixing code {code[:100]}... in language {code_language} and error is {st.session_state.stderr}")
                
                # Improved instructions template
                template = f"""
                Task: Correct the code snippet provided below in the {code_language} programming language, following the given instructions {fix_instructions}

                {code}

                Instructions for Fixing:
                1. Identify and rectify any syntax errors, logical issues, or bugs in the code.
                2. Ensure that the code produces the desired output.
                3. Comment on each line where you make changes, explaining the nature of the fix.
                4. Verify that the corrected code is displayed in the output.

                Please make sure that the fixed code is included in the output, along with comments detailing the modifications made.
                """

                # If there was an error in the previous execution, include it in the prompt
                if st.session_state.stderr:
                    logger.info(f"Error in previous execution: {st.session_state.stderr}")
                    st.toast(f"Error in previous execution: {st.session_state.stderr}", icon="❌")
                    template += f"\nFix the following error: {st.session_state.output}"
                    
                    # Check if the error indicates a missing or unavailable module
                    error_message = st.session_state.output.lower()  # Convert to lowercase for case-insensitive matching

                else:
                    st.toast("No error in previous execution.", icon="✅")
                    return code

                # Prompt Templates
                code_template = template
                
                # LLM Chains definition
                # Create a chain that generates the code
                palm_completion = palm.generate_text(
                    model=self.model,
                    prompt=code_template,
                    temperature=self.temperature,
                    max_output_tokens=self.max_output_tokens,
                    top_k=self.top_k,
                    top_p=self.top_p,
                    stop_sequences=[]
                )

                if palm_completion:
                    # Extracted code from the palm completion
                    code = palm_completion.result
                    extracted_code = self.utils.extract_code(code)
                    
                    # Check if the code or extracted code is not empty or null
                    if not code or not extracted_code:
                        raise Exception("Error: Generated code or extracted code is empty or null.")
                    else:
                        return extracted_code
                else:
                    raise Exception("Error in code fixing: Please enter a valid code.")
            else:
                st.toast("Error in code fixing: Please enter a valid code and language.", icon="❌")
                logger.error("Error in code fixing: Please enter a valid code and language.")
        except Exception as exception:
            st.toast(f"Error in code fixing: {exception}", icon="❌")
            logger.error(f"Error in code fixing: {traceback.format_exc()}")

    def convert_generated_code(self, code, code_language):
        """
        Function to convert the generated code to a different language using the palm API.
        """
        try:
            # Check for valid code
            if not code or len(code) == 0:
                logger.error("Error in code conversion: Please enter a valid code.")
                return
            
            logger.info(f"Converting code")
            if code and len(code) > 0:
                logger.info(f"Converting code {code[:100]}... to language {code_language}")
                
                # Improved instructions template
                template = f"""
                Task: Convert the code snippet provided below to the {code_language} programming language, following the given instructions:

                {code}

                Instructions for Conversion:
                1. Identify the functionality of the original code.
                2. Translate the code into the {code_language} programming language, maintaining the same functionality.
                3. Verify that the converted code is displayed in the output.

                Please make sure only the converted code should be included in the output.
                """

                # Prompt Templates
                code_template = template
                
                # LLM Chains definition
                # Create a chain that generates the code
                palm_completion = palm.generate_text(
                    model=self.model,
                    prompt=code_template,
                    temperature=self.temperature,
                    max_output_tokens=self.max_output_tokens,
                    top_k=self.top_k,
                    top_p=self.top_p,
                    stop_sequences=[]
                )

                if palm_completion:
                    # Extracted code from the palm completion
                    code = palm_completion.result
                    extracted_code = self.utils.extract_code(code)
                    
                    # Check if the code or extracted code is not empty or null
                    if not code or not extracted_code:
                        raise Exception("Error: Generated code or extracted code is empty or null.")
                    else:
                        return extracted_code
                else:
                    raise Exception("Error in code conversion: Please enter a valid code.")
            else:
                logger.error("Error in code conversion: Please enter a valid code and language.")
        except Exception as exception:
            st.toast(f"Error in code conversion: {exception}", icon="❌")
            logger.error(f"Error in code conversion: {traceback.format_exc()}")