from urllib.request import urlopen
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from common import get_secret
from .models import Article
from .serializers import ArticleSerializer, ArticlePasswordSerializer
from argon2 import PasswordHasher, exceptions
import json


# Create your views here.
class ArticlePagination(CursorPagination):
    page_size = 20
    ordering = '-id'


class ArticleViewSet(viewsets.ModelViewSet):
    """
    urls :
        - GET   /freeboard/articles/                        리스트
        - POST  /freeboard/articles/                        생성(title, content, password 필요)
        - GET   /freeboard/articles/<int:id>                상세
        - PUT   /freeboard/articles/<int:id>                수정(title, content, password 필요)
        - POST  /freeboard/articles/<int:id>/delete/        삭제(password 필요)

    title: 글제목, 제목은 20자 이하여야 합니다
    content: 글내용, 글 내용은 200자 이하로 작성해주세요
    password: 비밀번호, 비밀번호는 6 자 이상이어야 하고, 반드시 숫자가 1개 이상 포함 되어야 합니다
    """
    queryset = Article.objects.all()
    pagination_class = ArticlePagination

    def get_serializer_class(self):
        if self.action in ('list', 'create', 'update', 'partial_update', 'retrieve'):
            return ArticleSerializer
        elif self.action in 'delete':
            return ArticlePasswordSerializer

    def create(self, request, *args, **kwargs):
        """
        글 등록

        작성 규칙을 준수해야 작성 가능
        비밀번호를 암호화 하여 저장
        현재 날씨 정보를 기록

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        password_hasher = PasswordHasher()

        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # raise_exception=True serializer가 오류를 리턴(이 옵션이 없으면 규격에 맞지 않는 값은 None 들어옴
            raw_password = serializer.validated_data['password']
            serializer.validated_data['password'] = password_hasher.hash(raw_password)
            
            # 날씨 정보 가져오기
            api_key = get_secret('API_KEY')
            url = 'http://api.weatherapi.com/v1/current.json?key=' + api_key + '&q=korea&aqi=yes'

            response_body = urlopen(url, timeout=60).read()
            data = json.loads(response_body)
            current_weather = data['current']['condition']['text']

            serializer.validated_data['weather'] = current_weather

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        글 수정

        비밀번호가 일치해야 수정 가능

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        password_hasher = PasswordHasher()

        article_instance = self.get_object()
        serializer = self.get_serializer(article_instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            raw_password = serializer.validated_data['password']
            try:
                if password_hasher.verify(article_instance.password, raw_password):
                    serializer.validated_data['password'] = article_instance.password
                    self.perform_update(serializer)
                    return Response(serializer.data)

            except exceptions.VerifyMismatchError:  # 비밀번호가 일치하지 않음
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

            except exceptions.VerificationError:    # 비밀번호가 일치하지 않음
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

            except KeyError:
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)    # 글 작성 규칙에 맞지 않음

    def destroy(self, request, *args, **kwargs):
        """
        비밀번호 없이 삭제할 수 없도록 막아놓음
        """
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], name='delete')
    def delete(self, request, **kwargs):
        """
        비밀번호로 삭제
        
        비밀번호를 post 방식으로 입력 받음
        비밀번호로 검증 후 삭제

        :param request: request
        :param kwargs: pk
        :return: 
            - 성공: HTTP_204_NO_CONTENT
            - 실패: HTTP_400_BAD_REQUEST
        """
        article_instance = self.get_object()
        serializer = ArticlePasswordSerializer(data={'id': kwargs['pk'], 'password': request.data['password']})
        if serializer.is_valid(raise_exception=True):
            password_hasher = PasswordHasher()

            try:
                if password_hasher.verify(article_instance.password, serializer.validated_data['password']):
                    self.perform_destroy(article_instance)
                    return Response(status=status.HTTP_204_NO_CONTENT)
            except exceptions.VerifyMismatchError:  # 비밀번호가 일치하지 않음
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

            except exceptions.VerificationError:    # 비밀번호가 일치하지 않음
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

            except KeyError:
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
