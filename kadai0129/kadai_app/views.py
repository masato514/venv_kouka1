from django.shortcuts import render

from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import InquiryForm, PlayCreateForm, GroupCreateForm, GroupMusicCreateForm, CommentCreateForm, IineCreateForm, GroupMusicCreate2Form, FollowCreateForm, UserlogForm, PlayRemakeForm


from django.urls import reverse_lazy

from .models import Play, Grouper, Grouped, Comment, Likes, Follow, Userlog, Playfollower
from accounts.models import CustomUser

from django.contrib import messages

import logging

import sox

import shutil
import os

from django.db.models import Q
from functools import reduce
from operator import and_
from django.shortcuts import redirect, get_object_or_404

logger = logging.getLogger(__name__)

class UnloginView(generic.TemplateView):
    template_name = 'index2.html'

class IndexView(LoginRequiredMixin, generic.CreateView):
    model = Userlog
    form_class = UserlogForm
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        login_num = CustomUser.objects.get(username=self.request.user)
        login_num.loginnum += 1
        login_num.save()

        query = Userlog.objects.filter(user= self.request.user)

        ctx = super().get_context_data(**kwargs)
        if (query.count() == 0):
            ctx['userloginfo'] = False
        else:
            ctx['userloginfo'] = query.get()
        
        ctx['login_num'] = login_num.loginnum
        return ctx
    
    def form_valid(self, form):
        kadai_app = form.save(commit = False)
        kadai_app.user = self.request.user
        kadai_app.save()
        return redirect('kadai_app:index')

    def form_invalid(self, form):
        messages.error(self.request, "ユーザー登録に失敗しました。")
        return super().form_invalid(form)

class InquiryView(generic.FormView):
    """ お問い合わせページ """
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('kadai_app:inquiry')
    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class PlayListView(LoginRequiredMixin, generic.ListView):
    """ 投稿した曲一覧 """
    model = Play
    template_name = 'mypage.html'
    paginate_by = 2

    def get_queryset(self):
        plays = Play.objects.order_by('-created_at')
        return plays

class PlayDetailView(generic.DetailView):
    """ 再生画面 """
    model = Play
    template_name = 'play_detail.html'

    def get_context_data(self, **kwargs):
        loadednum = Play.objects.get(pk = self.kwargs.get('pk'))
        print(loadednum)
        loadednum.loaded_num += 1
        loadednum.save()
        print(loadednum.loaded_num)

        nowplay = Play.objects.get(pk = self.kwargs.get('pk'))
        fuser_pks = CustomUser.objects.get(id=nowplay.user.pk).pk

        que = Playfollower.objects.filter(current_play=loadednum, user=self.request.user )
        query = Follow.objects.filter(user=self.request.user, followuser__pk=fuser_pks)
        context = super().get_context_data(**kwargs)

        if (loadednum.parent_play != 0):
            parent_name_ob = Play.objects.get(pk=loadednum.parent_play)
            context['parent_name_ob'] = parent_name_ob
        else:
            pass

        if (que.count() > 0):
            context['child_name_ob'] = que
        else:
            pass

        
        if(query.count() ==0):
            context['flg'] = True
        else:
            context['flg'] = False
        context['loadnum'] = loadednum.loaded_num
        # テンプレートにコメント作成フォームを渡す
        context['comment_form'] = CommentCreateForm
        context['iine_num'] = Likes.objects.filter(player__pk= self.kwargs.get('pk')).count()
        # context['f_user'] = CustomUser.objects.get(id = self.kwargs.get('pk'))
        return context

class PlayCreateView(LoginRequiredMixin, generic.CreateView):
    """ 楽曲投稿画面 """
    model = Play
    template_name = 'play_create.html'
    form_class = PlayCreateForm
    success_url = reverse_lazy('kadai_app:mypage')


    def form_valid(self, form):
        kadai_app = form.save(commit = False)
        kadai_app.user = self.request.user
        kadai_app.save()
        FILE_PATH_NAME = kadai_app.attach1.file.name

        num = 0
        while os.path.exists('.\\media\\picth' + str(num) + '.wav'):
          num += 1
          
        IN_WAVE_FILE = FILE_PATH_NAME    # 入力音声
        OUT_WAVE_FILE = 'picth' + str(num) + '.wav'   # ピッチシフト済み音声
        # create trasnformer (単一ファイルに対する処理)
        transformer = sox.Transformer()

        # ピッチシフト の パラメタ
        # 単位：セミトーン（いわゆる半音 -> 1半音の変化は周波数的には約1.06倍）
        # 正値は上げる、負値は下げる
        # 実際にはfloat値を指定可能
        PITCHSHIFT = kadai_app.picth_num# 半音上げる

        # ピッチシフトをかける
        transformer.pitch(n_semitones=PITCHSHIFT)  # 上げる
        transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE)
        
        shutil.move('.\\picth' + str(num) + '.wav', '.\\media\\picth' + str(num) + '.wav')

        kadai_app.attach1 = OUT_WAVE_FILE
        
        kadai_app.save()
        messages.success(self.request, 'リストを作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "リストの作成に失敗しました。")
        return super().form_invalid(form)

class PlayUpdateView(LoginRequiredMixin, generic.UpdateView):
    """ 投稿した曲の編集画面 """
    model = Play
    template_name = 'play_update.html'
    form_class = PlayCreateForm

    def get_success_url(self):
        return reverse_lazy('kadai_app:play_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'リストを更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "リストの更新に失敗しました。")
        return super().form_invalid(form)

class PlayDeleteView(LoginRequiredMixin, generic.DeleteView):
    """ 投稿した曲の削除画面 """
    model = Play
    template_name = 'play_delete.html'
    success_url = reverse_lazy('kadai_app:mypage')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "リストを削除しました。")
        return super().delete(request, *args, **kwargs)

