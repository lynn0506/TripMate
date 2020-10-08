from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(ChatMember)
admin.site.register(ChatRoom)
admin.site.register(Follow)
admin.site.register(Message)

