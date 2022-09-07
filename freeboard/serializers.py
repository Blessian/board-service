from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['weather']                      # 사용자가 값을 넣지 못함
        extra_kwargs = {
            'password': {'write_only': True},               # 값이 출력되지 않음
        }


class ArticlePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'password']
        extra_kwargs = {
            'password': {'write_only': True},               # 값이 출력되지 않음
        }
