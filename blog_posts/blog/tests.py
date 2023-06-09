from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Category, Post, Comments, Tag
import unittest
from blog.spamcheck import SpamCheck

class SpamCheckTest(unittest.TestCase):
    def test_is_spam(self):
        spam_check = SpamCheck()
        # Проверка спам-слова
        result = spam_check.is_spam("Это сообщение содержит слово виагра")
        self.assertTrue(result)
        print("Результат проверки на спам:", result)

        # Проверка отсутствия спам-слова
        result = spam_check.is_spam("Это сообщение окей")
        self.assertFalse(result)
        print("Результат проверки на спам:", result)

class AddCommentsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Тестовая категория')
        self.post = Post.objects.create(title='Тестовый пост', description='Тестовое описание', category=self.category, author='Тестовый автор')

    def test_add_comment(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('add_comments', kwargs={'category_id': self.category.id, 'pk': self.post.id})
        response = self.client.post(url, {'text_comment': 'Тестовый коммент'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comments.objects.count(), 1)
        comment = Comments.objects.first()
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.text_comment, 'Тестовый коммент')

        print('Тест комментария успешно пройден')

    def test_add_spam_comment(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('add_comments', kwargs={'category_id': self.category.id, 'pk': self.post.id})
        response = self.client.post(url, {'text_comment': 'Спам текст'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comments.objects.count(), 0)
        self.assertContains(response, 'Ваш комментарий содержит спам и не может быть опубликован.')

        print('Тест комментария со спамом успешно пройден')


class AddPostViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Тестовая категория')
        self.tag1 = Tag.objects.create(name='Tag 1')
        self.tag2 = Tag.objects.create(name='Tag 2')
        self.admin_user = User.objects.create_user(username='adminuser', password='testpass')
        self.admin_user.groups.add(Group.objects.create(name='Admins'))

    def tearDown(self):
        self.admin_user.delete()

    def test_add_post(self):
        url = reverse('add_post')
        self.client.login(username='adminuser', password='testpass')

        form_data = {
            'title': 'Тестовый пост',
            'description': 'Тестовое описание',
            'category': self.category.id,
            'tags': [self.tag1.id, self.tag2.id],
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        print('Тест создания поста админом успешно пройден')

    def test_add_post_not_admin(self):
        regular_user = User.objects.create_user(username='regularuser', password='testpass')
        self.client.login(username='regularuser', password='testpass')
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 403)

        regular_user.delete()

        print('Тест создания поста не админом успешно пройден')


class EditPostViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Тестовая категория')
        self.tag1 = Tag.objects.create(name='Tag 1')
        self.tag2 = Tag.objects.create(name='Tag 2')
        self.admin_user = User.objects.create_user(username='adminuser', password='testpass')
        admin_group = Group.objects.create(name='Admins')
        self.admin_user.groups.add(admin_group)
        self.post = Post.objects.create(
            title='Тестовый пост',
            description='Тестовое описание',
            category=self.category,
            author=self.admin_user,
        )
        self.post.tags.add(self.tag1, self.tag2)

    def tearDown(self):
        self.post.delete()
        self.admin_user.delete()

    def test_edit_post(self):
        url = reverse('edit_post', args=[self.post.pk])
        self.client.login(username='adminuser', password='testpass')

        form_data = {
            'title': 'Новый заголовок',
            'description': 'Новое описание',
            'category': self.category.id,
            'tags': [self.tag2.id],
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Новый заголовок')
        self.assertEqual(self.post.description, 'Новое описание')
        self.assertEqual(list(self.post.tags.all()), [self.tag2])

        print('Тест редактирования поста админом успешно пройден')

    def test_edit_post_not_admin(self):
        regular_user = User.objects.create_user(username='regularuser', password='testpass')
        self.client.login(username='regularuser', password='testpass')
        response = self.client.get(reverse('edit_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

        regular_user.delete()

        print('Тест редактирования поста не админом успешно пройден')


class DeletePostViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Тестовая категория')
        self.tag1 = Tag.objects.create(name='Tag 1')
        self.tag2 = Tag.objects.create(name='Tag 2')
        self.admin_user = User.objects.create_user(username='adminuser', password='testpass')
        admin_group = Group.objects.create(name='Admins')
        self.admin_user.groups.add(admin_group)
        self.post = Post.objects.create(
            title='Тестовый пост',
            description='Тестовое описание',
            category=self.category,
            author=self.admin_user,
        )
        self.post.tags.add(self.tag1, self.tag2)

    def tearDown(self):
        self.post.delete()
        self.admin_user.delete()

    def test_delete_post(self):
        url = reverse('delete_post', args=[self.post.pk])
        self.client.login(username='adminuser', password='testpass')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

        print('Тест удаления поста админом успешно пройден')

    def test_delete_post_not_admin(self):
        regular_user = User.objects.create_user(username='regularuser', password='testpass')
        self.client.login(username='regularuser', password='testpass')
        response = self.client.post(reverse('delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)

        regular_user.delete()

        print('Тест удаления поста не админом успешно пройден')