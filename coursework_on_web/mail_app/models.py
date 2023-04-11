from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=50, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    comments = models.CharField(max_length=500, **NULLABLE, verbose_name='Комментарии')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.full_name


class Message(models.Model):
    topic = models.CharField(max_length=150, verbose_name='Тема')
    body = models.CharField(max_length=500, verbose_name='Текст сообщения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.topic


class Mailing(models.Model):
    DAILY = 'd'
    WEEKLY = 'w'
    MONTHLY = 'm'
    FREQUENCY_CHOICES = [
        (DAILY, 'Раз в день'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц')
    ]

    CREATED = 'c'
    STARTED = 's'
    FINISHED = 'f'
    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (FINISHED, 'Завершена')
    ]

    time = models.TimeField(verbose_name='Время рассылки')
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES, default=WEEKLY, verbose_name='Периодичность')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=CREATED, verbose_name='Статус рассылки')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ManyToManyField(Client)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                'set_status',
                'Can finish mailing'
            ),
        ]

    def __str__(self):
        return f'{str(self.id)}. Рассылка {self.owner.full_name} в {str(self.time)} - {self.status}.'


class MailingAttempt(models.Model):
    SUCCESS = 's'
    FAIL = 'f'
    STATUS_CHOICES = [
        (SUCCESS, 'Попытка успешна'),
        (FAIL, 'Попытка не удалась')
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=FAIL, verbose_name='Статус попытки')
    answer = models.CharField(max_length=300, **NULLABLE, verbose_name='Ответ почтового сервера')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        mail_attempt_str = f'{str(self.id)}. Попытка рассылки {str(self.time)} - {self.status}.'
        if self.answer:
            mail_attempt_str += self.answer
        return mail_attempt_str
