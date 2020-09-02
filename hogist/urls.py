from django.urls import path
from hogist import views
from hogist.mask_detection import index
from hogist.social_distancing import index as social_index
from hogist.mask_detection import index as mask_index
from hogist.testing_mask import index

urlpatterns = [
    # admin
    # path('admin-login/', views.admin_login, name='admin-login'),
    # path('admin-index/', views.admin_index, name='admin-index'),

    path('client/index/', views.index, name='index'),
    path('', views.landing, name='landing'),
    # path('login/', views.login, name='login'),
    # path('signup/', views.signup, name='signup'),
    path('client/logout/', views.logout, name='logout'),
    path('client/mask-detection/', views.mask_ip_details, name='mask_detection'),
    path('client/social-dis-detection/', views.social_dis_ip_details, name='social_detection'),
    # path('social-distancing', views.social_distancing, name='social_distancing'),

    # Streaming
    # path("stream_social-dis/", social_index, name="social-streaming"),
    # path("stream_Mask/", mask_index, name="Mask-streaming"),

    path('client/user_setting/', views.user_setting, name='user_setting'),

    path('client/change_password/', views.change_password, name='change_password'),

    path('client/show/', views.show_mask_stream, name='mask-stream'),
    path('client/show_social/', views.show_social_dis_stream, name='social-dis-stream'),
    # path('client/stream/', views.streaming, name='stream'),
    # path('st/', views.stream_mask, name='st'),

    path('client/mask', views.streaming, name='mask'),

]
