from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import openai
import os
from django.conf import settings
import logging

from PIL import Image
import pyocr
from django import forms
from .forms import ChatForm, ImageUploadForm

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


##
def index(request):
    return render(request, 'gptapp/chat_template.html')
##


# openai.api_key = 'YyJx5cO36OlfXnnGP0GmGGHNArOKEllFISeit5mRE3d0Fq9vxqtiOW9jnN9VKn8UWIMMYUxXmOdnX7X3uMFLqnA'

openai.api_key = settings.OPENAI_API_KEY
openai.api_base = 'https://api.openai.iniad.org/api/v1'


logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY
openai.api_base = 'https://api.openai.iniad.org/api/v1'


def chat_viewORI(request):
    chat_response = ""
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            chat_response = chat_with_gpt3(user_input)
    else:
        form = ChatForm()

    return render(request, 'gptapp/chat_template.html', {'form': form, 'chat_response': chat_response})

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
    return render(request, 'gptapp/chat_template.html', {'form': form, 'text': text})


def chat_view(request):
    #pyocrライブラリでTesseract OCRを使用するためのコマンドパスを設定ファイルから`settings.TESSERACT_CMD`に設定
    pyocr.tesseract.TESSERACT_CMD = settings.TESSERACT_CMD

    #出力を保持するための変数を初期化
    chat_response = ""
    #OCR処理によって取得したテキスト
    ocr_text = None


    #類似質問を格納する変数
    simular_q = ""
    #類似質問の回答を格納する変数
    simular_a = ""

    #POSTリクエストを処理するために使用される2つのフォームを初期化
    #`prefix`パラメータは、フォームがPOSTデータのどの部分を使用するかを区別するために設定
    chat_form = ChatForm(request.POST or None, prefix='chat')
    ocr_form = ImageUploadForm(request.POST or None, request.FILES or None, prefix='upload')


    #ユーザーがチャットボタンをクリックした場合の処理
    #もしチャットフォームが有効なデータを含んでいる場合、`chat_with_gpt3`関数を呼び出してユーザー入力に対する応答を取得し、それを`chat_response`に格納
    #また、OCR結果である`ocr_text`をPOSTデータから取得
    if 'chat_button' in request.POST:
        if chat_form.is_valid():
            user_input = chat_form.cleaned_data['user_input']
            chat_response = chat_with_gpt3(user_input)
        # フォームが送信された場合でもOCRフォームの情報を保持
        ocr_text = request.POST.get('ocr_text', None)


    #ユーザーが画像アップロードボタンをクリックした場合の処理
    if 'upload_button' in request.POST:
        if ocr_form.is_valid():
            uploaded_image1 = ocr_form.cleaned_data['image']
            tools = pyocr.get_available_tools()
            if len(tools) == 0:
                ocr_text = "OCRツールが見つかりませんでした"
            else:
                tool = tools[0]
                image = Image.open(uploaded_image1)
                ocr_text = tool.image_to_string(image, lang="jpn")
                ocr_text = ocr_text.replace(' ', '')

        # フォームが送信された場合でもチャットフォームの情報を保持
        user_input = request.POST.get('user_input', None)

        #交信
        chat_response = chat_with_gpt3(user_input)

    #Djangoの`render`関数を使用して、チャットとOCRフォーム、チャット応答、OCRテキストを含むコンテキストを`chat_template.html`テンプレートファイルに渡し、生成されたHTMLをクライアントに渡す
    return render(request, 'gptapp/chat_template.html', {'chat_form': chat_form, 'chat_response': chat_response, 'ocr_form': ocr_form, 'ocr_text': ocr_text})


#prompt_text : この引数にはユーザーからの入力やプロンプトが渡され、GPT-3に対する質問やステートメントとして機能します。
def chat_with_gpt3(prompt_text):
    #try-except構文。例外処理ともいう。tryで例外が発生するかもしれないが、実行したい処理。except エラー名：で例外発生時に行う処理をかく
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are teacher who only knows mathematics, you answer non-mathematics questions with 「数学のことしかわからないワンねぇ... and you always respond in Japanese. Do not use honorifics and add 'ワン' at the end of the word."},
                {"role": "user", "content": f"{prompt_text}"}
            ]
        )
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        return str(e)

