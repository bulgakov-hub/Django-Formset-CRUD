from django.db import models
from datetime import datetime


class TestBox(models.Model):
    """Тесты"""

    name = models.CharField('Название', max_length=30)
    description = models.CharField('Описание', max_length=300)
    date = models.DateTimeField('Дата создания', auto_now_add=True)

    # Параметры теста
    quantity_q = models.SmallIntegerField('Количество вопросов', default=14)
    quantity_a = models.SmallIntegerField('Количество ответов', default=4)

    class Meta:
        ordering = ['-date']
        verbose_name = ("Тест")
        verbose_name_plural = ("Тесты")


class QuestionTest(models.Model):
    """Вопросы теста"""

    question = models.CharField(max_length=2)
    test_box = models.ForeignKey(
        TestBox,
        on_delete=models.CASCADE,
        related_name='test_question')


class AnswerQuestion(models.Model):
    """Ответы на вопрос"""

    question = models.ForeignKey(
        QuestionTest,
        on_delete=models.CASCADE,
        related_name='question_answer')
    prefix_name = models.CharField('Обозначение', max_length=1)
    right = models.BooleanField(default=False)

    class Meta:
        ordering = ['prefix_name']
