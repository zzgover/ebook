from django.db import models
# Create your models here.
from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',on_delete='DO_NOTHING')
    name = models.CharField(max_length=200, db_index=True)
    author = models.CharField(max_length=100, blank=True)
    press = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='product/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

