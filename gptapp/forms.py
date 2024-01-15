from django import forms

class ChatForm(forms.Form):
    user_input = forms.CharField(label='', max_length=300, widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
