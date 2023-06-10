from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField('Тег', max_length=100)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    description = models.TextField('Описание категории', max_length=1000)
    picture = models.ImageField('Картинка категории', upload_to='cat_img', default='cat_img/categ.png')

    def __str__(self):
        return f'{self.name}, {self.description}'
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    tags = models.ManyToManyField(Tag, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField('Заголовок поста', max_length=100)
    description = models.TextField('Текст поста')
    picture = models.ImageField('Картинка поста', upload_to='image/%M', default='cat_img/categ.png')
    author = models.CharField('Имя автора', max_length=100)
    date = models.DateField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return f'{self.title}, {self.date}' 

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class Comments(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    text_comment = models.TextField('Текст комментария', max_length=2000)
    post = models.ForeignKey(Post, verbose_name = 'Публикация', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}, {self.post}' 

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'