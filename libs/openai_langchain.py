import traceback
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from libs.logger import logger
import openai
from dotenv import load_dotenv

class OpenAILangChain:
    code_chain = None
    code_language = 'Python'
    
    def __init__(self,code_language="python",temprature:float=0.3,max_tokens=1000,model="text-davinci-003",api_key=None):
        code_prompt = st.session_state.code_prompt
        code_language = st.session_state.code_language
        logger.info(f"Initializing LangChainCoder... with parameters: {code_language}, {temprature}, {max_tokens}, {model} {code_prompt}")

        
        # Load the environment variables
        load_dotenv()
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        memory = ConversationBufferMemory(input_key='code_prompt', memory_key='chat_history')
        
        # give info of selected source for API key
        if api_key:
            pass
            #st.toast("Using API key from input", icon="🔑")
        else:
            st.toast("Using API key from .env file", icon="🔑")
        
        self.code_language = code_language
        
        # Dynamically construct guidelines based on session state
        guidelines_list = []

        if st.session_state["coding_guidelines"]["modular_code"]:
            guidelines_list.append("- Ensure the method is modular in its approach.")
        if st.session_state["coding_guidelines"]["exception_handling"]:
            guidelines_list.append("- Integrate robust exception handling.")
        if st.session_state["coding_guidelines"]["error_handling"]:
            guidelines_list.append("- Add error handling to each module.")
        if st.session_state["coding_guidelines"]["efficient_code"]:
            guidelines_list.append("- Optimize the code to ensure it runs efficiently.")
        if st.session_state["coding_guidelines"]["robust_code"]:
            guidelines_list.append("- Ensure the code is robust against potential issues.")
        if st.session_state["coding_guidelines"]["naming_conventions"]:
            guidelines_list.append("- Follow standard naming conventions.")

        # Convert the list to a string
        guidelines = "\n".join(guidelines_list)

        template = f"""
        Task: Design a program {{code_prompt}} in {{code_language}} with the following guidelines and
        make sure the program doesn't ask for any input from the user and the output is printed on the screen.
        
        Guidelines:"""
        template += guidelines
        
        # Prompt Templates
        code_template = PromptTemplate(input_variables=["code_prompt", "code_language"], template=template)
        code_fix_template = PromptTemplate(input_variables=['code_prompt'],template='Fix any error in the following code in ' +f'{code_language} language' + ' for {code_prompt}')
        # LLM Chains definition
        
        # Create an OpenAI LLM model
        open_ai_llm = OpenAI(temperature=temprature, max_tokens=max_tokens, model=model,openai_api_key=openai.api_key)

        # Create a chain that generates the code
        self.code_chain = LLMChain(llm=open_ai_llm, prompt=code_template,output_key='code', memory=memory, verbose=True)

        # Create a chain that fixes the code
        code_fix_chain = LLMChain(llm=open_ai_llm, prompt=code_fix_template,output_key='code_fix', memory=memory, verbose=True)

        # Create a sequential chain that combines the two chains above
        sequential_chain = SequentialChain(chains=[self.code_chain, code_fix_chain], input_variables=['code_prompt','code_language'], output_variables=['code', 'code_fix'])
        
        # Save the chain in the session state
        if "sequential_chain" not in st.session_state:
            st.session_state.sequential_chain = sequential_chain

    def generate_code(self,code_prompt,code_language):
        try:
            logger.info(f"Generating code for prompt: {code_prompt} in language: {code_language}")
            if code_prompt and len(code_prompt) > 0 and code_language and len(code_language) > 0:
                logger.info(f"Generating code for prompt: {code_prompt} in language: {code_language}")
                
                if self.code_chain:
                    logger.info(f"Code chain is initialized.")
                    st.session_state.generated_code = self.code_chain.run({"code_prompt": code_prompt, "code_language": code_language})
                    logger.info(f"Generated code: {st.session_state.generated_code[:100]}...")

                # Memory for the conversation
                memory = ConversationBufferMemory(input_key='code_prompt', memory_key='chat_history')

                # save the memory in the session state
                if "memory" in st.session_state:
                    st.session_state.memory = memory
                
                with st.expander('Message History'):
                    st.info(memory.buffer)
                return st.session_state.generated_code
            else:
                st.toast("Error in code generation: Please enter a valid prompt and language.", icon="❌")
                logger.error("Error in code generation: Please enter a valid prompt and language.")
        except Exception as e:
            st.toast(f"Error in code generation: {traceback.format_exc()}", icon="❌")
            logger.error(f"Error in code generation: {traceback.format_exc()}")