from django.contrib import admin
from .models import Post, Setting, UserProfile, Blocked

# Register your models here.
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Setting)
admin.site.register(Blocked)