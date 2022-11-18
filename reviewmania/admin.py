from django.contrib import admin
from reviewmania.models import Category, Criteria, Photo, Product, Review, Score

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Criteria)
admin.site.register(Review)
admin.site.register(Score)
admin.site.register(Photo)