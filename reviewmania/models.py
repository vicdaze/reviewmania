from email.mime import image
from multiprocessing.sharedctypes import Value
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    @property
    def sorted_product_set(self):
        return self.product_set.order_by('title')

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_photo = models.ImageField(upload_to="products", blank=True)

    def __str__(self) -> str:
        return self.title

    def average_rating(self):
        return self.review_set.aggregate(Avg('score__value'))['score__value__avg']

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Criteria(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return self.name

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self) -> str:
        return self.text

    def average_rating(self):
        return self.score_set.aggregate(avg_value=Avg('value'))['avg_value']
    

class Score(models.Model):
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])

class Photo(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="reviews")
