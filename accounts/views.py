from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib import auth
from .models import *
from feeds.models import *
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate as django_authenticate
from django.contrib import messages 
from django.core.paginator import Paginator 
from django.utils import timezone
from TripMate.settings import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_STORAGE_BUCKET_NAME,AWS_S3_REGION_NAME
import boto3
from boto3.session import Session
from datetime import datetime
from sightengine.client import SightengineClient
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
def check(request):
    return render(request, 'accounts/check.html')

def signup(request):
    if request.method == "POST":
        print("zzz",request.method)
        name = request.POST['name']
        user_id = request.POST['user_id']
        password = request.POST['password']
        password2 = request.POST['password2']
        nickname = request.POST['nickname']
        gender = GENDER_OPTION[1] if request.POST['gender'] == 'male' else GENDER_OPTION[0]
        age = request.POST['age']
        
        file_to_upload = request.FILES.get('img')
        session = Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_S3_REGION_NAME
        )
        # s3 = session.resource('s3')
        now = datetime.now().strftime("%Y%H%M%S")
        # img_object = s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
        #     Key = user_id+now,
        #     Body = file_to_upload
        # )
        # s3_url = "https://tripmate-storage.s3.ap-northeast-2.amazonaws.com/"

        client = SightengineClient('1514919083', 'vHQ735wsS4nPrHYkyB2T')
        # output = client.check('nudity').set_url(s3_url + user_id + now)
        # output_nudity = output["nudity"]
        # raw = output_nudity['raw']
        # safe = output_nudity['safe']
        # partial = output_nudity['partial']
        # print(raw,safe,partial)
        # if(raw > 0.6 or partial > 0.6 or len(output_nudity) != 3 ):
        #     return redirect('check')
        # else:   
        if password == password2:
            user = User.objects.create_user(
                username = user_id,
                password = password, 
            )
            user.profile.name = name
            user.profile.nickname = nickname 
            user.profile.gender = gender
            user.profile.age = age 
            # user.profile.photo = s3_url + user_id + now
            print(user)
            user.save()
        
        login_user = django_authenticate(username=user_id, password=password)
        django_login(request, login_user)
        return redirect('main')

    return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']
        user = auth.authenticate(request, username=user_id, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('main')

        else:
            if user_id == "" or password == "":
                error = "아이디와 비밀번호를 모두 입력해주세요."
            else:
                error = "아이디와 비밀번호를 확인해주세요."
        return render(request, 'accounts/login.html', {'error': error})

    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('main')

def notice(request, id):
    notices = Notice.objects.filter(user_to = request.user.id).order_by('-created_at')
    if notices is not None:
        count = notices.filter(checked=False).count()
    else:
        count = 0
    paginator = Paginator(notices, 7)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    page_numbers_range = 10 
    max_index = len(paginator.page_range)
    current_page = int(page) if page else 1 
    start_index = int((current_page -1)/page_numbers_range) * page_numbers_range 
    end_index = start_index + page_numbers_range 

    if end_index >= max_index:
        end_index = max_index 

    paginator_range = paginator.page_range[start_index:end_index]

    return render(request, 'accounts/notice.html', {'id':id, 'notices':notices, 
                'count':count, 'posts':posts, 'paginator_range': paginator_range })

   
def chatroom(request, rid):
    chatroom = ChatRoom.objects.get(id=rid)
    print(chatroom)
    trip = Trip.objects.get(id=chatroom.trip_id)
    messages = chatroom.messages.all().order_by('sent_at')

    for member in chatroom.chatmember.all():
        if member.user.id == request.user.id:
            member.notice = 0
            member.save()
            chatroom.save()
        else:
            friend = member.user.profile.nickname
            print(friend)

    return render(request, 'accounts/chatroom.html', {'rid': rid, 'messages': messages, 'friend': friend, 'trip':trip.place})

def chatlist(request, id):
    chatrooms = ChatRoom.objects.all().order_by('-updated_at')
    chatlists = list()
    print(chatrooms.count())

    for chat in chatrooms:
        notice = 0
        exist = False
        
        for member in chat.chatmember.all():
            trip = Trip.objects.get(id=chat.trip_id)
            lastmessage = chat.messages.all() 

            if lastmessage.count() != 0:
                lastmessage = lastmessage.order_by('-sent_at')[0]

            if member.user.id == request.user.id:
                exist = True
                notice = member.notice
                print(chat.id, "chat id")
            else:
                print(member.user.profile.nickname, "상대방 이름")
                friend = member.user.profile.nickname
        
        if exist:
            chatlists.append([chat, lastmessage, notice, trip.place, friend])

    return render(request, 'accounts/chatlist.html', {'chatlists': chatlists})

def send_message(request, rid, id):
    if request.method == 'POST':
        content = request.POST['content']
        chatroom = ChatRoom.objects.get(id=rid)
        chatroom.updated_at = timezone.now()
        Message.objects.create(author_id=id, content=content, chatroom_id=rid)

        for member in chatroom.chatmember.all():
            if member.user.id != request.user.id:
                member.notice += 1  
                member.save()
                print(member, " member ")
                print("notice ", member.notice)
            
        chatroom.save()  
        print(chatroom)
    return redirect('chatroom', rid=rid)

# like button을 눌렀을때, follow_profile로 가도록 설정한다. 
def follow_trip(request, pk, tid, num):
    follow_from = Profile.objects.get(user_id=request.user.id)
    follow_to = Profile.objects.get(user_id=pk)
    print("follow trip views")

    try:
        place = Trip.objects.get(id=tid).place
        print("place 존재")
    except Trip.DoesNotExist:
        print("place 없음")
        return redirect('main', num=num)

    try:
        follow_already = Follow.objects.filter(follow_from=follow_from, follow_to=follow_to, place=place)
        print("place 존재")
        print(follow_already)
    except Follow.DoesNotExist:
        follow_already = None
    
    if follow_already.count() != 0:
        # follow_already.delete()
        print("follow 존재")
        return redirect('main', num=num)

    else:
        f = Follow()
        f.follow_from, f.follow_to, f.place = follow_from, follow_to, place
        f.save()

        try:
            # 원래 filter가 아니라 get을 사용해야하는데, 복수 매칭을 대비해서 사용
            follow_back = Follow.objects.filter(follow_from=follow_to, follow_to=follow_from, place=place)
        except Follow.DoesNotExist:
            follow_back = None 
            
        if follow_back.count() != 0: 
            chatroom = ChatRoom.objects.create(trip_id=tid, place=place)
            ChatMember.objects.create(user_id=request.user.id, chatroom_id = chatroom.id)
            ChatMember.objects.create(user_id=pk, chatroom_id=chatroom.id)
            print("yes follow back")

            for follow in follow_back:
                follow.deny = False
                follow.save()
            
            for follow in follow_already:
                follow.deny = False
                follow.save()

            # follow_back.save()
            f.deny = False
            f.save()
            return render(request, 'accounts/chatroom.html', {'rid': chatroom.id })

        else:
            print("no follow back")
            return redirect('main', num=num)


def unfollow_trip(request, pk, tid, num):
    follow_from = Profile.objects.get(user_id=request.user.id)
    follow_to = Profile.objects.get(user_id=pk)

    try:
        place = Trip.objects.get(id=tid).place
    except Trip.DoesNotExist:
        return redirect('main', num=num)

    f = Follow()
    f.follow_from, f.follow_to, f.place, f.deny = follow_from, follow_to, place, True
    f.save()

    return redirect('main', num = num)
  
