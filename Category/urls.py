from operator import ne
from django.urls import path
from .views import *

app_name='Category'

urlpatterns=[
    path('',CategoryView.as_view(),name='home'),
    path('details/<str:cat_slug>/<str:type_slug>/<str:brand_slug>/<str:product_slug>',ProductDetailsView.as_view(),name='datails'),
    path('search/<str:category_slug>/',SearchCategoryView.as_view(),name='search_category'),
    path('text_search/<str:text_search>',BoxSearchView.as_view(),name='box_search'),
    path('search/<str:category_slug>/<str:type_slug>',SearchCategoryView.as_view(),name='search_category'),

    path('search/<str:category_slug>/<str:type_slug>/<str:name_product>',SearchCategoryView.as_view(),name='search_product'),

    path('shop',ShopView.as_view(),name='shop'),
    path('type/products/',TypeProductView.as_view(),name='type_product'),
    path('like',LikeCategoryView.as_view(),name='like'),
    path('most_view',Most_View.as_view(),name='most_view'),
    path('add_slide',Add_Slide_View.as_view(),name='add_slide'),
    path('add',AddProductView.as_view(),name='add_product'),
    path('Category/choise',ChoiseView.as_view(),name='choise'),
   




   


    ]