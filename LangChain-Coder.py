# Importing the libraries
import tempfile
import subprocess
import traceback
import sys
import os
from io import StringIO
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain, SimpleSequentialChain
from langchain.memory import ConversationBufferMemory
import langchain.agents as lc_agents
from langchain.llms import OpenAI
import logging
from datetime import datetime
from langchain.llms import OpenAI as LangChainOpenAI
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# App title and description
st.title("LangChain Coder - 🦜🔗")
code_prompt = st.text_input("Enter a prompt to generate the code")
code_language = st.selectbox("Select the language", [
                             "C", "Cpp", "Python", "Javascript"])

# Buttons
button_generate = st.button("Generate Code")
button_run = st.button("Run Code")
button_generate_run = st.button("Generate and Run Code")

# Prompt Templates
code_template = PromptTemplate(
    input_variables=['topic'],
    template='Write me code in ' + f'{code_language} language' + ' for {topic}'
)

code_fix_template = PromptTemplate(
    input_variables=['topic'],
    template='Fix any error in the following code in ' + f'{code_language} language' + ' for {topic}'
)

# Memory for the conversation
memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')

# LLM Chains definition
# Create an OpenAI LLM model
open_ai_llm = OpenAI(temperature=0.7, max_tokens=1000)

# Create a chain that generates the code
code_chain = LLMChain(llm=open_ai_llm, prompt=code_template, output_key='code', memory=memory, verbose=True)

# Create a chain that fixes the code
code_fix_chain = LLMChain(llm=open_ai_llm, prompt=code_fix_template, output_key='code_fix', memory=memory,verbose=True)

# Create a sequential chain that combines the two chains above
sequential_chain = SequentialChain(chains=[code_chain, code_fix_chain],input_variables=['topic'],output_variables=['code', 'code_fix'])

global generated_code


def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%H:%M:%S",
        filename=log_file,  # Add this line to save logs to a file
        filemode='a',  # Append logs to the file
    )


# Setup logging
log_file = __file__.replace(".py", ".log")
setup_logging(log_file)


# Create a class
class PythonREPL:
    # Define the initialization method
    def __init__(self):
        pass

    # Define the run method
    def run(self, command: str) -> str:
        # Store the current value of sys.stdout
        old_stdout = sys.stdout
        # Create a new StringIO object
        sys.stdout = mystdout = StringIO()
        # Try to execute the code
        try:
            # Execute the code
            exec(command, globals())
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        # If an error occurs, print the error message
        except Exception as e:
            # Restore the original value of sys.stdout
            sys.stdout = old_stdout
            # Get the error message
            output = str(e)
        return output


def run_query(query, model_kwargs, max_iterations):
    # Create a LangChainOpenAI object
    llm = LangChainOpenAI(**model_kwargs)
    # Create the python REPL tool
    python_repl = lc_agents.Tool("Python REPL", PythonREPL().run,
                                "A Python shell. Use this to execute python commands.")
    # Create a list of tools
    tools = [python_repl]
    # Initialize the agent
    agent = lc_agents.initialize_agent(tools, llm, agent=lc_agents.AgentType.ZERO_SHOT_REACT_DESCRIPTION,model_kwargs=model_kwargs, verbose=True, max_iterations=max_iterations)
    # Run the agent
    response = agent.run(query)


def run_code(code, language):
    logger = logging.getLogger(__name__)
    logger.info(f"Running code: {code} in language: {language}")

    if language == "Python":
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=True) as f:
            f.write(code)
            f.flush()

            logger.info(f"Input file: {f.name}")
            output = subprocess.run(
                ["python", f.name], capture_output=True, text=True)
            logger.info(f"Output execution: {output.stdout + output.stderr}")
            return output.stdout + output.stderr

    elif language == "C" or language == "Cpp":
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
                logger.info(
                    f"Output execution: {run_output.stdout + run_output.stderr}")
                return run_output.stdout + run_output.stderr

    elif language == "Javascript":
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=True) as f:
            f.write(code)
            f.flush()

            print(f"Input file: {f.name}")
            output = subprocess.run(
                ["node", f.name], capture_output=True, text=True)
            print(f"Output execution: {output.stdout + output.stderr}")
            return output.stdout + output.stderr

    else:
        return "Unsupported language."


# Session state variables
if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

if "code_language" not in st.session_state:
    st.session_state.code_language = ""

# Generate the code
if button_generate or button_generate_run and code_prompt:
    logger = logging.getLogger(__name__)
    try:
        st.session_state.generated_code = code_chain.run(code_prompt)
        st.session_state.code_language = code_language
        st.code(st.session_state.generated_code,language=st.session_state.code_language.lower())

        with st.expander('Message History'):
            st.info(memory.buffer)
    except Exception as e:
        st.write(traceback.format_exc())
        logger.error(f"Error in code generation: {traceback.format_exc()}")

# Execute the code
if button_run or button_generate_run and code_prompt:
    logger = logging.getLogger(__name__)
    try:
        logger.info(f"Running code: {st.session_state.generated_code} in language: {st.session_state.code_language}")
        output = run_code(st.session_state.generated_code,st.session_state.code_language)
        logger.info(f"Output execution: {output}")

        if "error" in output.lower() or "exception" in output.lower() or "SyntaxError" in output.lower() or "NameError" in output.lower():
                
            logger.error(f"Error in code execution: {output}")
            response = sequential_chain({'topic': st.session_state.generated_code})
            fixed_code = response['code_fix']
            st.code(fixed_code, language=st.session_state.code_language.lower())

            with st.expander('Message History'):
                st.info(memory.buffer)
            logger.warning(f"Trying to run fixed code: {fixed_code}")
            output = run_code(fixed_code, st.session_state.code_language)
            logger.warning(f"Fixed code output: {output}")
        if not button_generate_run:
            st.code(st.session_state.generated_code,language=st.session_state.code_language.lower())
        st.write("Execution Output:")
        st.write(output)
        logger.info(f"Execution Output: {output}")

    except Exception as e:
        st.write("Error in code execution:")
        # print stack trace
        st.write(traceback.format_exc())
        logger.error(f"Error in code execution: {traceback.format_exc()}")
