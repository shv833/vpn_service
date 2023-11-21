from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from bs4 import BeautifulSoup

import requests


# Create your views here.
def index(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'index.html', {'username':user.get_username()})
    return render(request, 'index.html')

@login_required
def profile(request):
    user = request.user
    data = UserSite.objects.filter(user_id=user.id).values()
    for i in data:
        i['route'] = i['site_name'] + '/' + i['url']

    return render(request, 'profile.html', {'username':user.get_username(), 'user_id' : user.id,'data': data})

@login_required
def proxy(request, site_name, url):
    user = request.user
    data = UserSite.objects.get(user_id=user.id, site_name=site_name, url=url)
    
    response = requests.get(url)
    
    content = response.content.decode('utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    for tag in soup.find_all(['a', 'img']):
        original_url = tag.get('href') or tag.get('src')
        new_route = f'/{site_name}/{original_url}'
        if tag.get('href'):
            tag['href'] = new_route
        # if tag.get('src'):
        #     tag['src'] = f'{url}{original_url}'

    # response.content = str(soup).encode('utf-8')

    
    
    data.page_views += 1
    data.data_transferred += len(response.content)
    
    data.save(update_fields=["page_views", "data_transferred"])
    return render(request, 'proxy.html', {'src': str(soup)})


@login_required
def delrecord(request, pk):
    UserSite.objects.get(id=pk).delete()
    return redirect('profile')

@login_required
def addrecord(request):
    if request.method == "POST":
        site_name = request.POST.get('site_name')
        url = request.POST.get('url')
        UserSite.objects.create(user_id=request.user.id, site_name=site_name, url=url, page_views=0,data_transferred=0)
        return redirect('profile')
    return render(request, 'add_record.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        newuser = User.objects.create_user(username, password=password)
        
        newuser.save()
        messages.success(request, "Your account have been created successfully")
        
        return redirect('signin')
    
    return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            return render(request, 'index.html', {'username':user.get_username()})
        else:
            messages.error(request,"bad creds")
            return redirect('index')
    
    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('index')