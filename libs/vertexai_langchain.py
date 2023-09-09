import re
import traceback
from langchain import LLMChain, PromptTemplate
from langchain.llms import VertexAI
from libs.logger import logger
import streamlit as st
from google.oauth2 import service_account
from langchain.prompts import ChatPromptTemplate
  
class VertexAILangChain:
    def __init__(self, project="", location="us-central1", model_name="code-bison", max_tokens=256, temperature:float=0.3, credentials_file_path=None):
        self.project = project
        self.location = location
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.credentials_file_path = credentials_file_path
        self.vertexai_llm = None

    def load_model(self, model_name, max_tokens, temperature):
        try:
            logger.info(f"Loading model... with project: {self.project} and location: {self.location}")
            # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
            credentials = service_account.Credentials.from_service_account_file(self.credentials_file_path)

            logger.info(f"Trying to set Vertex model with parameters: {model_name or self.model_name}, {max_tokens or self.max_tokens}, {temperature or self.temperature}, {self.location}")
            self.vertexai_llm = VertexAI(
                model_name=model_name or self.model_name,
                max_output_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
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
            
            # Check for empty or null code prompt and code language
            if not code_prompt or len(code_prompt) == 0:
                logger.error("Code prompt is empty or null.")
                st.toast("Code prompt is empty or null.", icon="❌")
                return None
            
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

            # Setting Prompt Template.
            input_section = f"Given the input for code: {st.session_state.code_input}" if st.session_state.code_input else "make sure the program doesn't ask for any input from the user"

            template = f"""
            Task: Design a program {{code_prompt}} in {{code_language}} with the following guidelines and
            make sure the output is printed on the screen.
            And make sure the output contains only the code and nothing else.
            {input_section}

            Guidelines:
            {guidelines}
            """
            
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
                if response.startswith("```") or response.endswith("```"):
                    try:
                        generated_code = re.search('```(.*)```', response, re.DOTALL).group(1)
                    except AttributeError:
                        generated_code = response
                else:
                    st.toast(f"Error extracting code", icon="❌")
                    return response
                    
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

    def generate_code_completion(self, code_prompt, code_language):
        try:
            if not code_prompt or len(code_prompt) == 0:
                logger.error("Code prompt is empty or null.")
                st.error("Code generateration cannot be performed as the code prompt is empty or null.")
                return None
            
            logger.info(f"Generating code completion with parameters: {code_prompt}, {code_language}")
            template = f"Complete the following {{code_language}} code: {{code_prompt}}"
            prompt_obj = PromptTemplate(template=template, input_variables=["code_language", "code_prompt"])
            
            max_tokens = st.session_state["vertexai"]["max_tokens"]
            temprature = st.session_state["vertexai"]["temperature"]
            
            # Check the maximum number of tokens of Gecko model i.e 65
            if max_tokens > 65:
                max_tokens = 65
                logger.info(f"Maximum number of tokens for Model Gecko can't exceed 65. Setting max_tokens to 65.")
                st.toast(f"Maximum number of tokens for Model Gecko can't exceed 65. Setting max_tokens to 65.", icon="⚠️")
                
            self.model_name = "code-gecko" # Define the code completion model name.
            self.llm = VertexAI(model_name=self.model_name,max_output_tokens=max_tokens, temperature=temprature)
            logger.info(f"Initialized VertexAI with model: {self.model_name}")
            llm_chain = LLMChain(prompt=prompt_obj, llm=self.llm)
            response = llm_chain.run({"code_prompt": code_prompt, "code_language": code_language})
            
            if response:
                logger.info(f"Code completion generated successfully: {response}")
                return response
            else:
                logger.warning("No response received from LLMChain.")
                return None
        except Exception as e:
            logger.error(f"Error generating code completion: {str(e)}")
            raise

    def set_temperature(self, temperature):
        self.temperature = temperature
        self.vertexai_llm.temperature = temperature
        # call load_model to reload the model with the new temperature and rest values should be same
        self.load_model(self.model_name, self.max_tokens, self.temperature)
        
    def set_max_tokens(self, max_tokens):
        self.max_tokens = max_tokens
        self.vertexai_llm.max_output_tokens = max_tokens
        # call load_model to reload the model with the new max_output_tokens and rest values should be same
        self.load_model(self.model_name, self.max_tokens, self.temperature)
        
    def set_model_name(self, model_name):
        self.model_name = model_name
        # call load_model to reload the model with the new model_name and rest values should be same
        self.load_model(self.model_name, self.max_tokens, self.temperature)



