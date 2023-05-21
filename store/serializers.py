from rest_framework import serializers
from .signals import order_created
from django.db import transaction
from decimal import Decimal
from .models import *

class CollectionSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    
    class Meta:
        model = Collection
        fields = ['id','title','products_count']
    # read_only=True bcz we don't want to create or updatge
    products_count = serializers.IntegerField(read_only=True) 
    
    #----- add field in serializer
    # products_count = serializers.SerializerMethodField(method_name='calculate_products_count')
    # def calculate_products_count(self,collection):
    #     return collection.product_set.count() 

class ProductSerializer(serializers.ModelSerializer):
    # rename model field
    price = serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')

    class Meta:
        model = Product
        fields = ['id','title','description','slug','price','price_with_tax','inventory','collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    # ------- Custom function
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # ---- primary key
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )
    # ---- string 
    # collection = serializers.StringRelatedField()
    #----- nested object
    # collection = CollectionSerializer()
    # ---- hyperlink
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name='collection-detail'
    # )
    def create(self, validated_data):
        # unpack dictionary
        product = Product(**validated_data)
        product.other = 1
        product.save()
        return product
    
    def update(self, instance, validated_data):
        instance.unit_price = validated_data.get('unit_price')
        instance.save()
        return instance

    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)

    # override validate method to perform custom validation
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError
    #     return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','name','description','date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id,**validated_data)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']
    
    def get_total_price(self,cartItem:CartItem):
        print("unit_price is ",cartItem.product.unit_price)
        return cartItem.product.unit_price * cartItem.quantity 
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    items = CartItemSerializer(many = True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id','items','total_price']

    def get_total_price(self,cart:Cart):
        return sum([item.quantity * item.product.unit_price  for item in cart.items.all() ])



# class ProductsSerializer(serializers.ModelSerializer):
#     total_price = serializers.SerializerMethodField(method_name='calculate_total_price')
#     class Meta:
#         model = Product
#         fields =  fields = ['id','title','description','slug','unit_price','total_price','inventory','collection']

#     def calculate_total_price(self,obj):

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk = value).exists():
            return serializers.ValidationError("No Product with the given ID was found")
        return value
    
    def save(self, **kwargs):
        # dictionary Value
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cartItem = CartItem.objects.get(cart_id = cart_id, product_id = product_id)
            cartItem.quantity = quantity
            self.instance = cartItem
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id,**self.validated_data)
            return self.instance
    
    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']   

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Customer
        # user_id attribute is created dynamically at run time
        fields = ['id','user_id','phone','birth_date','membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','unit_price','quantity']
    # def get_product(self,obj):
    #     product = obj.product
    #     return SimpleProductSerializer(instance=product).data

class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id','placed_at','customer_id','payment_status','orderitem_set']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("No record with this cart ID")
        elif not CartItem.objects.filter(cart=cart_id).exists():
            raise serializers.ValidationError("No items with this cart")
        return cart_id

    def save(self,**kwargs):
        with transaction.atomic():
            # get_or_create return tuple 
            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cartitem = CartItem.objects.filter(cart=self.validated_data['cart_id'])
            orderitems = [
                OrderItem (
                    order = order,
                    product = item.product,
                    quantity = item.quantity,
                    unit_price = item.product.unit_price
                ) 
                for item in cartitem
            ]
            OrderItem.objects.bulk_create(orderitems)
            Cart.objects.filter(pk=self.validated_data['cart_id']).delete()
            
            order_created.send_robust(self.__class__,order=order)
            return order
