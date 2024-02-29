from rest_framework import serializers

from .models import Product, User, Lesson


class UserSerializer(serializers.ModelSerializer):
    """ Модель пользователей """

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class LessonSerializer(serializers.ModelSerializer):
    """ Уроки """

    class Meta:
        model = Lesson
        fields = ['name', 'url_video']


class ProductSerializer(serializers.ModelSerializer):
    """ Вывод информации о продуктах """

    author = UserSerializer()
    # lesson = LessonSerializer(many=True)
    lesson_count = serializers.SerializerMethodField('get_lesson_count')

    class Meta:
        model = Product
        fields = ('author', 'name', 'price', 'start', 'lesson_count')

    def get_lesson_count(self, instance):
        return instance.get_lesson_count


