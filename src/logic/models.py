from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from apscheduler.triggers.cron import CronTrigger

from logic.validators import validate_full_name
from logic.managers import UserManager
from logic.notifications import scheduler, send_birthday_notification


class User(AbstractUser):
    """Модель пользователя."""
    first_name = None
    last_name = None
    username = None

    full_name = models.CharField(
        verbose_name="ФИО",
        max_length=150,
        help_text="""Требуется: Имя, Фамилия и Отчество написанные через пробел 
        только на русском языке. Можно использовать не более 150 символов.""",
        validators=[validate_full_name],
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )

    objects = UserManager()

    EMAIL_FIELD = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]


    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Subscription(models.Model):
    """Модель подписки на пользователя."""
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions_as_subscriber',
        verbose_name='Подписчик',
    )
    birthday_person = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions_as_birthday_person',
        verbose_name='Именинник',
    )
    notification_time = models.TimeField(
        verbose_name='Время напоминания',
        default=timezone.now,
    )
    cron_job_id = models.CharField(
        verbose_name="id задачи cron",
        max_length=255,
        null=True,
    )

    def __str__(self):
        return f"{self.subscriber} хочет поздравить {self.birthday_person}!"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("subscriber", "birthday_person")

    def save(self, *args, **kwargs):
        """
        Создает задачу cron и сохраняет данные.
        """
        if self.pk:
            if self.cron_job_id:
                scheduler.remove_job(self.cron_job_id)
            super().save(*args, **kwargs)
            self._create_cron_job()
        else:
            super().save(*args, **kwargs)
            self._create_cron_job()

    def delete(self, *args, **kwargs):
        """
        Удаляет задачу cron и удаляет запись.
        """
        if self.cron_job_id:
            scheduler.remove_job(self.cron_job_id)
        super().delete(*args, **kwargs)

    def _create_cron_job(self):
        """
        Создает задачу cron.
        """
        schedule = CronTrigger(
            month=self.birthday_person.birth_date.month,
            day=self.birthday_person.birth_date.day,
            hour=self.notification_time.hour,
            minute=self.notification_time.minute
        )

        scheduler.add_job(
            send_birthday_notification,
            args=[self.subscriber.email, self.birthday_person.full_name],
            trigger=schedule,
            id=f"birthday_notification_{self.pk}",
            replace_existing=True
        )


@receiver(post_save, sender=Subscription)
def update_cron_job(sender, instance, **kwargs):
    instance._create_cron_job()


@receiver(pre_delete, sender=Subscription)
def delete_cron_job(sender, instance, **kwargs):
    if instance.cron_job_id:
        scheduler.remove_job(instance.cron_job_id)
