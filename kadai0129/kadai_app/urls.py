from django.urls import path

from . import views

app_name = 'kadai_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name = "index"),
    path('unlogin/', views.UnloginView.as_view(), name = "unlogin"),

    path('inquiry/', views.InquiryView.as_view(), name = "inquiry"),
    
    path('play-list/', views.PlayListView.as_view(), name= "play_list"),
    path('play-detail/<int:pk>/', views.PlayDetailView.as_view(), name = "play_detail"),
    path('play-create/', views.PlayCreateView.as_view(), name = "play_create"),
    path('play-update/<int:pk>/', views.PlayUpdateView.as_view(), name = "play_update"),
    path('play-delete/<int:pk>/', views.PlayDeleteView.as_view(), name = "play_delete"),
    path('group-list/', views.GroupListView.as_view(), name= "group_list"),
    path('group-create/', views.GroupCreateView.as_view(), name ="group_create"),
    path('group-detail/<str:group>/', views.GroupDetailView.as_view(), name = "group_detail"),
    path('group-update/<str:group>/', views.GroupCreate2View.as_view(), name = "group_update"),
    path('group-music-create/', views.GroupMusicCreateView.as_view(), name ="group_music_create"),
    path('searchpage/', views.SearchpageView.as_view(), name = "searchpage"),
    path('mypage/', views.MyPageView.as_view(), name= "mypage"),
    path('intro/', views.IntroView.as_view(), name = "intro"),
    path('play/', views.PlayView.as_view(), name = "play"),
    path('userpage/', views.UserpageView.as_view(), name = "userpage"),
    path('playlistname/', views.PlaylistnameView.as_view(), name= "playlistname"),
    # コメント追加用のhtml（htmlファイル自体はplay_detailに組み込まれる）
    path('comment/create/<int:pk>/', views.CommentCreate.as_view(), name='comment_create'),
    path('likes/form/<int:play_pk>', views.IineCreateView.as_view(), name='likes_form'),
    path('userpage/<int:pk>', views.UserDetailView.as_view(), name ="userpage"),
    path('follow/form/<int:fuser_pk>', views.FollowCreateView.as_view(), name='follow_form'),

    path('user-update/<int:pk>/', views.UserinfoUpdateView.as_view(), name = "user_update"),
    path('play-remake/<int:pk>/', views.PlayRemakeView.as_view(), name = "play_remake"),
]

