from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("get_preds/",get_preds, name="get_preds"),
]
