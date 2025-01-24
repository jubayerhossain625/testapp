from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    cover_image =models.ImageField(upload_to="products/covers/")

    def __str__(self):
        return self.name




class ProductImage(models.Model):
    product = models.ForeignKey(Product,related_name='gallery_images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"
    