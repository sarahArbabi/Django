from django.shortcuts import render,redirect, reverse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.views import View
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from order.models import ItemOrder

class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.id) + text_type(timestamp))

email_generator = EmailToken()
# Create your views here.
def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user=User.objects.create_user(username=data['username'],first_name=data['firstname'],last_name=data['lastname'],email =data['email'],password=data['password2'])
            user.is_active = False
            user.save()
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('accounts:active',kwargs={'uidb64':uidb64,'token':email_generator.make_token(user)})
            link = 'http://' + domain + url
            email = EmailMessage(
                'active user',
                link,
                'sarrrah.262@gmail.com',
                [data['email']]
            )
            email.send(fail_silently=False)
            messages.warning(request,'return to email','warning')
            return redirect('home:home')
    else:
        form = UserSignupForm()
    return render(request,'accounts/signup.html',{'form':form})




def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,username=data['user'],password=data['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in successfully','success')
                return redirect('home:home')
            else:
                messages.error(request,'user or password is not valid','danger')
    else:
        form = UserLoginForm()
    return render(request,'accounts/login.html',{'form':form})



class RegisterEmail(View):
    def get(self,request,uidb64,token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if user and email_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('accounts:login')



def user_logout(request):
    logout(request)
    messages.success(request,'You logged out successfully','warning')
    return redirect('home:home')



@login_required(login_url='accounts:login')
def user_profile(request):
    profile = Profile.objects.get(user_id = request.user.id)
    return render(request,'accounts/profile.html',{'profile':profile})



@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == 'POST':
        userform = UserUpdateForm(request.POST, instance=request.user)
        profileform = ProfileUpdateForm(request.POST,request.FILES,instance= request.user.profile)
        if userform and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request,'Information updated successfully','success')
            return redirect('accounts:profile')
    else:
        userform = UserUpdateForm(instance=request.user)
        profileform = ProfileUpdateForm(instance= request.user.profile)
    context ={'userform':userform,'profileform':profileform}
    return render(request,'accounts/update.html',context)



@login_required(login_url='accounts:login')
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'Your password changed successfully','success')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'accounts/change.html',{'form':form})



class ResetPassword(auth_views.PasswordResetView):
    template_name = 'accounts/reset.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'accounts/link.html'


class DonePassword(auth_views.PasswordResetDoneView):
    template_name = 'accounts/done.html'



class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/confirm.html'
    success_url = reverse_lazy('accounts:complete')


class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/complete.html'


def favorite(request):
    product = request.user.fa_user.all()
    return render(request,'accounts/favorite.html',{'product':product})



def history(request):
    data = ItemOrder.objects.filter(user_id=request.user.id)
    return render(request,'accounts/history.html',{'data':data})































































