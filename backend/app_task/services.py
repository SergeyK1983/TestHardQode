from datetime import date
from .models import StudentsInGroup


# При получении доступа к продукту, распределять пользователя в группу. Если продукт ещё не начался,
# то можно пересобрать группы так, чтобы везде было примерно одинаковое количество участников.
# По-умолчанию алгоритм распределения должен работать заполняя до максимального значения
def assign_student_to_group(qs_stud_to_prod):
    """ Распределение студентов по группам по умолчанию """

    product = qs_stud_to_prod.product
    student = qs_stud_to_prod.student

    group_count = product.group.all().count()
    groups = product.group.all()

    for i in range(group_count):
        if groups[i].get_users.all().count() < product.min_quantity:
            StudentsInGroup.objects.create(student=student, group=groups[i])
            break

    if not StudentsInGroup.objects.filter(student=student).exists():
        for i in range(group_count):
            if groups[i].get_users.all().count() < product.max_quantity:
                StudentsInGroup.objects.create(student=student, group=groups[i])
                break
        else:
            # Можно обработать исключение
            print("Добавить невозможно, группы полностью заполнены")
            return False
    return True


