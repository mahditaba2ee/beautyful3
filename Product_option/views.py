from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from Category.models import ProductModel
from .models import CommentModel,ReplayCommentModel
from Accounts.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class RankView(View):
    def post(self,request):
        type_request = request.POST['type_request']
        product_id = request.POST['product_id']
        product = ProductModel.objects.get(id = product_id)
        if request.user.is_authenticated: 
            username = request.user.username
            if type_request == 'start':
                if product.star.get(str(username)):
                    return JsonResponse({'rank':product.star,'username':username})
                return JsonResponse({'rank':product.star})
            rank = request.POST['rank']
            product.star[str(username)] =str( rank)
            product.save()
            return JsonResponse({'rank':product.star,'username':username})
        return JsonResponse({'status':'not_login','rank':product.star})



class CommentAddView(View):
    def post(self,request):
        cd = request.POST
        comment_body = cd['comment_body']
        product_id = cd['product_id']
        comment_id = cd['comment_id']

        product = ProductModel.objects.get(id=product_id)
        if comment_id=='':
            comment = CommentModel.objects.create(user=request.user,product = product,body=comment_body)
        
            if comment_body[0] == '@':
                user = comment_body.split(' ',1)[0][1::]
                if User.objects.filter(username= user).exists():
                    comment.to_user = user
                    comment.save()
                    return JsonResponse({'status':'comment'})
                

        else:
            c=CommentModel.objects.get(id=comment_id)
            user = comment_body.split(' ',1)[0][1::]
            ReplayCommentModel.objects.create(user = request.user ,to_user=user, comment=c,body=comment_body)
        messages.success(request,'نظر شما ثبت شد','success')
        return JsonResponse({'status':'commentrrr'})


class LikeView(LoginRequiredMixin,View):
    def post(self,request):
        if request.user.is_authenticated:
            id_product = request.POST['id_product']
            is_like = request.POST['is_like']
            product = ProductModel.objects.get(id = id_product )

            if (is_like == 'dislike'):
                if request.user in product.like.all():
                    product.like.remove(request.user)
                    product.like_count -=1
                    product.save()
                    all_like_me_count = request.user.all_like_me_count()
                    return JsonResponse({'like_status':'dislike','like_number':product.like.count(),'all_like_me_count':all_like_me_count})
                else:
                    return JsonResponse({'like_status':'like_before','like_number':product.like.count()})
            if (is_like =='like'):
                
                if request.user not in product.like.all():
                    product.like.add(request.user)
                    product.like_count +=1
                    product.save()
                    all_like_me_count = request.user.all_like_me_count()

                    return JsonResponse({'like_status':'like','like_number':product.like.count(),'all_like_me_count':all_like_me_count})
                else:
                    return JsonResponse({'like_status':'like_before','like_number':product.like.count()})
        else:
            return JsonResponse({'like_status':'no_login'})
