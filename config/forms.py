from django import forms
import openai

class ChatForm(forms.Form):
    user_input = forms.CharField(label='あなたの質問', max_length=300, widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))
