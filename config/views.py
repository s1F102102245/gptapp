from django.shortcuts import render
from .forms import ChatForm
import openai

openai.api_key = '8uHzWMhnMx70i0CwZLrfGuG9urGKr8F7fGBDCtfX0FqRx6cPjbOzGS1XrldNZ0Djv95KB0uZ7WrNQrOwcaR9jVQ'

def chat_with_gpt3(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def chat_view(request):
    chat_response = ""
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            chat_response = chat_with_gpt3(user_input)
    else:
        form = ChatForm()

    return render(request, 'gptapp/chat_template.html', {'form': form, 'chat_response': chat_response})
