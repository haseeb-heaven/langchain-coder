# LangChain Coder AI README

## 📌 Table of Contents
1. [Introduction](#introduction)
2. [AI Sections](#ai-sections)
3. [Features](#features)
4. [WebUI - Application Showcase](#webui---application-showcase)
5. [Vertex AI Integration](#vertex-ai-integration)
6. [📸 Image Showcase](#📸-image-showcase)
7. [Packages Used](#packages-used)
8. [📚 Links and References](#📚-links-and-references)
9. [Versioning](#versioning)
10. [✍️ Author](#✍️-author)

## Introduction

LangChain Coder AI is a state-of-the-art code generation tool powered by OpenAI and Vertex AI. It provides a seamless experience for developers to generate code snippets in various languages based on the provided prompts. The tool is integrated with advanced AI models like GPT-3.5, GPT-3.5 Turbo, GPT-4, Code Gecko, and Code Bison, ensuring high-quality code outputs.

## Features

- **AI-Powered Code Generation and Completion**: Utilizes OpenAI and Vertex AI models for efficient and accurate code suggestions.
- **Save and Execute Code**: Provides options to save the generated code and execute it instantly.
- **Coding Guidelines**: Ensures the generated code adheres to standards like modularity, exception handling, error handling, logging, comments, efficiency, robustness, memory management, speed optimization, and naming conventions.
- **Advanced Code Editor**: Customize your coding experience with features like adjustable font size, tab size, themes, keybindings, line numbers, print margins, wrapping, auto-updates, read-only mode, and language selection.
- **Customizable Vertex AI Settings**: Adjust settings like temperature, max tokens, model name, project, region, and credentials file for Vertex AI.
- **Offline and Online Compilation Modes**: Choose between offline and online compiler modes for code execution.

## AI-Sections.
### 🤖 OpenAI 
- **Customizable Settings**: Adjust Tokens, Temperature, and set your API Key directly in the settings.
- **Model Selection**: Choose from a variety of models including GPT 3.5, GPT 3.5 Turbo, and the latest GPT 4.

### 🌐 Vertex AI 
- **Customizable Settings**: Fine-tune Tokens, Temperature, and set your API Key in the settings.
- **Model Selection**: Opt for models like **Code Gecko** for completions and **Code Bison** for code generation. These models are designed to support code completion and generation, enhancing your coding experience.


## WebUI - Application Showcase

🌆 This is the main screen of the application. Dive in with a text prompt, choose your language, and let the magic happen with buttons that feel just right.</br>
![langchain-main-screen-ui](https://github.com/haseeb-heaven/LangChain-CoderAI/blob/master/resources/langchain-main-screen-ui.png?raw=true "")

🎨 Behold the canvas after the masterpiece is painted. Code generation was never this beautiful.</br>
![generated_code_ui](https://github.com/haseeb-heaven/LangChain-CoderAI/blob/master/resources/langchain-code-ui.png?raw=true "")

## Vertex AI Integration

LangChain Coder AI integrates with [Google Vertex AI](https://cloud.google.com/python/docs/reference/aiplatform/latest) to leverage its powerful machine learning models for code generation. Vertex AI offers a range of tools and services for ML and AI, and LangChain Coder AI taps into these resources to provide top-notch code suggestions. For more details on how LangChain integrates with Vertex AI, refer to the [official documentation](https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm).

Additionally, the Vertex AI SDK for Python allows for automation of data ingestion, model training, and predictions on Vertex AI. It provides a programmatic way to access most of the functionalities available in the Google Cloud console. For more information, check out the [Vertex AI SDK for Python](https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk).

## 📸 Image Showcase
**__Main Screen UI__**  
*The main screen of the application.*  
![langchain-main-screen-ui](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-main-screen-ui.png?raw=true "")  
</br>

**__Generated Code UI__**  
*Displays the generated code in a user-friendly UI.*  
![generated_code_ui](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-code-ui.png?raw=true "")  
</br>

**__API Rates__**  
*Shows the API rates for LangChain Coder AI.*  
![langchain-api-rates](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-api-rates.png?raw=true "")  
</br>

**__Dark Theme Code Editor__**  
*A dark-themed code editor for a comfortable coding experience.*  
![langchain-code-editor-dark-theme](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-code-editor-dark-theme.png?raw=true "")  
</br>

**__Coding Guidelines__**  
*Highlights the coding guidelines supported by LangChain Coder AI.*  
![langchain-code-guidelines](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-code-guidelines.png?raw=true "")  
</br>

**__Offline Compiler__**  
*Showcases the offline compiler mode for executing code.*  
![langchain-offline-compiler](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-offline-compiler.png?raw=true "")  
</br>

**__Online Compiler__**  
*The online compiler mode with support for multiple languages.*  
![langchain-online-compiler](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-online-compiler.png?raw=true "")  
</br>

**__Swift Code Demo__**  
*A demonstration showcasing Swift code generation.*  
![langchain-swift-code-demo](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-swift-code-demo.png?raw=true "")  
</br>

**__Vertex AI Code Gecko__**  
*Illustrates the code completion feature of Vertex AI Code Gecko.* 
![langchain-vertex-ai-code-gecko](https://github.com/haseeb-heaven/LangChain-Coder/blob/master/resources/langchain-vertex-ai-code-gecko.png?raw=true "")  
</br>




## Packages Used

- **streamlit**: A fast and simple way to create data apps.
- **streamlit_ace**: A Streamlit component for the Ace editor.
- **google-auth**: A Google Authentication Library.
- **google-auth-oauthlib**: A Google Authentication Library for OAuth.
- **google-cloud-aiplatform**: A client library for interacting with the Vertex AI API.
- **langchain**: A Python client library for interacting with the LangChain API.
- **openai**: A Python client library for interacting with the OpenAI API.
- **python-dotenv**: Reads the key-value pair from .env file and adds them to environment variable.
- **vertexai**: A Python client library for interacting with the Vertex AI API.


## 📚 Links-and-References
- [Google Vertex AI Documentation](https://cloud.google.com/python/docs/reference/aiplatform/latest)
- [LangChain Integration with Vertex AI](https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm)
- [Vertex AI SDK for Python](https://cloud.google.com/vertex-ai/docs/python-sdk/use-vertex-ai-python-sdk)


## Versioning

**Version 1.3** includes these features:

- *AI-powered code generation and completion*
- *Uses OpenAI and Vertex AI models*
- *Save, execute code, and select coding guidelines*
- *Advanced code editor features*
- *Customizable Vertex AI settings*
- *Offline and online compilation modes*
- *Coding guidelines*: 
  - *Modularity*
  - *Exception handling*
  - *Error handling*
  - *Logging*
  - *Comments*
  - *Efficiency*
  - *Robustness*
  - *Memory management*
  - *Speed optimization*
  - *Naming conventions*

**New in version 1.3:** AI-powered code generation and completion using OpenAI and Vertex AI models.

## ✍️ Author
Crafted with ❤️ by HeavenHM.