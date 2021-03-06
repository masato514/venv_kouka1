# Generated by Django 2.2.2 on 2022-02-01 21:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='song', max_length=40, verbose_name='タイトル')),
                ('attach1', models.FileField(default='audio0.mp3', upload_to='', verbose_name='添付ファイル')),
                ('about_song', models.TextField(default='song', max_length=400, verbose_name='説明')),
                ('tag', models.CharField(blank=True, default='song', max_length=10, null=True, verbose_name='タグ')),
                ('music_photo', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='ジャケット写真')),
                ('picth_num', models.IntegerField(default=0)),
                ('iine_num', models.IntegerField(default=0, verbose_name='いいね')),
                ('loaded_num', models.IntegerField(default=0, verbose_name='再生数')),
                ('parent_play', models.IntegerField(default=0, verbose_name='編集元楽曲キー')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name_plural': 'Play',
            },
        ),
        migrations.CreateModel(
            name='Userlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', models.CharField(default='こんにちは！', max_length=200, verbose_name='自己紹介')),
                ('genre', models.CharField(choices=[('A', 'Japan'), ('B', 'America'), ('C', 'China')], max_length=20, verbose_name='好きな音楽ジャンル')),
                ('avatar_photo', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='アバター写真')),
                ('good_instrument', models.CharField(choices=[('D', 'Dapan'), ('E', 'Emerica'), ('F', 'Fhina')], max_length=20, verbose_name='得意な楽器')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='基本情報')),
            ],
            options={
                'verbose_name_plural': 'Userlog',
            },
        ),
        migrations.CreateModel(
            name='Playfollower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_play', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_play', to='kadai_app.Play', verbose_name='子')),
                ('current_play', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_play', to='kadai_app.Play', verbose_name='親')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='フォロワー')),
            ],
            options={
                'verbose_name_plural': 'Playfollower',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kadai_app.Play', verbose_name='対象楽曲')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='いいねしたユーザー')),
            ],
            options={
                'verbose_name_plural': 'Likes',
            },
        ),
        migrations.CreateModel(
            name='Grouper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='playlist', max_length=40, unique=True, verbose_name='タイトル')),
                ('tag', models.CharField(blank=True, default='playlist', max_length=10, null=True, verbose_name='タグ')),
                ('music_photo', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='ジャケット写真')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name_plural': 'Grouper',
            },
        ),
        migrations.CreateModel(
            name='Grouped',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('douwload_music', models.FileField(blank=True, null=True, upload_to='upmusic', validators=[django.core.validators.FileExtensionValidator(['wav', 'mp3', 'alf'])], verbose_name='ダウンロードした曲')),
                ('priority', models.IntegerField(default=0, verbose_name='優先度')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kadai_app.Grouper')),
                ('upload_music', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='music', to='kadai_app.Play', verbose_name='投稿した曲')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
            options={
                'verbose_name_plural': 'Grouped',
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followuser', to=settings.AUTH_USER_MODEL, verbose_name='フォロー')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='フォロワー')),
            ],
            options={
                'verbose_name_plural': 'Follow',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kadai_app.Play', verbose_name='対象楽曲')),
            ],
        ),
        migrations.AddConstraint(
            model_name='play',
            constraint=models.UniqueConstraint(fields=('user', 'title'), name='play_unique'),
        ),
        migrations.AddConstraint(
            model_name='grouper',
            constraint=models.UniqueConstraint(fields=('user', 'title'), name='group_unique'),
        ),
        migrations.AddConstraint(
            model_name='grouped',
            constraint=models.UniqueConstraint(fields=('user', 'group', 'upload_music'), name='grouped_unique'),
        ),
    ]
