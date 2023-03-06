from django.shortcuts import render
from django.views import View
from django.http import  JsonResponse ,HttpResponse
from .forms import UserLoginForm , UsercreateForm
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render ,redirect
from django.contrib import messages
from .models import User , OtpCodeModel
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from random import randint
from utils.hash import hash_code
from utils.send_email import send_email_for_register
from .models import QuestionModel
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.



# from secrets import choice
# 
# from django.conf import settings

# 

# # from category.models import OrderModel
# # 
# 
# from .models import CompanyModel, User , OtpCodeModel
# from random import randint
# from django.core.mail import send_mail
# 
# 
# import string
# from comment.models import CommentModel, ReplayCommentModel
import time


# Create your views here.


class ShowFormLoginRegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Category:home')
        return super().dispatch(request, *args, **kwargs)

    def get(Self,request):
        return render(request,'Accounts/login_register.html')
    



class LoginView(LoginRequiredMixin,View):
 
    def post(self,request):
        form =UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['email'].lower()
            password = cd['password']
            user = authenticate(request,username=username , password=password)
            
            if user is not None:
                code = str(randint(10000,99999))
                send_email_for_register(user.email,str(code))
                otp = OtpCodeModel.objects.filter(user=user)
                if otp.exists():
                    otp.delete()
                OtpCodeModel.objects.create(user=user,code=hash_code(code))
                request.session['user'] = {
                'email':username,
                'password':password,
                
            }
                return render(request,'Accounts/otpcode.html')
                
            else:
                return JsonResponse({'login':'user_not_found'})
        else:
            if form.errors:
                print('sss')
            return JsonResponse({'login':'form_not_valid'})

class LogoutView(View):
    def get(self ,request):
        logout(request)
        messages.success(request,'شما با موفقیت خارج شدید','success')
        return redirect('Accounts:login_register')






class OtpCodeView(View):
    def post(self,request):
        email= request.session['user']['email']
        password = request.session['user']['password']
        user = authenticate(request,username=email,password=password)
        
        otp = OtpCodeModel.objects.get(user=user)
        if str(otp.code) == hash_code(request.POST['otpcode']):
            otp.delete()
            login(request,user)
            return JsonResponse({'status_login':'login'})
        return JsonResponse({'status_login':'no_login'})


class RegisterView(View):
    def post(self,request):
        form = UsercreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email'].lower()
            username = cd['username'].lower()
            phone = cd['phone']
            password = cd['password1']
            User.objects.create_user(email=email,username=username,phone=phone,password=password)
            return JsonResponse({'register':'user_register'})
        else:
            lst_err = list(form.errors.as_data().keys())
            return JsonResponse({'register':'form_error','error':lst_err})
            
           



class PasswordResetView(auth_view.PasswordResetView):
    template_name = 'Accounts/reset/password_reset.html'
    email_template_name = 'Accounts/reset/email.html'
    success_url=reverse_lazy('Accounts:password_reset_done')
    
    print(email_template_name)





class PasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'Accounts/reset/password_reset_done.html'




class PasswordResetConfirm(auth_view.PasswordResetConfirmView):
    template_name='Accounts/reset/password_reset_confirm.html'
    success_url=reverse_lazy('Accounts:password_reset_complate')
    


class PasswordResetComplateView(auth_view.PasswordResetCompleteView):
    template_name = 'Accounts/reset/password_reset_complate.html'



class ContactView(View):
    def get(self,request):
        return render(request,'Accounts/contact_us.html')
    def post(self,request):
        cd = request.POST
        name = cd['txt_name']
        que = cd['txt_question']
        QuestionModel.objects.create(name=name,que=que)
        messages.success(request,'سوال شما ثبت شد و در اسرع وقت به آن پاسخ داده میشود و در بخش سوالات به نمایش گداشته میشود ','success')
        return redirect('Accounts:contact')

class QuestionsView(View):
    def get(self,request):
        question = QuestionModel.objects.all()
        return render(request,'Accounts/quastion.html',{'question':question})


class Answer_QuestionsView(View):
    def get(self,request):
        question = QuestionModel.objects.filter(answer__isnull=True)
        return render(request,'Accounts/answer.html',{'question':question})
    def post(self,request):
        question =QuestionModel.objects.get(id= request.POST['id'])
        question.answer = request.POST['answer']
        question.save()
        return JsonResponse({'id':request.POST['id']})


class UserProfileView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'Accounts/profile.html')
    
    def post(self,request):
        info = request.POST
        user = User.objects.get(id = request.user.id)
        try:
            name = info['txt_name'].split(' ')[0]
            family = info['txt_name'].split(' ')[1]
            user.name = name
            user.family = family
            user.username = info['txt_username']
            user.email = info['txt_email']
            user.phone = info['txt_phone']
            user.address = info['txt_address']
            img = request.FILES['img']
            user.image = img

            user.save()
            if request.GET.get('next') =='orderview':
                return redirect('category:order')
            messages.success(request,'پروفایل شما با موفقیت تکمیل شد ','success')
            return redirect('Category:home')
        except:
            messages.success(request,'عملیات با خطا مواجه شد','success')
            return redirect('Accounts:profile')

        



class Check_Information_View(View):
    def post(self,request):
        txt_name = request.POST['txt_name']
        txt_value =  request.POST['txt_value']
        if txt_name == 'phone':
            if txt_value != request.user.phone:
                user = User.objects.filter(phone =txt_value ).exists()
                if user:
                    return JsonResponse({'phone_status':False})
            return JsonResponse({'phone_status':True})
        if txt_name == 'email':
            if txt_value != request.user.email:
                user = User.objects.filter(email =txt_value ).exists()
                if user:
                    return JsonResponse({'email_status':False})
            return JsonResponse({'email_status':True})
        if txt_name == 'username':
            if txt_value != request.user.username:
                user = User.objects.filter(username =txt_value ).exists()
                if user:
                    return JsonResponse({'username_status':False})
            return JsonResponse({'username_status':True})





# class NotifacationView(View):
#     def get(self,request):
#         myorders = OrderModel.objects.filter(usersender=request.user,view=False)
#         # for order in myorders:
#         #     order.view = True
#         #     order.save
#         return render(request,'accounts/noti.html',{'myorders':myorders})
#     def post(self,request):
#         idorder = request.POST.get('idorder')
#         iduser = request.POST.get('iduser')






# class NotificationsView(View):
#     def get(self,request):
#         comments = ReplayCommentModel.objects.filter(to_user = request.user.username,view=False)
#         comments_tag = CommentModel.objects.filter(to_user = request.user.username)
        
#         comments_view = ReplayCommentModel.objects.filter(to_user = request.user.username,view=True)
#         return render(request,'accounts/notifications.html',{'comments':comments,'comments_view':comments_view,'comments_tag':comments_tag})
    
#     def post(self,request):
#         comments = ReplayCommentModel.objects.filter(to_user = request.user.username)
#         for c in comments:
#             c.view =True
#             c.save()
#         return JsonResponse({'status':'ok'})

