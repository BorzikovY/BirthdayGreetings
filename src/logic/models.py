from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from logic.validators import validate_full_name
from logic.managers import UserManager


class User(AbstractUser):
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
        blank=True,
    )

    def __str__(self):
        return f"{self.subscriber} хочет поздравить {self.birthday_person}!"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("subscriber", "birthday_person")
