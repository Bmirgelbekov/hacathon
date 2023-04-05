from rest_framework.routers import DefaultRouter
from .views import AppartmentViewSet #, CommentViewSet

router = DefaultRouter()
router.register('post', AppartmentViewSet, 'posts')
#router.register('comment', CommentViewSet, 'comments')


urlpatterns = router.urls