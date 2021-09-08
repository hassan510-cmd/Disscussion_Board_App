from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
# Create your views here.

def sign_up(request):

	if request.method=='POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			# print('form is valid')
			new_user=form.save()
			# print("there is new user",new_user)
			login(request,new_user)
			# print(request)
			return redirect('home')
	else:
		form =UserCreationForm()
	# form =UserCreationForm()
	return render(request,'signup.html', {'form':form})

def login_page(request):
	message = ""
	if request.method=='POST':
		print('enter login method')
		username=request.POST['username']
		password=request.POST['passwd']
		current_user=User.objects.get(username=username)
		# print(*dir(current_user),sep='\n')
		if current_user.check_password(password):
			login(request,current_user)
			print('logged successfully')

			return redirect('home')
		else:
			message="invalid user name or password"
			print(message)
		# print(request.POST['username'])
		# print('done')
	return render(request,'login-page.html',{"message":message})


def logout_page(request):

	print('enter',request)
	print(f"{request.user} logged out successfully")
	logout(request)
	return redirect('login_page')

#
# def user_setting(request):
# 	return render(request,'user-setting.html')