from django.contrib import admin
from .models import Category, Product, Comment



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'owner', 'created_at')
    search_fields = ('content',)

