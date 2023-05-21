from django.contrib import admin
from store.models import Product
# alias used to rename field
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from tags.models import TaggedItem
from store.admin import ProductAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.

class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 0

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2","email","first_name","last_name"),
            },
        ),
    )

admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)