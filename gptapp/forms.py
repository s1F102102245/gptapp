from django import forms

class ChatForm(forms.Form):
    user_input = forms.CharField(label='', max_length=300, widget=forms.Textarea(attrs={'rows': 3, 'cols': 80}))


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
