from datetime import datetime
import os
from django.db import transaction
from alipay import AliPay
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import CourseExpire
from edu_api.settings.develop import BASE_DIR
from order.models import Order
from payments.models import UserCourse


class AliPayAPIView(APIView):

    def get(self, request):
        """生成支付链接"""

        order_number = request.query_params.get("order_number")
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return Response({"message": "对不起，当前订单不存在"})

        # 支付的初始化参数
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG['appid'],  # 沙箱支付的应用id
            app_notify_url=settings.ALIAPY_CONFIG['app_notify_url'],  # 默认回调url
            app_private_key_string=settings.ALIAPY_CONFIG['app_private_key_path'],  # 应用私钥
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=settings.ALIAPY_CONFIG['alipay_public_key_path'],
            sign_type=settings.ALIAPY_CONFIG['sign_type'],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG['debug'],  # 默认False
        )

        # 生成支付宝的支付链接
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_number,
            total_amount=float(order.real_price),
            subject=order.order_title,
            return_url=settings.ALIAPY_CONFIG['return_url'],
            notify_url=settings.ALIAPY_CONFIG['notify_url']  # 可选, 不填则使用默认notify url
        )

        # 生成支付的链接地址  需要将order_string与网关拼接进行拼接
        url = settings.ALIAPY_CONFIG['gateway_url'] + order_string

        return Response(url)

class AiliPayResultAPIView(APIView):
    """
    处理支付成功后的业务：验证支付情况
    """

    def get(self, request):
        # 支付的初始化参数
        alipay = AliPay(
            appid=settings.ALIAPY_CONFIG['appid'],  # 沙箱支付的应用id
            app_notify_url=settings.ALIAPY_CONFIG['app_notify_url'],  # 默认回调url
            # app_private_key_string=app_private_key_string,  # 应用私钥
            # # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # alipay_public_key_string=alipay_public_key_string,
            app_private_key_string=settings.ALIAPY_CONFIG['app_private_key_path'],  # 应用私钥
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=settings.ALIAPY_CONFIG['alipay_public_key_path'],
            sign_type=settings.ALIAPY_CONFIG['sign_type'],  # RSA 或者 RSA2
            debug=settings.ALIAPY_CONFIG['debug'],  # 默认False
        )

        # 验证alipay的异步通知，
        data = request.query_params.dict()
        signature = data.pop("sign")
        success = alipay.verify(data, signature)

        if success:
            # 验证支付结果成功后 开始处理订单相关的业务
            return self.order_result_pay(data)

        return Response({"message": "对不起，当前订单支付失败"})

    def order_result_pay(self, data):
        """
        修改订单
        生成用户购买记录
        展示购买的订单信息
        :return:
        """

        # 先查看订单是否成功
        order_number = data.get('out_trade_no')

        try:
            order = Order.objects.get(order_number=order_number, order_status=0)
        except Order.DoesNotExist:
            return Response({"message": "对不起，当前订单支付出现异常了"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            savepoint = transaction.savepoint()

            try:
                # 更新订单信息
                order.pay_time = datetime.now()
                order.order_status = 1
                order.save()

                # 根据订单获取对应的用户
                user = order.user
                # 获取购买订单的所有课程
                order_courses_all = order.order_courses.all()
                # 订单结算页所需的课程信息
                course_list = []

                for course_detail in order_courses_all:
                    """遍历本次订单中所有的商品"""
                    # 课程购买人数的增长
                    course = course_detail.course
                    course.students += 1
                    course.save()

                    # TODO 判断用户购买的课程是永久有效 如果不是永久有效则记录到期时间
                    pay_timestamp = order.pay_time.timestamp()

                    # # 不是永久课程
                    # if course_detail.expire > 0:
                    #     # 处理到期时间  最终到期时间= 购买时间+有效期
                    #     pass
                    # else:
                    #     # 永久购买
                    #     end_tome = None
                    # 如果购买的不是永久的课程
                    if course_detail.expire > 0:
                        expire = CourseExpire.objects.get(pk=course_detail.expire)
                        expire_timestamp = expire.expire_time * 24 * 60 * 60
                        # 当前购买时间 + 有效期时间 = 最终到期时间
                        end_time = datetime.fromtimestamp(pay_timestamp + expire_timestamp)
                    else:
                        # 永久购买
                        end_time = None

                        # # TODO 为用户生成购买记录
                        # UserCourse.objects.create()

                        # TODO 为用户生成购买课程的信息
                        UserCourse.objects.create(
                            user_id=user.id,
                            course_id=course.id,
                            trade_no=data.get("trade_no"),
                            buy_type=1,
                            pay_time=order.pay_time,
                            out_time=end_time,
                        )

                    # # TODO 为前端返回所需的信息
                    # course_list.append()
                    course_list.append({
                        "id": course.id,
                        "name": course.name
                    })

            except Order.DoesNotExist:
                transaction.savepoint_rollback(savepoint)
                return Response({"message": "订单信息更新失败"})

            # return Response({"message": "支付成功",
            #                  "success": "success",
            #                  "real_price": 100})
            #
                # 返回订单结算页面所需的数据
        return Response({"message": "支付成功",
                         "success": "success",
                         "pay_time": data.get("timestamp"),
                         "real_price": order.real_price,
                         "course_list": course_list
                         })


