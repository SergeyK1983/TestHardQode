from rest_framework import serializers

from .models import Product, User, Lesson, Group


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
    lesson_count = serializers.SerializerMethodField('get_lesson_count')

    class Meta:
        model = Product
        fields = ('author', 'name', 'price', 'start', 'lesson_count')

    def get_lesson_count(self, instance):
        return instance.get_lesson_count


class ProductLessonsSerializer(serializers.ModelSerializer):
    """ Вывод информации о продукте с уроками """

    lesson = LessonSerializer(many=True)

    class Meta:
        model = Product
        fields = ('author', 'name', 'price', 'start', 'lesson')


class StudentsListingField(serializers.RelatedField):
    """ Поле get_users, модель StudentsInGroup """
    def to_representation(self, value):
        return f"студент/ка {value.student.first_name}"


class GroupSerializer(serializers.ModelSerializer):
    """ Группы """
    get_users = StudentsListingField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['name', 'get_users']


class ProductStudentsSerializer(serializers.ModelSerializer):
    """ Вывод информации о продукте и записанных студентах """

    group = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('author', 'name', 'start', 'group')


class GroupFullnessSerializer(serializers.ModelSerializer):
    """ Вывод групп с процентом заполненности """

    fullness = serializers.SerializerMethodField('get_fullness')

    class Meta:
        model = Group
        fields = ['name', 'fullness']

    def get_fullness(self, instance):
        return instance.fullness()


class ProductStatisticsSerializer(serializers.ModelSerializer):
    """ Вывод статистики о всех продуктах """

    percentage = serializers.SerializerMethodField('get_percentage')
    students_count = serializers.SerializerMethodField('get_students')
    avg_fullness = serializers.SerializerMethodField('get_avg_fullness')
    group = GroupFullnessSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'students_count', 'avg_fullness', 'percentage', 'group')

    def get_percentage(self, instance):
        return instance.percentage_of_purchases

    def get_students(self, instance):
        return instance.get_students_count

    def get_avg_fullness(self, instance):
        return instance.avg_fullness_group

