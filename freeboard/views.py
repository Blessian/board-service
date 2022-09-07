from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from .models import Article
from .serializers import ArticleSerializer
from argon2 import PasswordHasher


# Create your views here.
class ArticlePagination(CursorPagination):
    page_size = 20
    ordering = '-id'


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination

    def create(self, request, *args, **kwargs):
        password_hasher = PasswordHasher()

        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # raise_exception=True serializer가 오류를 리턴(이 옵션이 없으면 규격에 맞지 않는 값은 None이 되어 들어옴
            raw_password = serializer.validated_data['password']
            serializer.validated_data['password'] = password_hasher.hash(raw_password)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
