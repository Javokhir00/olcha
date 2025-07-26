from django.db import models
from django.utils.text import slugify
from django.db.models import Avg
from config.settings import AUTH_USER_MODEL




class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Category(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='category/images/', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'



class Product(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=14, decimal_places=2)
    image = models.ImageField(upload_to='product/images/', null=True, blank=True)
    amount = models.IntegerField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def avg_rating(self):
        return self.comments.aggregate(Avg('rating'))['rating__avg'] or 0

    class Meta:
        ordering = ['-created_at']



class ProductImage(BaseModel):
    image = models.ImageField(upload_to='product/images/', null=True, blank=True)
    product = models.ForeignKey(Product, related_name='images', on_delete = models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.image.url



class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ONE   = 1,    '★☆☆☆☆'
        TWO   = 2,    '★★☆☆☆'
        THREE = 3,    '★★★☆☆'
        FOUR  = 4,    '★★★★☆'
        FIVE  = 5,    '★★★★★'

    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.THREE)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')


    def __str__(self):
        return f'{self.name} - {self.rating}'



class AttributeKey(BaseModel):
    key_name = models.CharField(max_length=255)

    def __str__(self):
        return self.key_name

    class Meta:
        verbose_name_plural = 'Attribute Keys'



class AttributeValue(BaseModel):
    value_name = models.CharField(max_length=255)

    def __str__(self):
        return self.value_name

    class Meta:
        verbose_name_plural = 'Attribute Values'



class Attribute(BaseModel):
    attribute_key = models.ForeignKey(AttributeKey, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = 'attributes')

    def __str__(self):
        return f'{self.product.name} - {self.attribute_key.key_name} - {self.attribute_value.value_name}'

    class Meta:
        verbose_name_plural = 'Attribute Products'






