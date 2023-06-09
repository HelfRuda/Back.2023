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

if name == 'main':
    unittest.main()