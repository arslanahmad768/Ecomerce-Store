from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count,Min,Max,Avg
from django.db.models import Value,F,Func,ExpressionWrapper,DecimalField
from django.db.models.functions import Concat
from store.models import Product,OrderItem,Order,Customer,Collection
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db.models import Q,F
from django.db import transaction
from django.db import connection

# @transaction.atomic()
def say_hello(request):
    # query_set = Product.objects.filter(id__gt=1) 
    # print(query_set[1])
    # extract Data without Model 
    # with connection.cursor() as cursor:
    #     # cursor.execute("INSERT")
    #     cursor.callproc("get_customer",[1,2,'a'])
    
    #--- return Id and Title from Product model
    # query_set = Product.objects.raw("select id,title from store_product")
    #--- used raw query to get all records of Product
    # query_set = Product.objects.raw("select * from store_product")
    
    #-- Transaction used to store changes togther if one changes failed all changes roll back
    # .......code...
    # with transaction.atomic():      #RETURN A Context manager
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     orderitem = OrderItem()
    #     orderitem.order = order
    #     orderitem.quantity = 3
    #     orderitem.unit_price = 100.0
    #     orderitem.product_id = 5
    #     orderitem.save()

    #-- DELETE Method
    # collection  = Collection.objects.get(pk=10)
    # collection.delete()
    # Collection.objects.filter(id__gt=5).delete()
   
    #--- Update Data
    # collection = Collection.objects.get(pk=1)
    # collection.featured_product = None
   
    # collection.save()
    #-- Bad Approach To update Data
    # Collection.objects.filter(pk=11).update(featured_product=None)
    # collection = Collection(pk=1)
    # collection.featured_product = None
    # collection.save()

    # Strong Intellisense and Autochange field name when column name changed.    
    # collection = Collection()
    # collection.title="Python"
    # collection.featured_product = Product(id=1)
    # collection.save()
    #-- Bad Approach for Insert Bcz when we update field this is not change
    # Collection.objects.create(title="Django",featured_product_id=1)
    # collection = Collection(title="videoGames")

    # Queryset Cache
   #  query_set = Product.objects.filter(id__lt=8)
   #  result = list(query_set)
   #  s = query_set[0]

    #-- Custom Manager
    # result = TaggedItem.objects.get_tag_for(Product,1)
    # query_set = Product.objects.filter(id__lt=10)
    # list(query_set)
    # query_set[0]


    #-- Get tag for specific Product
    # content_type = ContentType.objects.get_for_model(Product)
    # result = TaggedItem.objects \
    #     .select_related("tag") \
    #     .filter(
    #         content_type = content_type,
    #         object_id=1
    # )
   
    #-- Perform Expression on Unit_Price
    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8,output_field=DecimalField())
    # result = Product.objects.annotate(discount_price=discounted_price)
    # discounted_price = ExpressionWrapper(F('unit_price') * 0.12,output_field=DecimalField())
    # result = Product.objects.annotate(
    #     discount_price=discounted_price
    # )
    #-- Get Count of order of every Customer
   #  result = Customer.objects.annotate(orders_count=Count("order"))
   #  print(result)

    #----- Add django Cancat function
    # result = Customer.objects.annotate(
    #         full_name = Concat(
    #         F('first_name'),Value(' '),F('last_name')
    #     )
    #     )

    #-- Add func class to perform cancatination
    # result = Customer.objects.annotate(full_name=Func(
    #   F("first_name"),Value(" "),F("last_name"),function="CONCAT"  
    # ))


    #-- Add new attributes in Product Table with id of product Table
    # result = Product.objects.annotate(new_id=F("id"))
   
    #-- Perform calculation on product Table 
   #  result = Product.objects.filter(collection__id=3).aggregate(count=Count("id"),min_price=Min("unit_price"))
   #  print(result)
    # result = Product.objects.filter(collection__id=1).aggregate(count=Count('id))
    # result = Product.objects.aggregate(count=Count("id"),min_price=Min("unit_price"))

    #-- Return last 5 order with customer,orderitem and Product.
    # query_set = Order.objects.select_related("customer").prefetch_related("orderitem_set__product").order_by("-placed_at")[:5]
    #-- return promotion,collection and Product fields --prefetch_related("n")
    # query_set = Product.objects.prefetch_related("promotions").select_related("collection").all()
    # query_set = Product.objects.select_related("collection__someOtherFields").all()
    #-- Return Preload Product and Collection Table --select_relation(1)
    # query_set = Product.objects.prefetch_related('orderitem_set').all()
    # print(query_set)
    # for product in query_set:
    #     print(product.orderitem.payment_status)
    #-- Return all Product fields rather than Description field it's not good approach bcz 
       # if you use in template it generate lot of queries
    # query_set = Product.objects.defer("description")
    #-- Return Instance of Model class with only title and ID fields
    #-- values is better than only field bcz it execute multiple Queries  
    # query_set = Product.objects.only("title","id")
    
    # query_set = Product.objects.filter(id__in=OrderItem.objects.values("product_id")).order_by("title")
    # ---- return product that have been ordered
    # query_Set = orderitem.objects.filter('product_it').distinct()
    #-- return id,title and colllection__id column with bunch of  tuples datatype
    # query_set = Product.objects.values_list("id","title","collection__id")    
    #-- return id,title and colllection__id column with dict datatype not an object instance
    # query_set = Product.objects.values("id","title","collection__id")

    #----Slicing Products: 5,6,7,8,9
    # query_set = Product.objects.all()[5:10]
    # Products: 1,2,3,4,5
    # query_set = Product.objects.all()[:5]

    # DSC and Return First Object 
    # product = Product.objects.latest('title')
    # ASC and Return First Object 
    # product = Product.objects.earliest('title')
    # Return First Object
    # product = Product.objects.filter(collection__id=5)[0]
    # Filter and sorting by unit Price and return queryset
    # query_set = Product.objects.filter(collection__id=5).order_by("unit_price")
    # Product in ASC by unitPrice and Descending in title and reverse alter the Work Flow 
    # query_set = Product.objects.order_by("unit_price","-title").reverse() 
    # Product in DSC by title 
    # query_set = Product.objects.order_by("-title") 
    # Product in ASC by title 
    # query_set = Product.objects.order_by("title") 

    # Products: inventory = unit_price
    # we can compare integer value with string value using F class
    # query_set = Product.objects.filter(inventory=F('collection__id'))
    # query_set = Product.objects.filter(inventory=F('unit_price'))
    

    # print(query_set)
    # Products: Invenory <10 AND price < 20
    # query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # Invenory <10 AND and NOT price < 20
    # query_set = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20)) 
    # Invenory <10 OR price < 20
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # Invenory <10 AND price < 20
    # query_set = Product.objects.filter(Q(inventory__lt=10),  Q(unit_price__lt=20))
   #  orderData = OrderItem.objects.values('product_id').distinct()
   #  for order in orderData:
   #      print(order)    
   #  query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by("title")
   #  for q in query_set:
   #     print(q.id)
    # query_set = Product.objects.values_list("id","title")  #return Tuples with both fields
    # query_set = Product.objects.values("id","title","collection__title") #return Dictory and only Id and title
    # 5,6,7,8,9
    # query_set = Product.objects.all()[5:10]
    # 1,2,3,4,5
    # query_set = Product.objects.all()[:5]
    # query_set = Product.objects.order_by('unit_price')[0] // return First Value
    # product = Product.objects.latest('title') // Dsc and return first Value
    # product = Product.objects.earliest('title') // Asc and return first Value
    # query_set = Product.objects.filter(collection__id=6).order_by("unit_price")
    # query_set = Product.objects.filter(inventory=F('collection_id'))
    # inventry > 20 or unitprice<10
   
    # ------  Perform ~Not Operator in SQL 
    # query_set = Product.objects.filter(Q(inventory__gt=20) | ~Q(unit_price__lt=10))
    # query_set = Product.objects.filter(Q(inventory__gt=20),Q(unit_price__lt=10))
    # query_set = Product.objects.filter(collection__title="Pets")  inner join
    # product = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
   
    # ------ Return products that inventory < 10 and unit_price < 20
    # product = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # products = Product.objects.filter(inventory__lt=10,unit_price__lt=20) 
 
    #---- return products that description field have NUll Value
    # query_set = Product.objects.filter(description__isnull=True)
    # query_set = Product.objects.filter(last_update__year=2021) 
    # query_set = Product.objects.filter(title__icontains="Pets")
    # query_set = Product.objects.filter(title__contains="Pets")
    # ----- reurn products that belongs to this collection title
    # query_set = Product.objects.filter(collection__title="Pets")
    #----- return query_Set than have range btw
    # query_set = Product.objects.filter(unit_price__range=(20,22))
    #------ return value that greater than 20
    # Products = Product.objects.filter(unit_price__gt=20)
    
    #-------- Return Boolean Value
    # exist = Product.objects.filter(pk=1).exists()
    
    # product = Product.objects.filter(unit_price=20.00)
    # if len(product) > 0:
    #     for d in product:
    #         print(d)
    # else:
    #     print("No Record Exist")

    # Return record or None
   #  query_set = Product.objects.filter(pk=1,collection=1)
   #  for query in query_set:
   #      print(query.id)

    # Raise error if not Found we handle this by exception Handling 
    # try:
    #     query_set = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     print("Record Does not exist")

    return render(request, 'hello.html')
