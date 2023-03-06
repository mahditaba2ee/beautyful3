from django.contrib import admin
from .models import CommentModel,ReplayCommentModel
# Register your models here.
admin.site.register(CommentModel)
admin.site.register(ReplayCommentModel)
