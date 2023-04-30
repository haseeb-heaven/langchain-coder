![cover_logo](https://github.com/haseeb-heaven/LangChain-CoderAI/blob/master/resources/app_logo.png?raw=true "")
# LangChain Coder

This is **LangChain Coder**, a Streamlit app that utilizes LangChain and OpenAI's GPT-3 to generate code. It supports four different programming languages: Python, C, C++, and Javascript. </br>
With this app, you can **Generate code** and **Run it locally**, providing an alternative to the OpenAI **Code Interpreter Plugin**.
And this can also **Save Code** localy to a file for later use.

## WebUI - Application showcase.
This is the main screen of the application. It has a text input for the prompt, a dropdown menu for selecting the programming language, and three buttons: **Generate Code**, **Run Code**, and **Save Code**.</br>
![main_screen_ui](https://github.com/haseeb-heaven/LangChain-CoderAI/blob/master/resources/main_screen_ui.png?raw=true "")

This is the screen after code generation. It displays the generated code.</br>
![generated_code_ui](https://github.com/haseeb-heaven/LangChain-CoderAI/blob/master/resources/generated_code_ui.png?raw=true "")

## Requirements

This app requires the following libraries:

- streamlit
- langchain
- openai
- dotenv

This app requres compiler for following languages:
- C: GCC (GNU Compiler Collection). You can download it from the official GCC website: https://gcc.gnu.org/install/
- C++: GCC (GNU Compiler Collection). You can download it from the official GCC website: https://gcc.gnu.org/install/
- Python: The Python interpreter is already installed on most systems. If it's not installed on your system, you can download it from the official Python website: https://www.python.org/downloads/
- Javascript: Node.js. You can download it from the official Node.js website: https://nodejs.org/en/download/

## Getting Started

To use this tool, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages using the following command: 

```pip install -r requirements.txt```

4. To generate code you need [OpenAI API key](https://platform.openai.com/account/api-keys) </br>
You can set the API key as an environment variable using the following command:

```export OPENAI_API_KEY=<your API key>```

For Windows, use the following command instead:

```set OPENAI_API_KEY=<your API key>```
5. To run the program, execute the following command:

```streamlit run LangChain-Coder.py```

## Features:

- **Code Generation**: LangChain Coder generates code by utilizing LangChain and OpenAI's GPT-3. It prompts the user for a description of the code they want to generate and the programming language they want to use. The app then generates the code based on the prompt and returns it to the user.

- **Code Execution**: LangChain Coder can execute the code locally. Once the code has been generated, the user can click on the **Run Code** button to execute it. The app will display the output of the code execution.

- **Code Saving**: LangChain Coder also provides the option to save the generated code to a file. To save the code, enter a filename in the text input and click on the **Save Code** button.

- **Multiple Programming Languages**: LangChain Coder supports four different programming languages: _Python, C, C++, and Javascript_.

## Usage

To use LangChain Coder, follow these steps:

1. Enter a prompt to **Generate** the code.
2. Select the _programming language_ you want to use.
3. Click on the **Generate Code** button to generate the code.
4. If you want to run the code, click on the **Run Code** button.
5. If you want to save the code to a file, enter a filename and click on the **Save Code** button.

## Demo Usage.
<a href="https://drive.google.com/file/d/1nXdmZYL2kZtQLm0k4TIGaUgU8CW_YHZ7/view?usp=sharing" target="_blank">
  <img src="https://github.com/haseeb-heaven/LangChain-CoderAI/blob/master/resources/generated_code_ui.png" alt="Demo" width="480" height="320" border="10" />
</a>


## Author
This app was created by HeavenHM.
