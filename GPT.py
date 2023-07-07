import openai
import prompt_toolkit

# Set up OpenAI API key
openai.api_key = "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"

# Define function to generate response from GPT-3
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=40,
        temperature=0.5
    )
    return response['choices'][0]['message']['content']


# Define function to handle user input and generate response
def chat(user_input=None, prompt = {"role": "system", "content": "You are a friendly person."}):
    if not user_input:
        user_input = prompt_toolkit.prompt("> ")
    # user_input = input('>')
    prompt=prompt
    response = generate_response(prompt)
    # print(response)
    user_input = None

    return response

if __name__ == '__main__':
    # Call chat function to start the conversation
    msg = 'i am not happy.'
    print(chat())

    
