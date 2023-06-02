from django import forms

class ChatMessageForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your message...'}))
