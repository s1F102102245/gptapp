from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import openai
import os
from django.conf import settings
import logging

from .forms import OCRForm
import pytesseract
from PIL import Image


# irequestsmport openai

# openai.api_key = 
# 'YdtsmLm1tUQi2x5uiUlmyISUTJ_ZiP-EOwlmiMOyM0bjz6iun2gUnO6TszHRCb10O_QsmQwLZ-i7kH8h5rJ9Mww'
# openai.api_base = 'https://api.openai.iniad.org/api/v1'
import requests

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



# openai.api_key = 'YyJx5cO36OlfXnnGP0GmGGHNArOKEllFISeit5mRE3d0Fq9vxqtiOW9jnN9VKn8UWIMMYUxXmOdnX7X3uMFLqnA'

openai.api_key = settings.OPENAI_API_KEY
openai.api_base = 'https://api.openai.iniad.org/api/v1'


logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY
openai.api_base = 'https://api.openai.iniad.org/api/v1'

def chat_with_gpt3(prompt_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{prompt_text}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
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



# Tesseractバイナリファイルの相対パス
tesseract_path = os.path.join(settings.BASE_DIR, 'Tesseract-OCR', 'tesseract.exe')

def ocr_view(request):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    text = None

    if request.method == 'POST':
        form = OCRForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            img = Image.open(image)
            text = pytesseract.image_to_string(img)

    else:
        form = OCRForm()

    return render(request, 'gptapp/ocr.html', {'form': form, 'text': text})

