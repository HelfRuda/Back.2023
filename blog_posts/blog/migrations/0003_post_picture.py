# Generated by Django 4.1.6 on 2023-05-12 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='picture',
            field=models.ImageField(null=True, upload_to='', verbose_name='Картинка поста'),
        ),
    ]
