# from rest_framework.serializers import ModelSerializer
#
# from course.models import CourseCategory
#
#
# class CourseCategoryModelSerializer(ModelSerializer):
#     class Meta:
#         model = CourseCategory
#         fields = ("id","name")


from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, CourseLesson, CourseChapter


class CourseCategoryModelSerializer(ModelSerializer):
    """课程分类序列化器"""

    class Meta:
        model = CourseCategory
        fields = ("id", "name")


class TeacherModelSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', "title", "signature", "image", "brief"]


class CourseModelSerializer(ModelSerializer):
    """课程序列化器"""

    teacher = TeacherModelSerializer()
    # print('我进来了')
    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", "lesson_list", "discount_name", "real_price"]

class CourseDetailModelSerializer(ModelSerializer):
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "students", "lessons", "pub_lessons", "price", "teacher", "level_name", "course_img",
                  "course_video", "brief_html", "real_price", "discount_name", "active_time"]

class CourseLessonSerializer(ModelSerializer):
    """课程课时"""

    class Meta:
        model = CourseLesson
        fields = ["id", "name", "free_trail"]


class CourseChapterModelSerializer(ModelSerializer):
    """课程章节"""
    coursesections = CourseLessonSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id', "chapter", "name", "coursesections"]
