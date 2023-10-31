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
import pyocr
from django import forms

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



class ImageUploadForm(forms.Form):
    image = forms.ImageField()


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
    



def ocr_view(request):
    # Tesseractのパスを設定
    pyocr.tesseract.TESSERACT_CMD = settings.TESSERACT_CMD
    text = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # アップロードされた画像を取得
            uploaded_image = form.cleaned_data['image']

            # 利用可能なOCRツールを取得
            tools = pyocr.get_available_tools()
            if len(tools) == 0:
                text = "OCRツールが見つかりませんでした"
            else:
                tool = tools[0] # 最初のOCRツールを使用
                image = Image.open(uploaded_image)      # 画像からテキストを抽出
                text = tool.image_to_string(image, lang="jpn")                
                text = text.replace(' ', '') # 不要なスペースを削除
    else:
        form = ImageUploadForm()

    # OCRの結果をテンプレートに渡す
    return render(request, 'gptapp/ocr.html', {'form': form, 'text': text})