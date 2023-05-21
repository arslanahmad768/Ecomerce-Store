from django.urls import path,include
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from . import views
from pprint import pprint


router = routers.DefaultRouter()
# router = SimpleRouter()
# provide two additional feature you can api endpoint
# if we pass 127.0.0.1:8000/store/product.json from client side we see data in json format
router.register('products',views.ProductViewSet,basename='product')
router.register('collections',views.CollectionViewSet)
router.register('cart',views.CartViewSet)
router.register('customer',views.CustomerViewSet)
router.register('orders',views.OrderViewSet,basename='orders')
# router.register('cartitem',views.CartItemViewSet)

cartItem_router = routers.NestedDefaultRouter(router,'cart',lookup='cart')
cartItem_router.register('item',views.CartItemViewSet,basename='cart-item')

# product_router = routers.NestedDefaultRouter(router,'products',lookup='product')
# product_router.register('reviews',views.ReviewSet,basename='product-reviews')
# router = DefaultRouter()

# router.register('products',views.ProductViewSet)
# router.register('collections',views.CollectionViewSet)
#--- pretty printer used for printing complex data structures
#  pprint(router.urls)
# ---- append in list of url routers
urlpatterns = router.urls + cartItem_router.urls
# urlpatterns = router.urls + product_router.urls
# urlpatterns = [
#     path('',include(router.urls)),
    # as_view method  convert class based view to regular function based view
    # path('products/',views.ProductList.as_view(),name='product_list'),
    # path('product/<int:pk>/',views.ProductDetail.as_view(),name='product_list'),
    # path('products/',views.product_list,name='product_list'),
    # path('products/<int:id>/',views.product_detail,name='product_list'),
    # path('collections/',views.CollectionList.as_view(),name='collection-list'),
    # path('collections/',views.collection_list,name='collection-list'),
    # path('collection/<int:collection_id>/',views.collection_detail,name='collection-detail'),
    # path('collection/<int:pk>/',views.CollectionDetail.as_view(),name='collection-detail'),

# ]