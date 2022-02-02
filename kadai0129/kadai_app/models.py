import os

from django.db import models

from accounts.models import CustomUser

from django.core.validators import FileExtensionValidator

import sox

class Play(models.Model):
    """投稿した曲モデル"""
    name = 'song'
    TAG = (
        ('A', 'Japan'),
        ('B', 'America'),
        ('C', 'China'),
    )


    user = models.ForeignKey(CustomUser, verbose_name = 'ユーザー', on_delete = models.PROTECT)
    title = models.CharField(verbose_name = 'タイトル', max_length = 40, default = name)
    attach1 = models.FileField(verbose_name='添付ファイル', default = 'audio0.mp3')
    about_song = models.TextField(verbose_name = '説明', max_length = 400, default = name)
    tag = models.CharField(verbose_name = 'タグ', max_length = 10, default = name,blank=True, null=True)
    music_photo = models.ImageField(verbose_name='ジャケット写真', upload_to='images', blank=True, null=True)
    picth_num = models.IntegerField(default = 0)
    iine_num = models.IntegerField(default = 0, verbose_name='いいね')
    loaded_num = models.IntegerField(default=0, verbose_name='再生数')

    parent_play = models.IntegerField(verbose_name='編集元楽曲キー', default=0)

    created_at = models.DateTimeField(verbose_name = '作成日時', auto_now_add = True)
    update_at = models.DateTimeField(verbose_name = '更新日時', auto_now = True)

    class Meta:
        verbose_name_plural = 'Play'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "title"],
                name="play_unique"
            ),
        ]

    def __str__(self):
        return self.title

class Grouper(models.Model):
    """プレイリスト作成モデル"""
    name = 'playlist'
    user = models.ForeignKey(CustomUser, verbose_name = 'ユーザー', on_delete = models.PROTECT)
    title = models.CharField(verbose_name = 'タイトル', max_length = 40, default = name, unique=True,)
    tag = models.CharField(verbose_name = 'タグ', max_length = 10, default = name,blank=True, null=True)
    music_photo = models.ImageField(verbose_name='ジャケット写真', upload_to='images', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name = '作成日時', auto_now_add = True)
    update_at = models.DateTimeField(verbose_name = '更新日時', auto_now = True)

    class Meta:
        verbose_name_plural = 'Grouper'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "title"],
                name="group_unique"
            ),
        ]
    def __str__(self):
        return self.title

class Grouped(models.Model):
    """曲追加モデル"""

    name = 's'
    user = models.ForeignKey(CustomUser, verbose_name = 'ユーザー', on_delete = models.PROTECT)
    group = models.ForeignKey(Grouper, on_delete=models.CASCADE)
    upload_music = models.ForeignKey(Play, related_name='music',verbose_name = '投稿した曲', on_delete = models.CASCADE, blank=True, null=True)
    douwload_music = models.FileField(verbose_name='ダウンロードした曲', upload_to='upmusic', validators=[FileExtensionValidator(['wav', 'mp3', 'alf',])], blank=True, null=True)
    priority = models.IntegerField(verbose_name='優先度', default=0)
    created_at = models.DateTimeField(verbose_name = '作成日時', auto_now_add = True)
    update_at = models.DateTimeField(verbose_name = '更新日時', auto_now = True)

    class Meta:
        verbose_name_plural = 'Grouped'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "group", "upload_music"],
                name="grouped_unique"
            ),
        ]
    def __str__(self):
        return str(self.group)

class Comment(models.Model):
    """記事に紐づくコメント"""

    text = models.TextField('')
    target = models.ForeignKey(Play, on_delete=models.CASCADE, verbose_name='対象楽曲')

class Likes(models.Model):
    """いいねモデル"""
    player = models.ForeignKey(Play, on_delete=models.CASCADE, verbose_name='対象楽曲')
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name='いいねしたユーザー')

    class Meta:
        verbose_name_plural = 'Likes'
    
    def __str__(self):
        return self.player

class Follow(models.Model):
    """フォロー機能"""
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name='フォロワー')

    followuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
    verbose_name='フォロー', related_name='followuser')

    class Meta:
        verbose_name_plural = 'Follow'
    
    def __str__(self):
        return str(self.followuser)

class Userlog(models.Model):
    """ユーザー登録後の追加情報（自己紹介等）"""
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name='基本情報')

    intro = models.CharField(verbose_name='自己紹介', max_length=200, default='こんにちは！')#*

    GENRE = (
        ('A', 'Japan'),
        ('B', 'America'),
        ('C', 'China'),
    )

    GOOD_INS = (
        ('D', 'Dapan'),
        ('E', 'Emerica'),
        ('F', 'Fhina'),
    )

    genre = models.CharField(verbose_name='好きな音楽ジャンル', choices = GENRE, max_length=20)

    avatar_photo = models.ImageField(verbose_name='アバター写真', upload_to='images', blank=True, null=True)

    good_instrument = models.CharField(verbose_name='得意な楽器', choices=GOOD_INS, max_length=20)

    class Meta:
        verbose_name_plural = 'Userlog'
    
    def __str__(self):
        return str(self.intro)

class Playfollower(models.Model):
    """派生した楽曲を格納するモデル"""
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name='フォロワー')

    current_play = models.ForeignKey(Play, on_delete=models.CASCADE,
    verbose_name='親', related_name='current_play')

    child_play = models.ForeignKey(Play, on_delete=models.CASCADE, verbose_name='子', related_name='child_play')

    class Meta:
        verbose_name_plural = 'Playfollower'
    
    def __str__(self):
        return str(self.child_play)