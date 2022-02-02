from django.contrib import admin
from .models import Play, Grouper, Grouped, Comment, Likes, Follow, Userlog,Playfollower

admin.site.register(Play)
admin.site.register(Grouper)
admin.site.register(Grouped)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Follow)
admin.site.register(Userlog)
admin.site.register(Playfollower)