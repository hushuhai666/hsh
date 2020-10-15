from rest_framework.generics import ListAPIView

from edu_api.settings.constanst import BANNER_LENGTH
from home.models import Banner,Nav
from home.serializers import BannerModelSerializer,FooterModelSerializer


class BannerListAPIView(ListAPIView):
    """轮播图"""
    queryset = Banner.objects.filter(is_delete=False, is_show=True).order_by("-id")[:BANNER_LENGTH]
    serializer_class = BannerModelSerializer

class FooterListAPIViewh(ListAPIView):
    queryset = Nav.objects.filter(is_delete=False,is_show=True,position=1)
    serializer_class = FooterModelSerializer

class FooterListAPIViewf(ListAPIView):
    queryset = Nav.objects.filter(is_delete=False,is_show=True,position=2)
    serializer_class = FooterModelSerializer