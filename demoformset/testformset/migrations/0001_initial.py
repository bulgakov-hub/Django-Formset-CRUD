# Generated by Django 3.1.2 on 2020-10-12 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название')),
                ('description', models.CharField(max_length=300, verbose_name='Описание')),
                ('quantity_q', models.SmallIntegerField(default=14, verbose_name='Количество вопросов')),
                ('quantity_a', models.SmallIntegerField(default=4, verbose_name='Количество ответов')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
                'ordering': ['-date'],
            },
        ),
    ]