from django import forms


class ProcessOrderForm(forms.Form):
    feedback_message = forms.CharField(label='反馈消息', widget=forms.Textarea)