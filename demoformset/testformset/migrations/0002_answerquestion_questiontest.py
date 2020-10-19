# Generated by Django 3.1.2 on 2020-10-13 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testformset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=2)),
                ('test_box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_question', to='testformset.testbox')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(max_length=1, verbose_name='Обозначение')),
                ('right', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answer', to='testformset.questiontest')),
            ],
            options={
                'ordering': ['prefix'],
            },
        ),
    ]