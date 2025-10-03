from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from users.models import CustomUser


class Recipient(models.Model):
    email = models.EmailField(unique=True, max_length=100)
    full_name = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'recipient'
        verbose_name_plural = 'recipients'
        ordering = ['email']


class Message(models.Model):
    subject = models.CharField(max_length=100, blank=True)
    letter = models.TextField()
    owner = models.ForeignKey(CustomUser, verbose_name='владелец сообщения',
                              blank=True, null=True,
                              on_delete=models.SET_NULL)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ['subject']


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена'),
    ]

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Создана')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)
    owner = models.ForeignKey(CustomUser, verbose_name='владелец рассылки', blank=True, null=True,
                              on_delete=models.SET_NULL)

    def __str__(self):
        return f'Рассылка #{self.id}'

    def update_status(self):
        now = timezone.now()
        if now >= self.end_datetime:
            self.status = 'Завершена'
        elif now >= self.start_datetime:
            self.status = 'Запущена'
        else:
            self.status = 'Создана'
        self.save()

    def send(self):
        subject = self.message.subject
        letter = self.message.letter

        for recipient in self.recipients.all():
            try:
                from django.conf import settings
                response = send_mail(
                    subject,
                    letter,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient.email],
                    fail_silently=False,
                )
                SendAttempt.objects.create(
                    mailing=self,
                    status='Успешно',
                    server_response=f"Отправлено: {response}"
                )
            except Exception as e:
                SendAttempt.objects.create(
                    mailing=self,
                    status='Не успешно',
                    server_response=str(e)
                )

    class Meta:
        verbose_name = 'mailing'
        verbose_name_plural = 'mailings'
        ordering = ['id']


class SendAttempt(models.Model):
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ]

    attempt_datetime = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, related_name='send_attempts')

    def __str__(self):
        return f"Попытка для рассылки #{self.mailing.id} — {self.status} ({self.attempt_datetime})"

    class Meta:
        verbose_name = 'attempt'
        verbose_name_plural = 'attempts'
        ordering = ['status']