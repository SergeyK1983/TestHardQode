import logging
from datetime import date
from .models import StudentsInGroup

logger = logging.getLogger(__name__)


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
            logger.info("Добавить невозможно, группы полностью заполнены")
            return False
    return True
# TODO доделать: защиту от двойных записей


def save_equal_quantity(users, groups, num, num_rem=0):
    """ Равное распределение по группам. Используется в rebuild_groups() """
    j = count = 0
    for i in range(users.count()-num_rem):
        StudentsInGroup.objects.create(student=users[i].student, group=groups[j])
        count += 1
        if count // num == 1:
            j += 1
            count = 0
    logger.info("Распределение завершено!")


def rebuild_groups(product_ins):
    """ Пересборка групп на равномерное количество учащихся. На вход подаётся экземпляр Продукта. """

    users = product_ins.get_users.all()
    groups = product_ins.group.all()

    if users.count() / groups.count() < product_ins.min_quantity:
        # Можно обработать исключение
        logger.info("Распределить не удалось. Число студентов в одной из групп меньше минимума")
        return False

    if date.today() == product_ins.start.date():
        # Можно обработать исключение
        logger.info("В этот день пересобирать группу уже поздно!")
        return False

    for i in range(groups.count()):
        StudentsInGroup.objects.filter(group=groups[i]).delete()

    if users.count() % groups.count() == 0:
        num = users.count() / groups.count()  # число в группе
        save_equal_quantity(users, groups, num)
        return True

    if users.count() % groups.count() != 0:
        num = users.count() // groups.count()  # число в группе
        num_rem = users.count() - num * groups.count()  # остаток
        save_equal_quantity(users, groups, num, num_rem)

        j = 0
        for i in range(users.count()-num_rem, users.count()):
            StudentsInGroup.objects.create(student=users[i].student, group=groups[j])
            j += 1
        return True
