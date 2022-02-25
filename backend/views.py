import cProfile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import JsonResponse
from .attachment import bulk_upload
import os




import stripe
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
import json
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings




def index(request):
    if request.user.is_authenticated:
        # get user
        user = request.user
        print(user)
        has_paid = Paid.objects.get(user = request.user)
        if has_paid.has_paid:
            print(has_paid.has_paid, 'has_paid')
            if request.method == 'POST':
                fileu = request.FILES['file'] if 'file' in request.FILES else None
                if fileu is not None:
                    if ".csv" in os.path.splitext(str(fileu))[-1] or ".tsv" in os.path.splitext(str(fileu))[-1]:
                        one = str(fileu)
                        two = one.replace("(", "")
                        three = two.replace(")", "")
                        mainFile = three.replace(" ", "_")
                        if uploader.objects.filter(file=mainFile).exists() != True:
                            cpath = os.getcwd()
                            fileS = uploader(username=request.user, file=fileu)
                            fileS.save()
                            fileG = uploader.objects.get(file=mainFile)
                            mFile = os.path.join(cpath, "media/{}".format(fileG.file))
                            bulk_upload(mFile)
                            print("edited")
                            return JsonResponse({'data' : True}, safe=False)
                        elif uploader.objects.filter(file=mainFile).exists():
                            return JsonResponse({'data' : False}, safe=False)
                    else:
                        return JsonResponse({'data' : 'false1'}, safe=False)
            return render(request, 'drag_drop.html')
        else:
            return redirect('package')
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
                Paid.objects.create(user=user, has_paid=False)
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

def package(request):
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'package.html', context)

def logouted(request):
    logout(request)
    return redirect('/signin/')

def allfiles(request):
    data = uploader.objects.all()
    return render(request, "allfiles.html", {"data": data})





######################################
######################################
########## Payment Gateway ###########
######################################
######################################
@csrf_exempt
def create_checkout_session(request):

    request_data = json.loads(request.body)
    # product = get_object_or_404(Package, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        payment_method_types=['card'], 
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': 'Package',
                    },
                    'unit_amount': int(10) * 100,
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )

    order = StripeOrder()
    user_obj = User.objects.get(username=request.user)
    order.user = user_obj
    order.status = 'create'
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "payments/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        order = get_object_or_404(StripeOrder, stripe_payment_intent=session.payment_intent)
        order.status = 'Paid'
        order.save()
        has_paid, true_false = Paid.objects.get_or_create(user = request.user)
        print(has_paid, true_false, 'Hhihihihi')
        has_paid.has_paid = True
        has_paid.save()
        return render(request, self.template_name)

class PaymentFailedView(TemplateView):
    template_name = "payments/payment_failed.html"