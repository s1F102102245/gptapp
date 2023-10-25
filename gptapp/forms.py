from django import forms

class OCRForm(forms.Form):
    image = forms.ImageField(label='画像ファイル')