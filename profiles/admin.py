from django.contrib import admin
from .models import Post, FightRecord

# Register your models here.
admin.site.register(Post)
admin.site.register(FightRecord)