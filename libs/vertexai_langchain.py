import re
import traceback
from langchain import LLMChain, PromptTemplate
from langchain.llms import VertexAI
from libs.logger import logger
import streamlit as st

class VertexAILangChain:
    def __init__(self, project, location, model_name, max_output_tokens, temperature, credentials_file_path):
        self.project = project
        self.location = location
        self.model_name = model_name
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.credentials_file_path = credentials_file_path
        self.vertexai_llm = None

    def load_model(self):
        try:
            logger.info(f"Loading model... with project: {self.project} and location: {self.location}")
            
            # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
            from google.oauth2 import service_account
            credentials = service_account.Credentials.from_service_account_file(self.credentials_file_path)

            logger.info(f"Trying to set Vertex model with parameters: {self.model_name}, {self.max_output_tokens}, {self.temperature}, {self.location}")
            self.vertexai_llm = VertexAI(
                model_name=self.model_name,
                max_output_tokens=self.max_output_tokens,
                temperature=self.temperature,
                verbose=True,
                location=self.location,
                credentials=credentials,
            )
            logger.info("Vertex model loaded successfully.")
            return True
        except Exception as exception:
            logger.error(f"Error loading Vertex model: {str(exception)}")
            logger.error(traceback.format_exc())  # Add traceback details
            return False

    def generate_code(self, code_prompt, code_language):
        try:
            # Dynamically construct guidelines based on session state
            guidelines_list = []
            logger.info(f"Generating code with parameters: {code_prompt}, {code_language}")
            
            if st.session_state["coding_guidelines"]["modular_code"]:
                logger.info("Modular code is enabled.")
                guidelines_list.append("- Ensure the method is modular in its approach.")
            if st.session_state["coding_guidelines"]["exception_handling"]:
                logger.info("Exception handling is enabled.")
                guidelines_list.append("- Integrate robust exception handling.")
            if st.session_state["coding_guidelines"]["error_handling"]:
                logger.info("Error handling is enabled.")
                guidelines_list.append("- Add error handling to each module.")
            if st.session_state["coding_guidelines"]["efficient_code"]:
                logger.info("Efficient code is enabled.")
                guidelines_list.append("- Optimize the code to ensure it runs efficiently.")
            if st.session_state["coding_guidelines"]["robust_code"]:
                logger.info("Robust code is enabled.")
                guidelines_list.append("- Ensure the code is robust against potential issues.")
            if st.session_state["coding_guidelines"]["naming_conventions"]:
                logger.info("Naming conventions is enabled.")
                guidelines_list.append("- Follow standard naming conventions.")
            
            logger.info("Guidelines: " + str(guidelines_list))

            # Convert the list to a string
            guidelines = "\n".join(guidelines_list)

            template = f"""
            Task: Design a program {{code_prompt}} in {{code_language}} with the following guidelines and
            make sure the program doesn't ask for any input from the user and the output is printed on the screen.
            
            Guidelines:"""
            template += guidelines
            
            prompt = PromptTemplate(template=template,input_variables=["code_prompt", "code_language"])
            formatted_prompt = prompt.format(code_prompt=code_prompt, code_language=code_language)
            logger.info(f"Formatted prompt: {formatted_prompt}")
            
            logger.info("Setting up LLMChain...")
            llm_chain = LLMChain(prompt=prompt, llm=self.vertexai_llm)
            logger.info("LLMChain setup successfully.")
            
            # Pass the required inputs as a dictionary to the chain
            logger.info("Running LLMChain...")
            response = llm_chain.run({"code_prompt": code_prompt, "code_language": code_language})
            if response or len(response) > 0:
                logger.info(f"Code generated successfully: {response}")
                # Extract text inside code block
                generated_code = re.search('```(.*)```', response, re.DOTALL).group(1)
                if generated_code:
                    # Skip the language name in the first line.
                    response = generated_code.split("\n", 1)[1]
                    logger.info(f"Code generated successfully: {response}")
                else:
                    logger.error(f"Error generating code: {response}")
                    st.toast(f"Error generating code: {response}", icon="❌")
            return response
        except Exception as exception:
            stack_trace = traceback.format_exc()
            logger.error(f"Error generating code: {str(exception)} stack trace: {stack_trace}")
            st.toast(f"Error generating code: {str(exception)} stack trace: {stack_trace}", icon="❌")



