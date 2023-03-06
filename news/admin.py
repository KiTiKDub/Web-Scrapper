from django.contrib import admin
from .models import User, Query, Article

# Register your models here.
admin.site.register(User)
admin.site.register(Query)
admin.site.register(Article)