from django.urls import path
from . import views


urlpatterns = [
    path('fetch', views.FetchListApi.as_view(), name='fetch'),
    path('submit/<int:questionnaire_id>', views.submit, name="response"),
    path('submit/<int:questionnaire_id>/<int:question_id>/<int:answer_id>',
         views.submit, name="response"),
    path('submit/<int:questionnaire_id>/<int:question_id>',
         views.submit, name="response")

]
