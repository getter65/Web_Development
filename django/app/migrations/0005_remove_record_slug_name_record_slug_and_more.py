from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_record'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='slug_name',
        ),
        migrations.AddField(
            model_name='record',
            name='slug',
            field=models.CharField(default=1, max_length=200, unique=True, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='record',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='Количество просмотров'),
        ),
    ]
