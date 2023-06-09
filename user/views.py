from django.shortcuts import render
from .forms import CreateUserForm,LogInForm
from .models import UserModel
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.
#홈페이지
def home(request):
    user = request.user.is_authenticated
    if user:# 로그인 상태
        return render(request,'home.html')
    else:
        return redirect('log-in')

def create_user_view(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():  # 2
            print("save")
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            password1 = request.POST.get('password_check1', '')
            password2 = request.POST.get('password_check2', '')

            if password1 ==password2:
                UserModel.objects.create_user(username=username,password=password1,email=email)
                return redirect('log-in')
        else:
            print(form.errors)
    else:
        pass
    form = CreateUserForm()
    return render(request, 'user/create_user.html', {'form': form})  # 4


def log_in_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        me = auth.authenticate(request, username=username,password=password)
        if me is not None:
            print("로그인")
            auth.login(request, me)
            return redirect('/')
        else:
            return redirect('/log-in', {'error': '유저이름 혹은 패스워드를 확인 해 주세요'})
    elif request.method =='GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
    form = LogInForm()
    return render(request, 'user/log_in.html',{'form': form})




@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')