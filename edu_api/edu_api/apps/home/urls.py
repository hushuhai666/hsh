from django.urls import path

from home import views

urlpatterns = [
    path("banners/", views.BannerListAPIView.as_view()),
    path("header/", views.FooterListAPIViewh.as_view()),
    path("footer/", views.FooterListAPIViewf.as_view()),
]