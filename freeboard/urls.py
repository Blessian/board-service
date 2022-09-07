from rest_framework import routers
from .views import ArticleViewSet

router = routers.SimpleRouter()
router.register('articles', ArticleViewSet, basename='articles')
urlpatterns = router.urls
