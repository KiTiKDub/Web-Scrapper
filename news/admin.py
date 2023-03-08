from django.contrib import admin
from .models import User, Query, Article, Likes, Dislikes

# Register your models here.
admin.site.register(User)
admin.site.register(Query)
admin.site.register(Article)
admin.site.register(Likes)
admin.site.register(Dislikes)