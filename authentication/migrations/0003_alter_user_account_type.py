# Generated by Django 3.2 on 2021-05-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20210429_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_type',
            field=models.CharField(default='personal', max_length=50, verbose_name='Account Type'),
        ),
    ]
