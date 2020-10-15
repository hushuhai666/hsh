import xadmin

from course import models


class CourseCategoryModelAdmin(object):
    pass


xadmin.site.register(models.CourseCategory, CourseCategoryModelAdmin)


class CourseModelAdmin(object):
    pass


xadmin.site.register(models.Course, CourseModelAdmin)


class CourseChapterModelAdmin(object):
    pass


xadmin.site.register(models.CourseChapter, CourseChapterModelAdmin)


class CourseLessonModelAdmin(object):
    pass


xadmin.site.register(models.CourseLesson, CourseLessonModelAdmin)


class TeacherModelAdmin(object):
    pass


xadmin.site.register(models.Teacher, TeacherModelAdmin)

"""
以下是课程优惠相关的
"""


class PriceDiscountTypeModelAdmin(object):
    """价格优惠类型"""
    pass


xadmin.site.register(models.CourseDiscountType, PriceDiscountTypeModelAdmin)


class PriceDiscountModelAdmin(object):
    """价格优惠公式"""
    pass


xadmin.site.register(models.CourseDiscount, PriceDiscountModelAdmin)


class CoursePriceDiscountModelAdmin(object):
    """商品优惠和活动的关系"""
    pass


xadmin.site.register(models.CoursePriceDiscount, CoursePriceDiscountModelAdmin)


class ActivityModelAdmin(object):
    """商品活动模型"""
    pass


xadmin.site.register(models.Activity, ActivityModelAdmin)


class CourseExpireModelAdmin(object):
    """课程有效期模型"""
    pass


xadmin.site.register(models.CourseExpire, CourseExpireModelAdmin)
