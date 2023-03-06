from django.core.mail import send_mail
from django.conf import settings
# from django.http import JsonResponse
# from django.views import View
# from .models import OrderItemsModel
# from Accounts.models import NotifacationModel
# class SendEmailView(View):
#     def post(self,request):
#         id = request.POST['iduser']
#         order_item=OrderItemsModel.objects.get(id = id)
#         name = order_item.product.name
#         order_id = order_item.order.id
#         email =  order_item.user_created.email
#         text =f"لطفا محصول {name} با کد سبد خریذ {order_id} را هر چه سریع تر تایید کنید "
#         send_mail('تاییدیه',text,settings.EMAIL_HOST_USER,(email,))

#         NotifacationModel.objects.create(user = order_item.user_created,text=text)

#         return JsonResponse({'status':email})





# def send_email(lst,id,email,address,name,family):
#     send_mail('تاییدیه',f'محصولات{lst}با کد{id}به آدرس {address}و مشخصات{name+family}ارسال شد با تشکر',settings.EMAIL_HOST_USER,(email,))
    
def send_email_for_register(email,txt):
    send_mail('کد ورود شما به سایت ',f'کد تایید شما {txt}میباشد لطفا کد را در اختیار کسی نگذارید',settings.EMAIL_HOST_USER,(email,))