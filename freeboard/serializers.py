from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}           # 값이 출력되지 않음


class ArticlePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'password']
        extra_kwargs = {'password': {'write_only': True}}
