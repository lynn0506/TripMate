from django.db import models
from django.utils import timezone
from django.conf import settings 
from django.contrib.auth.models import User 
from multiselectfield import MultiSelectField 
# from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=10)
    itier_name =  models.CharField(max_length=100)
    itier_lat =  models.CharField(max_length=300)
    itier_long =  models.CharField(max_length=300)
    my_num = models.IntegerField()

    start_date = models.DateTimeField(blank=False, default=timezone.now)
    end_date = models.DateTimeField(blank=False, default=timezone.now)
    bref_info = models.CharField(max_length=100)
    keyword1 = models.CharField(max_length=10)
    keyword2 = models.CharField(max_length=10)
    keyword3 = models.CharField(max_length=10)
    genderChoices = [
        ('M', '남성'),
        ('F', '여성'),
        ('X', '전부'),
    ]#튜플의 첫번째 요소가 저장될 값, 두번째 요소가 사람이 읽을 수 있는 이름
    want_gender = models.CharField(max_length=1, choices=genderChoices,blank=True)
    want_num = models.IntegerField()
    ageChoices = [
        (10, '10대'),
        (20, '20대'),
        (30, '30대'),
        (40, '40대'),
        (50, '50대'),
        (60, '60대 이상'),
    ]
    want_age = models.IntegerField(choices=ageChoices,blank=True)


    #mates = models.ManyToManyField(User, blank=True, related_name='trip', through='Mate')   
    def __str__(self):
        return str(self.user)

class MapInfo(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="map_info")
    # 구글맵 연동시 받아올 정보 부분 variable 추가 필요 


class Location(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="location")
    location = models.CharField(max_length=100)

class Mate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Matching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="match_user")
    mates = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="mate")
    # 0 : false / 1 : true / 2 : undefined
    toLike = models.IntegerField(default=2) 
    fromLike = models.IntegerField(default=2) 
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user
