import re
from langchain import LLMChain, PromptTemplate
from langchain.llms import VertexAI
from libs.logger import logger
import streamlit as st

class CodeyLib:
    def __init__(self, project, location, model_name, max_output_tokens, temperature):
        self.project = project
        self.location = location
        self.model_name = model_name
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.llm = None

    def load_model(self):
        try:
            self.llm = VertexAI(
                model_name=self.model_name,
                max_output_tokens=self.max_output_tokens,
                temperature=self.temperature,
                verbose=True,
                location=self.location,
            )
            logger.info("Model loaded successfully.")
        except Exception as exception:
            logger.error(f"Error loading model: {str(exception)}")

    def generate_code(self, question, code_language):
        try:
            template = """
            Task: Design a program {question} in {code_language} with following requirements:

            Requirements:
            - Ensure the method is modular in its approach.
            - Integrate robust exception handling.
            - Add error handling to each module.
            - Optimize the code to ensure it runs efficiently.
            - Ensure the code is robust against potential issues.
            - Follow standard naming conventions.
            """
            prompt = PromptTemplate(input_variables=["question", "code_language"], template=template)
            formatted_prompt = prompt.format(question=question, code_language=code_language)
            
            llm_chain = LLMChain(prompt=prompt, llm=self.llm)
            
            # Pass the required inputs as a dictionary to the chain
            response = llm_chain.run({'question': question, 'code_language': code_language})
            logger.info(f"Code generated successfully: {response}")
            # Extract text inside code block
            generated_code = re.search('```(.*)```', response, re.DOTALL).group(1)
            # Skip the language name in the first line.
            response = generated_code.split("\n", 1)[1]
            logger.info(f"Code generated successfully: {response}")
            return response
        except Exception as exception:
            logger.error(f"Error generating code: {str(exception)}")
            st.error(f"Error generating code: {str(exception)}")

