from django import forms
import openai

class ChatForm(forms.Form):
    user_input = forms.CharField(max_length=300, 
                    
                    widget=forms.Textarea(attrs={
                            'rows': 4,
                            'cols': 50,
                            'style':'resize:none;',}))
