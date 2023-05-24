from django import forms


class CreateNewsForm(forms.Form):
    title = forms.CharField(max_length=128, label='Title')
    text = forms.CharField(widget=forms.Textarea, label='Text')


class QueryForm(forms.Form):
    q = forms.CharField(max_length=128, label='Query')
