from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name='index'),
    path('token/', obtain_auth_token, name='api-token'),  # Add this line for token authentication
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.custom_register, name='register'),
    path('users/', views.user_list, name='user_list'),
    path('user_detail/', views.user_detail, name='user_detail'),
    # Add other views as needed
    path('questions/', views.question_list_create, name='question-list-create'),
    path('questions/<int:question_id>/replies/create/', views.reply_create, name='reply-create'),
    path('questions/<int:question_id>/', views.question_detail, name="question-detail"),
    path('questions/<int:question_id>/replies/', views.get_replies_for_question, name="get-replies-for-question"),
]
