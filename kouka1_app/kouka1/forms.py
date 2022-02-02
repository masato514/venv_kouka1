from django import forms


class Kouka1Form(forms.Form):
    name = forms.CharField(label='名前', max_length=30)
    age = forms.IntegerField(label='年齢')
    tell = forms.CharField(label='電話番号', max_length=100)
    email = forms.EmailField(label='メール')
    live = forms.CharField(label='住所', max_length=11)    

    