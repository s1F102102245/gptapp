from django import forms
import openai

class ChatForm(forms.Form):
    user_input = forms.CharField(label='質問はあるワン？', max_length=300, widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))
