from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import EmailField


class CustomUser(AbstractUser):
    email: EmailField = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('manager', 'Менеджер'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def is_manager(self):
        return self.role == 'manager'

    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return self.email