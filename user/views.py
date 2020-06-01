from django.shortcuts import render, redirect, get_object_or_404
from .models import User_db
from hit_book.models import hit_book
from .opt_validation import OTP

# Create your views here.


def login_view(request, post_id=None):  # get the  details and check whether they match with the username and password in the db
    context = {'err': ''}
    if request.POST:
        username = request.POST['username'] 
        password = request.POST['password']
        val = User_db.login_check(username, password)
        if not val[0]: # if false
            context['err'] = 'wrong password bitch  '
            return render(request, 'login.html', context)
        else: 
            request.session['user_id_hit'] = val[1]
            if post_id is None :
                return redirect('/home') 
            else:
                return redirect(f'/view/hit/{post_id}/')  # if the email is sent to the user then the user can directly view the post after logging in 
    return render(request, 'login.html', context)

def create_user_view(request): # opt verification pending. 
    if request.POST:
        otp  = OTP()
        otp.generate_otp()
        request.session['otp'] = otp.otp
        otp.send_email(user_email=request.POST['email'])
        request.session['user_save'] = {'user_name':request.POST['username'],
                                        'email':request.POST['email'], 
                                        'password':request.POST['password1']}
        return redirect('/signup/1')
    return render(request, 'create/user.html')

def otp_check(request, validation):
    context = {}
    if request.POST: 
            if int(request.POST['otp']) == int(request.session['otp']): 
                user_data = request.session['user_save']
                request.session['user_save'] = None 
                user = User_db(user_name=user_data['user_name'],email=user_data['email'], password= user_data['password'])
                user.create_user()
                request.session['user_id_hit'] = str(User_db.objects.latest('id').id) # storing the user id in sessions so anyone cannot access anyones blogs 
                hit_book.objects.create(title='general', description='general', user_id=request.session['user_id_hit']) # creating a general book class to add the random hit's of the user. 
                return redirect('/home')
            else:
                context = {'err':'INVALID OTP'}
                return render(request,'otp.html',context)        
    return render(request,'otp.html',context)
