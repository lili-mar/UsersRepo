from django.shortcuts import render, HttpResponse, redirect  #test HttpResponse
from .models import *               #import ALL models
from django.contrib import messages     #validation
import bcrypt

#Login/Reg = localhost:8000
def landing(request):
    request.session.flush()
    return render(request, 'landing.html')

def register(request):
    if request.method == 'POST':
        print(request.POST) #should see QueryDict
        
        errors = User.objects.reg_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')    #redirect the user back to the form to fix the errors
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()    
            new_user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = hashed_pw)       
            request.session['user_id'] = new_user.id
            messages.success(request, "You have successfully registered!")
            return redirect('/success')

def login(request):
    if request.method == 'POST':
        print(request.POST) #should see QueryDict
        
        errors = User.objects.login_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')    #redirect the user back to the form to fix the errors
        else:
            this_user = User.objects.get(email = request.POST['email'])   
            request.session['user_id'] = this_user.id
            messages.success(request, "You have successfully logged in!")
            return redirect('/success')
 
# replace with Your NEW APPLICATION    
def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)