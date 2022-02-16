import cProfile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import uploader
from django.http import JsonResponse
from .attachment import bulk_upload
import os

def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fileu = request.FILES['file'] if 'file' in request.FILES else None
            if fileu is not None:
                one = str(fileu).lower()
                two = one.replace("(", "")
                three = two.replace(")", "")
                mainFile = three.replace(" ", "_")
                if uploader.objects.filter(file=mainFile).exists() != True:
                    print('In else')
                    cpath = os.getcwd()
                    fileS = uploader(username=request.user, file=fileu)
                    fileS.save()
                    fileG = uploader.objects.get(file=mainFile)
                    mFile = os.path.join(cpath, "media/{}".format(fileG.file))
                    bulk_upload(mFile)
                    return JsonResponse("{'data' : True}", safe=False)
                if uploader.objects.filter(file=mainFile).exists():
                    return JsonResponse({'data' : False}, safe=False)
        return render(request, 'drag_drop.html')
    else:
        return redirect('/signin/')

def signin(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'index.html', {'msg':"Invalid Credentials!"})
    else:
        return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        cpassword = request.POST['pass1']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'msg':"Username Already Exists!"})
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('/signin/')
        else:
            return render(request, 'signup.html', {'msg':"Passwords Not Matched!"})
    else:
        return render(request, 'signup.html')

def subscription(request):
    if request.is_authenticated:
        return render(request, 'subscription.html')
    else:
        return redirect('/signin/')

def logouted(request):
    logout(request)
    return redirect('/signin/')

def allfiles(request):
    data = uploader.objects.all()
    return render(request, "allfiles.html", {"data": data})