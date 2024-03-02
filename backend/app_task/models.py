from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Модель пользователей """

    teacher = models.BooleanField(default=False, verbose_name="Преподаватель")
    student = models.BooleanField(default=True, verbose_name="Студент")

    def save(self, *args, **kwargs):
        if self.teacher and self.student:
            self.student = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-{self.username}"


# Создать сущность продукта. У продукта должен быть создатель этого продукта(автор/преподаватель).
# Название продукта, дата и время старта, стоимость (1 балл)
# Определить, каким образом мы будем понимать, что у пользователя(клиент/студент) есть доступ к продукту. (2 балл)
class Product(models.Model):
    """ Продукт """

    author = models.ForeignKey(User, to_field='username', related_name='author', on_delete=models.CASCADE,
                               verbose_name="Автор/Преподаватель")
    name = models.CharField(max_length=200, unique=True, verbose_name="Название")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Стоимость, руб")
    start = models.DateTimeField(verbose_name="Дата и время начала")
    min_quantity = models.IntegerField(default=2, verbose_name="min кол.")
    max_quantity = models.IntegerField(default=10, verbose_name="max кол.")
    students = models.ManyToManyField(User, related_name="get_prod", through='StudentsToProduct')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['id']

    @property
    def get_lesson_count(self):
        return self.lesson.all().count()

    @property
    def get_students_count(self):
        return self.get_users.all().count()

    @property
    def percentage_of_purchases(self):
        """ Процент покупок """
        all_students = User.objects.filter(student=True).count()
        students = self.get_users.all().count()
        percent = round(students / all_students * 100, 2)
        return percent

    @property
    def avg_fullness_group(self):
        """ Средняя заполненность групп """
        groups = self.group.all()
        fullness = 0
        for group in groups:
            fullness += group.fullness()
        avg_fullness = round(fullness / groups.count(), 2)
        return avg_fullness

    def __str__(self):
        return f"{self.id}-product: {self.name[:20]}"


class StudentsToProduct(models.Model):
    """
    Промежуточная модель для связи допущенных студентов с продуктом. Условно считаем, что продукт оплачен, после
    чего пользователь записан в эту модель
    """
    student = models.ForeignKey(User, related_name='product', to_field='username', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='get_users', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Допущенные студенты'
        verbose_name_plural = 'Допущенные студенты'
        ordering = ['id', 'product', 'student']

    # TODO защита от двойных записей


# Создать сущность урока. Урок может принадлежать только одному продукту.
# В уроке должна быть базовая информация: название, ссылка на видео. (1 балл)
class Lesson(models.Model):
    """ Урок """

    product_id = models.ForeignKey(Product, related_name="lesson", on_delete=models.CASCADE, verbose_name="Урок")
    name = models.CharField(max_length=200, unique=True, verbose_name="Название урока")
    url_video = models.URLField(max_length=200, verbose_name="Ссылка на видео")

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['id']

    def __str__(self):
        return f"{self.id}-lesson: {self.name[:20]}-{self.product_id}"


# Создать сущность группы. По каждому продукту есть несколько групп пользователей, которые занимаются в этом продукте.
# Минимальное и максимальное количество юзеров в группе задается внутри продукта. Группа содержит следующую информацию:
# ученики, которые состоят в группе, название группы, принадлежность группы к продукту (2 балла)

class Group(models.Model):
    """ Учебная группа """

    product_id = models.ForeignKey(Product, related_name="group", on_delete=models.CASCADE, verbose_name="Группа")
    name = models.CharField(max_length=15, unique=True, verbose_name="Название группы")
    min_quantity = models.IntegerField(blank=True, null=True, verbose_name="min кол.")
    max_quantity = models.IntegerField(blank=True, null=True, verbose_name="max кол.")
    students = models.ManyToManyField(User, through='StudentsInGroup')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['id']

    def save(self, *args, **kwargs):
        if Product.objects.filter(id=self.product_id.id).exists():
            product = Product.objects.get(id=self.product_id.id)
            self.min_quantity = product.min_quantity
            self.max_quantity = product.max_quantity
        super().save(*args, **kwargs)

    def fullness(self):
        """ Процент заполненности группы """
        num_st = self.get_users.all().count()
        percent = round(num_st * 100 / self.max_quantity, 2)
        return percent

    def __str__(self):
        return f"{self.id}- группа: {self.name} - {self.product_id}"


class StudentsInGroup(models.Model):
    """ Промежуточная модель для связи студентов с учебной группой """

    student = models.ForeignKey(User, related_name='get_group', to_field='username', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='get_users', to_field='name', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Состав группы'
        verbose_name_plural = 'Состав группы'
        ordering = ['id', 'group', 'student']

