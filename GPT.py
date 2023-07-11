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
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


# Define function to handle user input and generate response
def chat(user_inputs=None, Prompt = [{"role": "system", "content": "You are a humorous and lovely boy."},
                                     {"role": "system", "content": "You can say at most 2 sentences each time."}]):
    if not user_inputs:
        user_inputs = prompt_toolkit.prompt("> ")
        new = {"role":"user", "content": user_inputs}
        Prompt.append(new)


    for msg in user_inputs:
        Prompt.append({"role":"user", "content": str(msg)})

    response = generate_response(Prompt)
    Prompt.append({"role":"assistant", "content": response})
    
    # 后续使用中维护Prompt的大小
    if len(Prompt)>10:
        del Prompt[1]
        del Prompt[1]

    return response

if __name__ == '__main__':
    # Call chat function to start the conversation
    msg = ['I am not happy.','i am hungry now.']
    print(chat(msg))

    
