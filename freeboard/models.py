from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, help_text='제목은 20자 이하여야 합니다')
    content = models.TextField(max_length=200, help_text='글 내용은 200자 이하로 작성해주세요')
    password_regex = RegexValidator(regex=r'(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$')
    password = models.CharField(
        validators=[password_regex],
        max_length=128,
        help_text='비밀번호는 6 자 이상이어야 하고, 숫자 1 개 이상 반드시 포함 되어야 합니다'
    )

    REQUIRED_FIELDS = ['title', 'content', 'password']