def make_simular_with_gpt3(prompt_text):
    try:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are teacher who only knows mathematics, you only create similar problems and their answers, answer non-mathematics question with '数学の問題しか作れないワン...'.  and you always respond in Japanese. Do not use honorifics and add 'ワン' at the end of the word."},
                {"role": "user", "content": f"{prompt_text}"}
            ]
        )
        return response['choices'][0]['message']['content']

    except Exception as e:
        return str(e)

'''
def chat_with_gpt3(prompt_text, generate_similar=False):
    try:
        messages = [
                {"role": "system", "content": "You are a helpful assistant and you always respond in Japanese."},
                {"role": "user", "content": f"{prompt_text}"}
        ]
        
        if generate_similar:
            messages.append({"role": "system", "content": "Please generate a similar math problem and provide the answer."})
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        
        content = response['choices'][0]['message']['content']
        simular_q = None
        simular_a = None
        
        # If requested to generate similar problem, parse response for problem and answer
        if generate_similar:
            parts = content.split('Similar Question:')  # Assuming GPT-3 marks the similar question with this text
            if len(parts) > 1:
                simular_q = parts[1].split('Answer:')[0].strip()  # Extracting the similar question
                simular_a = parts[1].split('Answer:')[1].strip()  # Extracting the answer
        
        return content, simular_q, simular_a
    except Exception as e:
        return str(e), None, None

# You would call this function like this when you want to generate a new problem along with the answer:
# chat_response, simular_q, simular_a = chat_with_gpt3(user_input, generate_similar=True)
'''

def math_Answerer(request):
    #pyocrライブラリでTesseract OCRを使用するためのコマンドパスを設定ファイルから`settings.TESSERACT_CMD`に設定
    pyocr.tesseract.TESSERACT_CMD = settings.TESSERACT_CMD

    #出力を保持するための変数を初期化
    chat_response = ""
    #OCR処理によって取得したテキスト
    ocr_text = None

    simular_question = "" 

    #POSTリクエストを処理するために使用される2つのフォームを初期化
    #`prefix`パラメータは、フォームがPOSTデータのどの部分を使用するかを区別するために設定
    chat_form = ChatForm(request.POST or None, prefix='chat')
    ocr_form = ImageUploadForm(request.POST or None, request.FILES or None, prefix='upload')

    #ユーザーがチャットボタンをクリックした場合の処理
    #もしチャットフォームが有効なデータを含んでいる場合、`chat_with_gpt3`関数を呼び出してユーザー入力に対する応答を取得し、それを`chat_response`に格納
    #また、OCR結果である`ocr_text`をPOSTデータから取得
    if 'chat_button' in request.POST:
        if chat_form.is_valid():
            user_input = chat_form.cleaned_data.get('user_input')
            if user_input:  # user_inputが空でなければTrue
                chat_response = chat_with_gpt3(user_input)
                simular_question = make_simular_with_gpt3(user_input)
            else:
                # ユーザー入力が空の場合の処理
                return  # 例えばここで処理を終了したり、適切なメッセージと共にリダイレクトしたり、エラーメッセージを表示する

        # フォームが送信された場合でもOCRフォームの情報を保持
        ocr_text = request.POST.get('ocr_text', None)


    #ユーザーが画像アップロードボタンをクリックした場合の処理
    if 'upload_button' in request.POST:
        if ocr_form.is_valid():
            uploaded_image1 = ocr_form.cleaned_data['image']
            tools = pyocr.get_available_tools()
            if len(tools) == 0:
                ocr_text = "OCRツールが見つかりませんでした"
            else:
                tool = tools[0]
                image = Image.open(uploaded_image1)
                ocr_text = tool.image_to_string(image, lang="jpn")
                ocr_text = ocr_text.replace(' ', '')

                # OCRで取得したテキストをChatGPTに送る
                chat_response = chat_with_gpt3(ocr_text)
                simular_question = make_simular_with_gpt3(user_input)

        # フォームが送信された場合でもチャットフォームの情報を保持
        #user_input = request.POST.get('user_input', None)
        #chat_response = chat_with_gpt3(user_input)

    #Djangoの`render`関数を使用して、チャットとOCRフォーム、チャット応答、OCRテキストを含むコンテキストを`chat_template.html`テンプレートファイルに渡し、生成されたHTMLをクライアントに渡す
    return render(request, 'gptapp/math_index.html', {'chat_form': chat_form, 'chat_response': chat_response, 'simular_question':simular_question,'ocr_form': ocr_form, 'ocr_text': ocr_text})
