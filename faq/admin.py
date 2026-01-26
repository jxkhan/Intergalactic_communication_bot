from django.contrib import admin
from .models import Categories, FAQ
# Register your models here.


admin.site.register(Categories)
admin.site.register(FAQ)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)


class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'category', 'views', 'helpful_votes', 'created_at', 'updated_at')
    search_fields = ('question', 'answer', 'keywords')
    list_filter = ('category',)
    ordering = ('-created_at',)   
