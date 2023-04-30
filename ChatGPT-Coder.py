import os
import openai
import subprocess
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define method to remove any special characters from the generated code
def remove_special_characters(language, code):
    if code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    
    if language == "Python":
        code = code.replace(">>>", "")
        code = code.replace("...", "")
        code = code.replace("python", "")
        
    if language == "C" or language == "C++":
        code = code.replace("$", "")
        code = code.replace("gcc", "")
        code = code.replace("g++", "")
        code = code.replace("./", "")

    if language == "Javascript":
        code = code.replace(">", "")
        
    
    return code

def run_code(language, code):
    
    # Remove any special characters from the generated code.
    code = remove_special_characters(language, code)
    
    if language == "Python":
        with open("temp_code.py", "w") as f:
            f.write(code)

        output = subprocess.run(["python", "temp_code.py"], capture_output=True, text=True)
        return output.stdout + output.stderr

    elif language == "C" or language == "C++":
        ext = ".c" if language == "C" else ".cpp"
        with open("temp_code" + ext, "w") as f:
            f.write(code)

        compile_output = subprocess.run(["gcc" if language == "C" else "g++", "-o", "temp_executable", "temp_code" + ext], capture_output=True, text=True)
        if compile_output.returncode != 0:
            return compile_output.stderr

        run_output = subprocess.run(["./temp_executable"], capture_output=True, text=True)
        return run_output.stdout + run_output.stderr

    elif language == "Javascript":
        with open("temp_code.js", "w") as f:
            f.write(code)

        output = subprocess.run(["node", "temp_code.js"], capture_output=True, text=True)
        return output.stdout + output.stderr

    else:
        return "Unsupported language."


languages = ["C", "C++", "Python", "Javascript"]
print("Select a programming language: ")
for i, lang in enumerate(languages):
    print(f"{i + 1}. {lang}")

lang_choice = int(input("Enter the number corresponding to your choice: ")) - 1
language = languages[lang_choice]
prompt = input("Enter a prompt: ")

chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"Write a {language} code full source code including main method for the following prompt: {prompt}."},
        {"role": "system", "content": "Generate code in raw text format only. Your response should consist of only code and nothing else. Please do not provide any explanations or descriptions of the code," \
         "and avoid using any special characters or formatting that might interfere with copying and pasting the code into a programming environment." \
         "Your code should be complete and functional, and should accomplish the task specified in the prompt." \
         ".And if there is input required dont ask user from input just use some random input."},
        {"role": "user", "content": prompt},
    ],
    max_tokens=2000,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

generated_code = chat_completion.choices[0].message.content.strip()
#print(f"\nGenerated code in {language} is code {generated_code}")

print("\nRunning the generated code...\n")
output = run_code(language, generated_code)
print("Output:", output)
