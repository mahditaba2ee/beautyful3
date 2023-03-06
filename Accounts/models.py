# from django.db import models

# # Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import MyUserManager


# # Create your models here.
# #coustom user model
class User(AbstractBaseUser):
    email = models.EmailField(max_length=200,unique=True)
    username = models.CharField(max_length=50,unique=True)
    phone = models.CharField(max_length=13,unique=True)
    address = models.CharField(max_length=500,blank=True)
    name =  models.CharField(max_length=50)
    family =  models.CharField(max_length=50)
    image = models.ImageField(upload_to='poster/')
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =('email','phone')

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

    def all_like_me_count(self):
        return self.like_product.all().count()

    def get_ful_name(self):
        return f'{self.name}  {self.family}'

   
        
# #send sms for register not working in now
class OtpCodeModel(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    code = models.CharField(max_length=500,null=True)
    created = models.DateTimeField(auto_now_add=True)

class QuestionModel(models.Model):
    name = models.CharField(max_length=50)
    que= models.CharField(max_length=500)
    answer = models.CharField(max_length=500,null=True)




# class NotifacationModel(models.Model):
#     user = models.ForeignKey(User,models.CASCADE,related_name='usernoti')
#     text = models.CharField(max_length=500,null=True)
#     view = models.BooleanField(default=False)


    
