from django import forms

class ChatForm(forms.Form):
    user_input = forms.CharField(
        label='',
        max_length=300, 
        required=False,
        widget=forms.Textarea(
            attrs={
            'rows': 15,
            'cols': 30,
            'style': 'resize:none; border:none; outline: none;',
            'class': 'forms-py-class',
            }
        )
    )

class ImageUploadForm(forms.Form):
    image = forms.ImageField(required=False,label='',)