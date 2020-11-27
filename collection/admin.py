from django.contrib import admin
from collection.models import Collection, ProductInCollection


class ProductInCollectionInLine(admin.TabularInline):
    model = ProductInCollection
    raw_id_fields = ['collection']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'created_at', 'updated_at']
    inlines = [ProductInCollectionInLine]
