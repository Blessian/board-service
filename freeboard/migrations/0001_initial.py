# Generated by Django 4.1 on 2022-09-06 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='제목은 20자 이하여야 합니다', max_length=20)),
                ('content', models.TextField(help_text='글 내용은 200자 이하로 작성해주세요', max_length=200)),
                ('password', models.CharField(help_text='비밀번호는 6 자 이상이어야 하고, 숫자 1 개 이상 반드시 포함 되어야 합니다', max_length=128)),
            ],
        ),
    ]