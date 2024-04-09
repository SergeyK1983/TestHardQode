import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StudentsToProduct
from .services import assign_student_to_group

logger = logging.getLogger(__name__)


@receiver(post_save, sender=StudentsToProduct)
def add_student_to_group(sender, created, **kwargs):
    if created:
        if assign_student_to_group(StudentsToProduct.objects.last()):
            logger.info("Студент добавлен в группу!")
        else:
            logger.info("Студент в группу не добавлен!")