class GroupListView(LoginRequiredMixin, generic.ListView):
    """ プレイリストの一覧 """
    model = Grouped
    template_name = 'mypage.html'
    paginate_by = 5
    context_object_name = "grouper_list"

    def get_queryset(self): #ユーザーごとの投稿曲表示
        groups = Grouper.objects.filter(user = self.request.user).order_by('-created_at')
        return groups
    
class GroupCreateView(LoginRequiredMixin, generic.CreateView):
    """ プレイリスト作成フォーム """
    model = Grouper
    template_name = 'group_create.html'
    form_class = GroupCreateForm
    success_url = reverse_lazy('kadai_app:mypage')


    def form_valid(self, form):
        kadai_app = form.save(commit = False)
        kadai_app.user = self.request.user
        kadai_app.save()
        messages.success(self.request, 'リストを作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "リストの作成に失敗しました。")
        return super().form_invalid(form)

class GroupDetailView(LoginRequiredMixin,generic.ListView):
    """ プレイリスト詳細画面 """
    model = Grouped
    template_name = 'group_detail.html'

    # def get_queryset(self):
    #     return Grouped.objects.filter(group__title=self.kwargs.get('group'))
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['grouped_l'] = Grouped.objects.filter(group__title=self.kwargs.get('group')).filter(user=self.request.user)
        ctx['group'] = Grouper.objects.get(title__contains=self.kwargs.get('group'), user=self.request.user)
        return ctx

class GroupMusicCreateView(LoginRequiredMixin, generic.CreateView):
    """ プレイリスト編集画面 """
    model = Grouper, Play
    template_name = 'group_music_create.html'
    form_class = GroupMusicCreateForm
    success_url = reverse_lazy('kadai_app:group_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['play_m_l'] = Play.objects.all()
        ctx['groups'] = Grouper.objects.filter(user=self.request.user)
        return ctx

    def form_valid(self, form):
        catch_group_title = self.request.POST.get('m_gr')
        for_music_num = int(self.request.POST.get('ex_counter'))

        # 入力されたプレイリスト名がGrouperモデル内にないと新規作成する
        query = Grouper.objects.filter(title = catch_group_title).filter(user = self.request.user)
        if (query.count() == 0 ):
            catch_music_photo = self.request.FILES['filefield']
            Grouper.objects.create(user=self.request.user, title=catch_group_title, music_photo=catch_music_photo)
        else:
            if ( 'filefield' in self.request.FILES):
                catch_music_photo = self.request.FILES['filefield']
                group_ob = query.get()
                group_ob.music_photo = catch_music_photo
                group_ob.save()
            else:
                pass
        selected_group_object = query.get()

        mygroup_objects = []
        for i in range(1, for_music_num + 1):
            if self.request.POST.get('music' + str(i)) is None:
                pass
            else:
                selected_play_object = Play.objects.get(title = self.request.POST.get('music' + str(i)))
                mygroup_objects.append(Grouped(user=self.request.user, group=selected_group_object, upload_music=selected_play_object))
            
        Grouped.objects.bulk_create(mygroup_objects)

        messages.success(self.request, '音楽をリストに追加しました。')
        return redirect('kadai_app:mypage')

    def form_invalid(self, form):
        messages.error(self.request, "追加に失敗しました。")
        return redirect('kadai_app:mypage')

class SearchpageView(generic.ListView):
    """ 検索画面 """
    template_name = 'searchpage.html'

    def get_queryset(self):
        if self.request.GET.get('q', ''):
            params = self.parse_search_params(self.request.GET['q'])
            query = reduce(
                lambda x,y : x & y,
                list(map(lambda z: Q(title__icontains=z), params))
            )
            # 下記でもOK
            # query = reduce(and_, [Q(title__icontains=p) | Q(message__icontains=p) for p in params])
            return Play.objects.filter(query)
        else:
            return None
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx
        
    def parse_search_params(self, words: str):
        search_words = words.replace('　', ' ').split()
        return search_words

class MyPageView(LoginRequiredMixin, generic.TemplateView):
    """ 投稿した曲、ダウンロードした曲、お気に入りユーザー、プレイリストの一覧 """
    model = Play, Grouper, Grouped, Follow
    template_name = 'mypage.html'
    print()
    def get_context_data(self, **kwargs):
        query = Userlog.objects.filter(user= self.request.user)
        ctx = super().get_context_data(**kwargs)
        if (query.count() == 0):
            ctx['userloginfo'] = False
        else:
            ctx['userloginfo'] = query.get()
        ctx['group'] = Grouper.objects.filter(user = self.request.user)
        ctx['music'] = Play.objects.filter(user = self.request.user)
        ctx['player'] = Grouped.objects.filter(user = self.request.user)
        ctx['following'] = Follow.objects.filter(user = self.request.user) 
        return ctx

class IntroView(generic.TemplateView):
    """ アプリ紹介画面 """
    template_name = 'intro.html'

class PlayView(generic.TemplateView):
    """ 再生画面 """
    model = Play
    template_name = 'play.html' 

    def detail(request, pk):
        """その楽曲の表示"""
        loading = Play.objects.get(id=pk)
        return render(request, 'play.html', {'loading': loading})

class UserpageView(generic.TemplateView):
    template_name = 'userpage.html'  

class PlaylistnameView(generic.TemplateView):
    template_name = 'playlistname.html'

# コメント作成用のview(play_detailに組み込む)
class CommentCreate(generic.CreateView):
    """
    記事へのコメント作成ビュー
    ページは表示されないが、コメントを作成するために使用
    """
    model = Comment
    # model = Comment, Play
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Play, pk=post_pk)

        comment = form.save(commit=False)
        comment.target = post
        comment.save()

        return redirect('kadai_app:play_detail', pk=post_pk)

class IineCreateView(LoginRequiredMixin, generic.CreateView):
    """ いいねビュー """
    model = Likes, Play
    form_class = IineCreateForm
    def form_valid(self, form):
        play_pks =self.kwargs.get('play_pk')
        query = Likes.objects.filter(user = self.request.user).filter(player__pk=play_pks)
        if (query.count() == 0):
            lk = form.save(commit=False)
            lk.player = get_object_or_404(Play, pk=play_pks)
            lk.user = self.request.user
            lk.save()
            return redirect('kadai_app:play_detail', pk=play_pks)
        else:
            query.delete()
            return redirect('kadai_app:play_detail', pk=play_pks)

class GroupCreate2View(LoginRequiredMixin, generic.CreateView):
    """ プレイリスト作成画面（改訂版） """
    model = Grouped
    template_name = 'group_update.html'
    form_class = GroupMusicCreate2Form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['group_name'] = self.kwargs.get('group')
        ctx['grouped_l'] = Grouped.objects.filter(user = self.request.user).filter(group__title= self.kwargs.get('group'))
        ctx['play_m_l'] = Play.objects.all()
        return ctx

    def pry1(self, g_num):
        nyuryoku1 = []
        for j in range(1, g_num +1):
            nyuryoku1.append(self.request.POST.get(str(j)))
        return nyuryoku1

    def pry2(self, g_num):
        pri_num = []
        nyuryoku1 = []
        for j in range(1, g_num + 1):
            nyuryoku1.append(self.request.POST.get(str(j)))
            pri_num.append(self.request.POST.get(str(nyuryoku1[j - 1])))
            print(self.request.POST.get(str(nyuryoku1[j - 1])))
        return pri_num

    def form_valid(self, form):
        g_m = Grouped.objects.filter(user = self.request.user).filter(group__title= self.kwargs.get('group'))
        
        g_num =  g_m.count()
        l_nyuryoku1 = self.pry1(g_num)
        l_pri_num= self.pry2(g_num)
        for i in range(g_num):
            musicob = g_m.get(pk =l_nyuryoku1[i])
            musicob.priority = l_pri_num[i]
            musicob.save()
        
        for_music_num = int(self.request.POST.get('ex_counter'))
        catch_group_title = self.kwargs.get('group')

        selected_group_object = Grouper.objects.get(title = catch_group_title,user = self.request.user)

        for i in range(1, g_num + 1):
            if self.request.POST.get('delnum' + str(i)) is None:
                pass
            else:
                delete_query = Grouped.objects.filter(upload_music__title = self.request.POST.get('delnum' + str(i)))
                delete_query.delete()

        mygroup_objects = []
        for i in range(1, for_music_num + 1):
            if self.request.POST.get('music' + str(i)) is None:
                pass
            else:
                selected_play_object = Play.objects.get(title = self.request.POST.get('music' + str(i)))
                mygroup_objects.append(Grouped(user=self.request.user, group=selected_group_object, upload_music=selected_play_object))
        Grouped.objects.bulk_create(mygroup_objects)

        
        
        return redirect('kadai_app:group_detail', group=self.kwargs.get('group'))

class FollowCreateView(LoginRequiredMixin, generic.CreateView):
    """ お気に入り登録ビュー """
    model = Follow
    form_class = FollowCreateForm

    def form_valid(self, form):
        fuser_pks =self.kwargs.get('fuser_pk')
        query = Follow.objects.filter(user = self.request.user).filter(followuser__pk=fuser_pks)
        if (query.count() == 0):
            lk = form.save(commit=False)
            lk.followuser = get_object_or_404(CustomUser, pk=fuser_pks)
            lk.user = self.request.user
            lk.save()
            messages.success(self.request, 'ユーザーをお気に入りリストに追加しました。')
            return redirect('kadai_app:userpage', pk=fuser_pks)
        else:
            query.delete()
            messages.success(self.request, 'ユーザーをお気に入りリストから削除しました。')
            return redirect('kadai_app:userpage', pk=fuser_pks)

# ログインしていなくても閲覧できるよう「LoginRequiredMixin」を外す
class UserDetailView(generic.DetailView):
    """ ユーザーページ """
    model = CustomUser
    template_name = 'userpage.html'

    def get_context_data(self, **kwargs):
        fuser_pks =self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        # テンプレートにコメント作成フォームを渡す
        # context['comment_form'] = CommentCreateForm
        context['follower_num'] = Follow.objects.filter(followuser__pk= self.kwargs.get('pk')).count()
        context['f_user'] = CustomUser.objects.get(id = self.kwargs.get('pk'))
        context['group'] = Grouper.objects.filter(user__pk = self.kwargs.get('pk'))
        context['music'] = Play.objects.filter(user__pk = self.kwargs.get('pk'))
        
        query = Follow.objects.filter(user = self.request.user).filter(followuser__pk=fuser_pks)
        
        if (query.count() == 0):
            context['flg'] = True
        else:
            context['flg'] = False
        print(context['flg'])
        return context

class UserinfoUpdateView(LoginRequiredMixin, generic.UpdateView):
    """ 新規登録時のユーザー情報の編集画面 """
    model = Userlog
    template_name = 'user_update.html'
    form_class = UserlogForm

    def get_success_url(self):
        return reverse_lazy('kadai_app:mypage')

    def form_valid(self, form):
        messages.success(self.request, 'リストを更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "リストの更新に失敗しました。")
        return super().form_invalid(form)

class PlayRemakeView(LoginRequiredMixin, generic.CreateView):
    """ 楽曲投稿画面 """
    model = Play
    template_name = 'play_remake.html'
    form_class = PlayRemakeForm
    success_url = reverse_lazy('kadai_app:mypage')
        
    # music_photo = self.request.POST.get('music_photo')

    def form_valid(self, form):
        p_play = Play.objects.get(pk = self.kwargs.get('pk'))

        kadai_app = form.save(commit = False)
        kadai_app.user = self.request.user
        kadai_app.parent_play = p_play.pk
        kadai_app.attach1 = p_play.attach1
        kadai_app.save()

        Playfollower.objects.create(user=self.request.user, current_play=p_play, child_play=kadai_app)
        FILE_PATH_NAME = kadai_app.attach1.file.name

        num = 0
        while os.path.exists('.\\media\\picth' + str(num) + '.wav'):
          num += 1
          
        IN_WAVE_FILE = FILE_PATH_NAME    # 入力音声
        OUT_WAVE_FILE = 'picth' + str(num) + '.wav'   # ピッチシフト済み音声
        # create trasnformer (単一ファイルに対する処理)
        transformer = sox.Transformer()

        # ピッチシフト の パラメタ
        # 単位：セミトーン（いわゆる半音 -> 1半音の変化は周波数的には約1.06倍）
        # 正値は上げる、負値は下げる
        # 実際にはfloat値を指定可能
        PITCHSHIFT = kadai_app.picth_num# 半音上げる

        # ピッチシフトをかける
        transformer.pitch(n_semitones=PITCHSHIFT)  # 上げる
        transformer.build(IN_WAVE_FILE, OUT_WAVE_FILE)
        
        shutil.move('.\\picth' + str(num) + '.wav', '.\\media\\picth' + str(num) + '.wav')

        kadai_app.attach1 = OUT_WAVE_FILE
        
        kadai_app.save()
        messages.success(self.request, 'リストを作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "リストの作成に失敗しました。")
        return super().form_invalid(form)