from rest_framework import serializers
from decimal import Decimal
from .models import Product,Collection,Review

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