from django.contrib import admin

from .models import (
    Category,
    Order,
    OrderProduct,
    Product,
    ProductPromotionEvent,
    PromotionEvent,
    StockManagement,
    User,

)

# Register your models here.

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Product)
admin.site.register(ProductPromotionEvent)
admin.site.register(PromotionEvent)
admin.site.register(StockManagement)
admin.site.register(User)