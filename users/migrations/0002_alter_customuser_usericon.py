# Generated by Django 3.2.3 on 2021-05-25 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='usericon',
            field=models.ImageField(blank=True, null=True, upload_to='tube/usericon/', verbose_name='ユーザーアイコン'),
        ),
    ]