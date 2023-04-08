from rest_framework.routers import DefaultRouter
from .views import AppartmentViewSet,FavoritesViewSet   #, CommentViewSet

router = DefaultRouter()
router.register('post', AppartmentViewSet, 'posts'),

router.register(r'favorites', FavoritesViewSet, basename='favorites')



# router.register('comment', CommentViewSet, 'comments')
urlpatterns = router.urls