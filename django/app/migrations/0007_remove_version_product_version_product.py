from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_version'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='product',
        ),
        migrations.AddField(
            model_name='version',
            name='product',
            field=models.ManyToManyField(to='app.product', verbose_name='Продукты'),
        ),
    ]
