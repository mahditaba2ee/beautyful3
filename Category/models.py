from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from Accounts.models import User 
# Create your models here.


class CategoryModel(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=200,unique=True,null=True,blank=True)
    img = models.ImageField(upload_to='category/img',null=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.slug

    def save(self, *args,**kwargs):
        slug = str(self.name)
        self.slug =slugify(slug,allow_unicode=True)
        return super().save()
  
    def get_absoulut_url(self):
       
        return reverse('Category:search_category',args=(self.slug,))
        
     

   
class TypeProductModel(models.Model):
    category = models.ForeignKey(CategoryModel,models.CASCADE,related_name='type_to_category')
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category/img',null=True)
    slug = models.SlugField(max_length=100, unique=True,blank=True, verbose_name='آدرس لینک',)

    def __str__(self) -> str:
        return f'{self.name}   محصولی از   {self.category.name}'

    def save(self,*args,**kwargs):
        slug = self.category.slug+'-'+self.name
        self.slug =slugify(slug,allow_unicode=True)
        return super().save()
    def get_absoulut_url(self):
        return reverse('Category:search_category',args=(self.category.slug,self.slug))
        

     

class BrandModel(models.Model):
    category = models.ForeignKey(CategoryModel,models.CASCADE,related_name='brand_to_category',null=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200,unique=True,blank=True)
    des = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.slug
    def save(self,*args,**kwargs):
        
        slug = f'{self.category.slug}-{self.name}'
        self.slug = slugify(slug,allow_unicode=True)
        return super().save()
       

   
class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel,models.CASCADE,related_name='product_to_category')
    brand = models.ForeignKey(BrandModel,models.CASCADE,related_name='product_to_brand',null=True)
    type = models.ForeignKey(TypeProductModel,models.CASCADE,related_name='product_to_type',null=True,blank=True)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    des = models.CharField(max_length=500)
    all_price = models.IntegerField()
    off_price = models.PositiveIntegerField(null=True,blank=True)
    color = models.JSONField(default=dict,blank=True,null=True)

    slug = models.SlugField(max_length=200,unique=True,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    available=models.BooleanField(default=True)

    like = models.ManyToManyField(User,blank=True,related_name='like_product')
    star = models.JSONField(default=dict,blank=True,null=True)
    special = models.BooleanField(default=False)
    
    like_count = models.IntegerField(default=0)


    
    def get_absoulut_url(self):
       
        return reverse('Category:datails',args=(self.category.slug,self.type.slug,self.brand.slug,self.slug))
        
    
    
    def save(self,*args,**kwargs):

        if self.off_price != None:
            self.special =True
        else:
            self.special =False
        slug = self.full_name + str(self.id)
        self.slug=slugify(slug,allow_unicode=True)
        super().save()
        

    def get_like_user(self):
        return self.like.count()
      
    class Meta:
        ordering =('-like_count',)



class ImageProductModel(models.Model):
    product = models.ForeignKey(ProductModel,models.CASCADE,related_name='image_to_product',null=True,blank=True)
    image = models.ImageField(upload_to='product/')
   

    def save(self,*args,**kwargs):
        self.image.name=f'{self.product.name}.png'

        return super().save()


class ImagdeSlidModel(models.Model):
    image = models.ImageField()
    url = models.URLField()
    title = models.CharField(max_length=50,null=True)
    des=models.CharField(max_length=100,null=True)
    
 
