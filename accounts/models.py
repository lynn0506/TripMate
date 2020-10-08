from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator 

from multiselectfield import MultiSelectField
from faker import Faker
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_OPTION = (('Female', '여'), ('Male', '남'))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    follows = models.ManyToManyField('self', through = 'Follow', blank=True, related_name = 'follow', symmetrical=False)
    nickname = models.CharField(max_length=15, verbose_name='이름')
    age = models.IntegerField(null=True, blank=True, verbose_name='나이')
    gender = MultiSelectField(choices=GENDER_OPTION)
    photo = models.TextField(blank=True)
    location = models.CharField(max_length=50, verbose_name='위치')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):  
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):  
        instance.profile.save()

    def __str__(self):
        return f'user={self.user}, name={self.name}, age={self.age}, gender={self.gender}, nickname={self.nickname}, location={self.location}, photo={self.photo}'


class ChatRoom(models.Model):
    place = models.CharField(max_length=10, verbose_name='채팅방')
    trip_id = models.IntegerField(null=True, blank=True)
    chat_members = models.ManyToManyField(User, blank=True, related_name="chatroom", through="ChatMember")
    chat_users = models.ManyToManyField('self', blank=True, related_name='chatroom', through='ChatMember', symmetrical=False)
    updated_at = models.DateTimeField(default=timezone.now)

# followers
class Follow(models.Model): 
    follow_to = models.ForeignKey(Profile, related_name = 'follow_from', on_delete=models.CASCADE)
    follow_from = models.ForeignKey(Profile, related_name = 'follow_to', on_delete=models.CASCADE)
    followers = models.ManyToManyField('self', through = 'Follow', blank=True, \
                                        related_name = 'follow', symmetrical=False)
    place = models.CharField(max_length=10,  verbose_name='장소')
    deny = models.BooleanField(null=True, blank=True)
   
    def __str__(self):
        return '{} follows {}'.format(self.follow_from, self.follow_to)

class ChatMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chatmember')
    notice = models.IntegerField(default=0, verbose_name='채팅수')

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_from')
    content = models.CharField(max_length=300)
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
