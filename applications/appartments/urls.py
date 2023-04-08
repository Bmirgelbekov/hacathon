from rest_framework.routers import DefaultRouter
from .views import AppartmentViewSet,FavoritesView, ApartamentsViewCreate  #, CommentViewSet

router = DefaultRouter()
router.register('post', AppartmentViewSet, 'posts'),
router.register('post-create', ApartamentsViewCreate, 'posts'),

router.register(r'favorites_d', FavoritesView, basename='favorites_ff')

urlpatterns = router.urls