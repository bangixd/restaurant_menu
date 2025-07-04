from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Restaurant(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurant")
    name = models.CharField(max_length=100)

    short_description = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)

    slug = models.SlugField(unique=True, blank=True)

    address = models.CharField(max_length=255, blank=True)
    location = models.JSONField(null=True, blank=True)  # {'lat': ..., 'lng': ...}
    phone_number = models.CharField(max_length=20, blank=True)

    instagram = models.URLField(blank=True)
    telegram = models.URLField(blank=True)

    banner = models.ImageField(upload_to='restaurant_banners/', null=True, blank=True)
    rating = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Restaurant.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RestaurantGallery(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='restaurant_gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.restaurant.name}"


class RestaurantOpeningHour(models.Model):
    DAYS_OF_WEEK = [
        ('sat', 'شنبه'),
        ('sun', 'یک‌شنبه'),
        ('mon', 'دو‌شنبه'),
        ('tue', 'سه‌شنبه'),
        ('wed', 'چهار‌شنبه'),
        ('thu', 'پنج‌شنبه'),
        ('fri', 'جمعه'),
    ]

    restaurant = models.ForeignKey('Restaurant', related_name='opening_hours', on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        unique_together = ('restaurant', 'day')
        ordering = ['day']

    def __str__(self):
        return f"{self.restaurant.name} - {self.get_day_display()}: {self.open_time} تا {self.close_time}"



class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.restaurant.name} - {self.title}"


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"
