from libs.palmai_coder import PalmAI


def main():
    prompt = input("Please enter your prompt: ")
    palm_ai = PalmAI(mode="creative")
    result = palm_ai.generate_code(prompt)
    
    if result is not None:
        print(result)
    else:
        print("An error occurred while generating the text.")

if __name__ == "__main__":
    main()