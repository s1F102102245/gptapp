from django.shortcuts import render
from .forms import ChatForm
from django.conf import settings
import openai
import requests
import logging


# openai.api_key = 'YyJx5cO36OlfXnnGP0GmGGHNArOKEllFISeit5mRE3d0Fq9vxqtiOW9jnN9VKn8UWIMMYUxXmOdnX7X3uMFLqnA'

openai.api_key = settings.OPENAI_API_KEY
openai.api_base = 'https://api.openai.iniad.org/api/v1'


logger = logging.getLogger(__name__)

def chat_with_gpt3(prompt_text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt_text,
            max_tokens=150
        )
        logger.info(response)
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(e)
        return str(e)


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

