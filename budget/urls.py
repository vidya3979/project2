"""budgetmonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .views import registration,signin,signout,expens_create,view_expense,edit_expense,delete_expense,review_expense

urlpatterns = [
    path("",lambda request:render(request,"budget/base.html")),
    path('registration',registration,name='registration'),
    path('signin',signin,name="signin"),
    path('signout',signout,name='signout'),
    path('addexpens',expens_create,name="addexpens"),
    path('viewexpens',view_expense,name='viewexpens'),
    path("editexpens/<int:id>",edit_expense,name="editexpens"),
    path("deleteexpens/<int:id>",delete_expense,name="deleteexpens"),
    path("reviewexpens",review_expense,name="reviewexpens"),
]
