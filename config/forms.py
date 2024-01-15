from django import forms
import openai

class ChatForm(forms.Form):
    user_input = forms.CharField(
        max_length=300, 
        widget=forms.Textarea(
            attrs={
            'rows': 3,
            'cols': 80,
            'style': 'resize:none;'
            }
        )
    )

