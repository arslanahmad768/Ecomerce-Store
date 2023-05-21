from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet,GenericViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status
from .filters import ProductFilter
from .pagination import DefaultPagination

from .permissions import isAdminOrReadOnly,FullDjangoModelPermission,CanViewHistoryPermission
from .models import *
from .serializers import *
# Create your views here.
class ReviewSet(ModelViewSet):
    # we can't access url parameter directly on this queryset that's why we override queryset
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
 
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['title','description']
    ordering_fields = ['unit_price','last_update']
    permission_classes = [isAdminOrReadOnly]
#-----  Custom filter
    filterset_class = ProductFilter
    # Custom Pagination
    # pagination_class = DefaultPagination
#------- define filter fields
    # filterset_fields = ['collection_id','unit_price']

# ------ Bad Aproach for filtering data

    # def get_queryset(self):
    #     query_set = Product.objects.all()

#------- we use query_params to receive query_parameter
#------- get return key value otherwise retorn None

    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         query_set = query_set.filter(collection_id=collection_id)
    #     return query_set

    def get_serializer_context(self):
        return {'request':self.request} 
    # kwargs is a dictionary that have url paraemeter
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'product does not deleted because \
                                it asoociated with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)

    def delete(self,request,pk):
        product = get_object_or_404(Product,pk=pk)
        query_Set = product.orderitem_set.all()
        print("count is",query_Set.count())
        # return ordetitem according to product instance
        if product.orderitem_set.count() > 0:
            return Response({'error':'product does not deleted because \
                                it asoociated with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response("Deleted")

# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer

    #------- if you have complex logic to return querysey
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()

    #------ if you have complex logic to return serializer    
    # def get_serializer(self, *args, **kwargs):
    #     return ProductSerializer
    
    # def get_serializer_context(self):
    #     return {'request':self.request}
#--- base class APIView
#--- Repeat different logic that's why we move towrds concrete classes 
#--- that actually a combination of mixins
# class ProductList(APIView):
#     def get(self,request):
#         query_set = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(query_set,many=True, context= {'request':request})
#         return Response(serializer.data)

#     def post(self,request): 
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status = status.HTTP_201_CREATED)

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    # --- if you want to override the pk url parameter
    # lookup_field = 'id'


# class ProductDetail(APIView):
#     def get(self,reuqest,id):
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     def put(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProductSerializer(product ,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         query_Set = product.orderitem_set.all()
#         print("count is",query_Set.count())
#         # return ordetitem according to product instance
#         if product.orderitem_set.count() > 0:
#             return Response({'error':'product does not deleted because \
#                               it asoociated with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response("Deleted")

# @api_view(['GET','POST'])
# def product_list(request):
#     #  Serializing
#     if request.method == 'GET':
#         query_set = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(query_set,many=True, context= {'request':request})
#         return Response(serializer.data)
#     # deserializing
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # serializer.validated_data
#         return Response(serializer.data)
        # ------ bad approach
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response("Ok")
        # else:
        #     return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def product_detail(request,id):
#     # to handle exception we use raise_exception instead of try block
#     product = get_object_or_404(Product,pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product ,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         query_Set = product.orderitem_set.all()
#         print("count is",query_Set.count())
#         # return ordetitem according to product instance
#         if product.orderitem_set.count() > 0:
#             return Response({'error':'product does not deleted because \
#                               it asoociated with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response("Deleted")

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializer
    permission_classes = [isAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count()>0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request, pk):
    #     collection = get_object_or_404( Collection,pk = pk)
    #     if collection.product_set.count() > 0:
    #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response("Deleted")
    
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('product')).all()
#     serializer_class = CollectionSerializer

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('product')).all()
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404( Collection,pk = pk)
#         if collection.product_set.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response("Deleted")

# @api_view(['GET','POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         # alternative solution of method serializer to add new field
#         collection = Collection.objects.annotate(products_count=Count('product')).all()
#         # collection = Collection.objects.all()
#         serializer = CollectionSerializer(collection,many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# @api_view(['GET','PUT','DELETE'])
# def collection_detail(request,collection_id):
#     collection = get_object_or_404(
#         Collection.objects.annotate(products_count=Count('product')),
#         pk=collection_id)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection,request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.product_set.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response("Deleted")

# --- Custom ViewSet
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    # reverse relation we use prefetch related bcz it will many to one relation
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
        
    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(
            cart_id = self.kwargs['cart_pk']) \
            .select_related('product')
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
 
    # Apply permissions on different Action's
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
    @action(detail=True,permission_classes = [CanViewHistoryPermission])
    def history(self,request,pk):
        return Response("Ok")

    # custom action
    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        # request.user is set when we pass json token.
        print("request user is ",request.user.id)
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer,data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
class OrderViewSet(ModelViewSet):
    http_method_names = ['get','post','delete','patch','options','head']
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer( data=request.data,
            context={"user_id":self.request.user.id} )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer 

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id = Customer.objects.only('id').get(user_id = user.id)
        return Order.objects.filter(customer_id = customer_id)
        
