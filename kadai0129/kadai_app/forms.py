from django import forms
from django.core.mail import EmailMessage
from .models import Play, Grouper, Grouped, Comment, Likes, Follow, Userlog

class UserlogForm(forms.ModelForm):
    class Meta:
        model = Userlog
        fields = ('intro', 'genre', 'avatar_photo', 'good_instrument')
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

class InquiryForm(forms.Form):
    name = forms.CharField(label = 'お名前', max_length = 30)
    email = forms.EmailField(label = 'メールアドレス')
    title = forms.CharField(label = 'タイトル', max_length = 30)
    message = forms.CharField(label = 'メールアドレス', widget = forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = ' お名前をここに入力してください'
        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください'
        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください'
        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください'


    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject ='お問い合わせ{}'.format(title)
        message ='送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(name, email, message)
        from_email = 'admin@example.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject =subject, body = message, from_email = from_email, to = to_list, cc = cc_list)
        message.send()

class PlayCreateForm(forms.ModelForm):
    """ 楽曲投稿フォーム """
    class Meta:
        model = Play
        fields = ('title', 'attach1', 'about_song','music_photo','tag','picth_num')
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

class PlayRemakeForm(forms.ModelForm):
    """ remake楽曲投稿フォーム """
    class Meta:
        model = Play
        fields = ('title', 'about_song','music_photo','tag','picth_num')
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

class GroupCreateForm(forms.ModelForm):
    """ プレイリスト作成フォーム """
    class Meta:
        model = Grouper
        fields = ('title', 'music_photo','tag')
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            id = kwargs.get("instance").user.id
            self.fields['title'].queryset = Grouper.objects.filter(user_id=id)
            # for field in self.fields.values():
            #     field.widget.attrs['class'] = 'form-control'

class GroupMusicCreateForm(forms.ModelForm):
    """ 曲追加フォーム """
    class Meta:
        model = Grouped
        fields = ()
        # fields = ('upload_music', 'douwload_music', 'group',)
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            az = self.kwargs.get("instance").user
            self.fields['group'].queryset = Grouper.objects.filter(user=az)

class GroupMusicCreate2Form(forms.ModelForm):
    class Meta:
        model = Grouped
        fields=()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class IineCreateForm(forms.ModelForm):
    class Meta:
        model = Likes
        fields = ()

class FollowCreateForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ()