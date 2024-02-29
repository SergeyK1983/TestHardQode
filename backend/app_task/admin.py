from django.contrib import admin
from .models import User, Product, StudentsToProduct, Lesson, Group, StudentsInGroup


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'teacher', 'student')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'price', 'start', 'min_quantity', 'max_quantity')


class StudentsToProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'product')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'name', 'url_video')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'name', 'min_quantity', 'max_quantity')


class StudentsInGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'group')


admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(StudentsToProduct, StudentsToProductAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(StudentsInGroup, StudentsInGroupAdmin)
