# Generated by Django 4.2.11 on 2024-04-30 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kasa', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Produkti', 'verbose_name_plural': 'Produktet'},
        ),
        migrations.AlterModelOptions(
            name='sale',
            options={'verbose_name': 'Shitja', 'verbose_name_plural': 'Shitjet'},
        ),
        migrations.AddField(
            model_name='sale',
            name='store',
            field=models.CharField(default='d1', max_length=2),
        ),
    ]
