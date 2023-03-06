from django.urls import path
from .views import *
app_name ='Option'
urlpatterns=[

    path('rank',RankView.as_view(),name='rank'),
    path('comment',CommentAddView.as_view(),name='commet'),
    path('like',LikeView.as_view(),name='like')
    
]