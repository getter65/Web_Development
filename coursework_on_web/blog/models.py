from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):
    header = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.CharField(max_length=3000, verbose_name='Содержимое статьи')
    picture = models.ImageField(upload_to='post_pictures/', **NULLABLE, verbose_name='Изображение')
    views = models.PositiveIntegerField(verbose_name='Количество просмотров', **NULLABLE)
    published_on = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.header

