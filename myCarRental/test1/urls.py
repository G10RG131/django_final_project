from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('test1/', views.test1, name='test1'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('add_car/', views.add_car, name='add_car'),
    path('profile/', views.profile, name='profile'),
    path('car/delete/<int:car_id>/', views.delete_car, name='delete_car'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/like/<int:car_id>/', views.like_car, name='like_car'),
    path('car/delete/<int:car_id>/', views.delete_car, name='delete_car'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
