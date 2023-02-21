from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_version_product_version_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='product',
        ),
        migrations.AddField(
            model_name='version',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.product', verbose_name='Продукт'),
        ),
    ]
