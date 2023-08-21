from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

import requests

# import openai

# openai.api_key = 
# 'YdtsmLm1tUQi2x5uiUlmyISUTJ_ZiP-EOwlmiMOyM0bjz6iun2gUnO6TszHRCb10O_QsmQwLZ-i7kH8h5rJ9Mww'
# openai.api_base = 'https://api.openai.iniad.org/api/v1'


# Create your views here.


def root(request):
    return HttpResponse('Hello Django')


def pattern(request, username):
    return HttpResponse('Hello {}'.format(username))

def param(request):
    text = ''
    for key in request.GET:
        text += '{} : {}, '.format(key, request.GET[key])
    return HttpResponse(text)

def index(request):
    return render(request, 'gptapp/index.html')




def chat_with_gpt3(prompt_text):
    endpoint_url = "https://api.openai.iniad.org/api/v1"
    headers = {
        "Authorization": f"YdtsmLm1tUQi2x5uiUlmyISUTJ_ZiP-EOwlmiMOyM0bjz6iun2gUnO6TszHRCb10O_QsmQwLZ-i7kH8h5rJ9Mww",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt_text,
        "max_tokens": 150
    }
    response = requests.post(endpoint_url, headers=headers, json=data)
    response_json = response.json()

    if 'choices' in response_json and len(response_json['choices']) > 0:
        return response_json['choices'][0]['text'].strip()
    else:
        return "Error in getting response."


def chat_view(request):
    response_text = ""
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        response_text = chat_with_gpt3(user_input)

    return render(request, "gptapp/chat_template.html", {"response_text": response_text})



