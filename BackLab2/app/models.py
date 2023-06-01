from django.db import models

class User(models.Model):

    first_name = models.TextField(
        blank=True,
        null=True,
        verbose_name='Имя',
    )
    last_name = models.TextField(
        blank=True,
        null=True,
        verbose_name='Фамилия',
    )
    email = models.TextField(
        blank=True,
        null=True,
        verbose_name='Почта',
    )

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Product(models.Model):

    name = models.TextField(
        blank=True,
        null=True,
        verbose_name='Название',
    )
    price = models.TextField(
        blank=True,
        null=True,
        verbose_name='Цена',
    )
    image = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Картинка'
    )

    class Meta:
        managed = False
        db_table = 'products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

