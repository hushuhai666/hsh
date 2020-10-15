import re

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from rest_framework import serializers
from user.models import UserInfo
from user.utils import get_user_by_account
from rest_framework import exceptions


class UserModelSerializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")

    class Meta:
        model = UserInfo
        fields = ("id", "username", "password", "phone", "token")

        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "username": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
            },
            "phone": {
                "write_only": True,
            },
        }


    def validate(self, attrs):
        phone = attrs.get('phone')
        passward = attrs.get('passward')

        user = UserInfo.objects.filter(phone=phone)
        if user:
            raise exceptions.ValidationError('用户已存在')


        # 验证手机号格式  密码格式
        if not re.match(r"1[3-9]\d{9}$", phone):
            raise serializers.ValidationError("手机号格式不正确")

        # 验证手机号是否被注册
        try:
            user = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user = None

        if user:
            raise serializers.ValidationError("当前手机号已经被注册")

        #验证密码是否符合
        # if not re.match(r"/^\w{5,16}$/", passward):
        #     raise serializers.ValidationError("密码不符合要求，请重新输入")

        return attrs


    def create(self, validated_data):
        """
        用户信息设置
        用户名  token  密码加密
        """
        # 对密码进行加密处理
        password = validated_data.get("password")
        hash_password = make_password(password)

        # 为用户名设置默认值  随机字符串  手机号
        username = validated_data.get("phone")

        # 添加数据
        user = UserInfo.objects.create(phone=username, username=username, password=hash_password,)

        # TODO 为注册成功的用户生成token
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        print(user)

        return user


