from django.db import models


class Category(models.Model):
    name = models.CharField(max_length = 30)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 255)
    slug = models.SlugField(max_length = 255)
    image = models.ImageField(upload_to='product_image', default=  '/product_image/no_image.jpeg', blank=True, null=True)
    description = models.TextField()#default = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    available = models.BooleanField(default = True)
    
    def __str__(self):
        return self.name
    
class ProductLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING) #, null=False, blank=False
    price = models.IntegerField()
    date_from = models.DateField() # この日から値段がprice
    
    def __str__(self):
        date_str = self.date_from.strftime('%y-%m-%d')
        return "{} {}".format(self.product.name, date_str)
