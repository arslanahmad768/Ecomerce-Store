from django.contrib import admin,messages
from django.http import HttpRequest
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html,urlencode

from . import models

# class OrderItem(admin.ModelAdmin):
#     autocomplete_fields = ['customer']
class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    # min_num = 1
    # max_num = 10
    extra = 1
# Register your models here.
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['payment_status','placed_at','customer']
    list_per_page = 10
    inlines = [OrderItemInline]
class InventoryFilter(admin.SimpleListFilter):
    # side bar name
    title = "Inventory"
    # url parameter name
    parameter_name = "Inventory"

    def lookups(self, request, model_admin):
        return [
            #low will displat on side bar
            ('<10','Low')
        ]
    def queryset(self, request, queryset):
        if self.value == '<10':
            # return product that inventory less than 10 
            return queryset.filter(inventory__lt=10)
        
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title','unit_price']
    # exclude = ['inventory']
    #  auto complete slug field
    prepopulated_fields = {
        'slug':["title"]
    }
    # if you have hundered of drop down list you use to add search functionality it will only show 10 values
    autocomplete_fields = ['collection']
    list_display = ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    search_fields = ['product ']
    # inlines = [TagInline]
    list_per_page = 10
    actions = ['ClearInventory']
    list_filter = ['collection','last_update',InventoryFilter]
    #--------- used to prevent run muliple queries and it will like select_related and return queryet
    list_select_related = ['collection']
    #--------- get title form collection model
    def collection_title(self,product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status (self,obj):
        if obj.inventory < 10:
            return "Low"
        return "Ok"
    @admin.action(description="Clear Inventory")
    def ClearInventory(self,request,queryset):
        invenotryCount = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{invenotryCount} products was successfully Updated',
            # messages.ERROR
        )
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_editable = ['membership']
    list_per_page = 10
    # Eager Loading to prevent multiple queries agains customer.
    list_select_related = ['user']
    ordering = ['user__first_name','user__last_name']
    # search_fields = ['first_name','last_name']     default case sensitive and search for start or middle or any
    # search_fields = ['first_name__startswith','last_name__startswith']    case sensitve search 
    search_fields = ['user__first_name__istartswith','user__last_name__istartswith']  
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        # reverse ('site:app_model_page')
        # we use reverse function bcz url of produts changes and querystring in url
        url = reverse('admin:store_product_changelist') + "?" +  urlencode({
            "collection__id":str(collection.id)
        })
        return format_html('<a href="{}">{}</a>',url,collection.product_count)
        # return collection.product_count
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )