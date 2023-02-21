import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_category_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('slug_name', autoslug.fields.AutoSlugField(editable=False, populate_from='title', verbose_name='Slug')),
                ('content', models.CharField(max_length=500, verbose_name='Содержимое')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='records/', verbose_name='Превью')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('published', models.BooleanField(verbose_name='Признак публикации')),
                ('views_count', models.IntegerField(verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
            },
        ),
    ]
