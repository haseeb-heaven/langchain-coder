import traceback
import os
import streamlit as st
from langchain.chat_models import ChatLiteLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from libs.logger import logger
from dotenv import load_dotenv
import libs.general_utils

class OpenAILangChain:
    code_chain = None
    code_language = 'Python'
    lite_llm = None  # Change from open_ai_llm to lite_llm
    memory = None
    
    def __init__(self,code_language="python",temprature:float=0.3,max_tokens=1000,model="gpt-3.5-turbo",api_key=None):
        code_prompt = st.session_state.code_prompt
        code_language = st.session_state.code_language
        self.utils = libs.general_utils.GeneralUtils()

        logger.info(f"Initializing OpenAILangChain... with parameters: {code_language}, {temprature}, {max_tokens}, {model} {code_prompt}")

        # Set the OPENAI_API_KEY environment variable
        load_dotenv()
        
        #st.toast(f"Proxy API value is {st.session_state.proxy_api} and length {len(st.session_state.proxy_api)}", icon="✅")
        if st.session_state.proxy_api != "" and len(st.session_state.proxy_api) > 0 and api_key == None:
            st.toast("Using proxy API", icon="✅")
            os.environ["OPENAI_API_KEY"] = "" # This value is ignored when api_base is set.
        elif api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        # Create a LiteLLM model
        self.lite_llm = ChatLiteLLM(model=model, temperature=temprature, max_tokens=max_tokens, openai_api_key=api_key)
        
        if st.session_state.proxy_api:
            self.lite_llm.api_base = st.session_state.proxy_api
        
        # Define code_template and memory
        code_template = PromptTemplate(input_variables=['code_prompt'],template='Write a code in ' +f'{code_language} language' + ' for {code_prompt}')
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
        
        # Prompt Templates
        code_template = PromptTemplate(input_variables=["code_prompt", "code_language"], template=template)
        # LLM Chains definition
        
        # Create a chain that generates the code
        self.code_chain = LLMChain(llm=self.lite_llm, prompt=code_template,output_key='code', memory=memory, verbose=True)  # Change from open_ai_llm to lite_llm

        # Auto debug chain
        auto_debug_template = PromptTemplate(input_variables=['code_prompt'],template='Debug and fix any error in the following code in ' +f'{code_language} language' + ' for {code_prompt}')
        auto_debug_chain = LLMChain(llm=self.lite_llm, prompt=auto_debug_template,output_key='code_fix', memory=self.memory, verbose=True)  # Change from open_ai_llm to lite_llm
        
        if not st.session_state.auto_debug_chain:
            st.session_state.auto_debug_chain = auto_debug_chain
        
        # Create a sequential chain that combines the two chains above
        sequential_chain = SequentialChain(chains=[self.code_chain, auto_debug_chain], input_variables=['code_prompt','code_language'], output_variables=['code', 'code_fix'])
           
        # Save the chain in the session state
        if "sequential_chain" not in st.session_state:
            st.session_state.sequential_chain = sequential_chain

    def generate_code(self,code_prompt,code_language):
        try:
            
            # check for valid prompt and language
            if not code_prompt or len(code_prompt) == 0:
                st.toast("Error in code generation: Please enter a valid prompt.", icon="❌")
                logger.error("Error in code generation: Please enter a valid prompt.")
                return
            
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
                
                #with st.expander('Message History'):
                    #st.info(memory.buffer)
                code = st.session_state.generated_code
                extracted_code = self.utils.extract_code(code)
                return extracted_code
            else:
                st.toast("Error in code generation: Please enter a valid prompt and language.", icon="❌")
                logger.error("Error in code generation: Please enter a valid prompt and language.")
        except Exception as e:
            st.toast(f"Error in code generation: {e}", icon="❌")
            logger.error(f"Error in code generation: {traceback.format_exc()}")

    def fix_generated_code(self, code_snippet, code_language, fix_instructions=""):
        """
        Function to fix the generated code using the palm API.
        """
        try:
            # Check for valid code
            if not code_snippet or len(code_snippet) == 0:
                logger.error("Error in code fixing: Please enter a valid code.")
                return
            
            logger.info(f"Fixing code")
            if code_snippet and len(code_snippet) > 0:
                logger.info(f"Fixing code {code_snippet[:100]}... in language {code_language} and error is {st.session_state.stderr}")
                
                # Improved instructions template
                template = f"""
                Task: Correct the code snippet provided below in the {code_language} programming language, following the given instructions {fix_instructions}

                {code_snippet}

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
                    return code_snippet

                # Prompt Templates
                code_template = template
                
                # LLM Chains definition
                # Create a chain that fixed the code
                fix_generated_template = PromptTemplate(
                    input_variables=['code_prompt', 'code_language'],
                    template=code_template
                )

                fix_generated_chain = LLMChain(
                    llm=self.lite_llm,
                    prompt=fix_generated_template,
                    output_key='fixed_code',
                    memory=self.memory,
                    verbose=True
                )

                # Prepare the input for the chain
                input_data = {
                    'code_prompt': code_snippet,
                    'code_language': code_language
                }

                # Run the chain
                output = fix_generated_chain.run(input_data)

                logger.info("Text generation completed successfully.")

                if output:
                    # Extracted code from the palm completion
                    fixed_code = output['code_fix']
                    extracted_code = self.utils.extract_code(fixed_code)
                    
                    # Check if the code or extracted code is not empty or null
                    if not code_snippet or not extracted_code:
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