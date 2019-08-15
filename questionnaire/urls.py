from django.urls import path
from . import views


urlpatterns = [
    path('fetch', views.FetchListApi.as_view(), name='fetch'),
    path('submit', views.submit, name="response")
]
