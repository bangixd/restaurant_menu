from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


class Restaurant(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurant")
    name = models.CharField(max_length=100)
    eng_name = models.CharField(max_length=100, null=True, blank=True)

    slogan = models.CharField(max_length=255, blank=True, null=True, verbose_name='شعار رستوران')
    short_description = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)

    logo = models.ImageField(upload_to='restaurant/logos/', blank=True, null=True, verbose_name='لوگوی رستوران')

    slug = models.SlugField(unique=True, blank=True)

    address = models.CharField(max_length=255, blank=True)
    location = models.JSONField(null=True, blank=True)  # {'lat': ..., 'lng': ...}
    phone_number1 = models.CharField(max_length=20, blank=True)
    phone_number2 = models.CharField(max_length=20, blank=True)

    instagram = models.URLField(blank=True)
    telegram = models.URLField(blank=True)

    banner = models.ImageField(upload_to='restaurant_banners/', null=True, blank=True)
    rating = models.FloatField(default=0.0)

    zarinpal_merchant_id = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.eng_name)
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


class RestaurantVideo(models.Model):
    restaurant = models.ForeignKey('Restaurant', related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    video = models.FileField(upload_to='restaurant/videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.restaurant.name} - {self.title or "ویدیو"}'


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


class RestaurantComment(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='متن نظر')
    rating = models.PositiveSmallIntegerField(verbose_name='امتیاز (از ۵)', default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'نظر رستوران'
        verbose_name_plural = 'نظرات رستوران'

    def __str__(self):
        return f"{self.user} -> {self.restaurant} ({self.rating}/5)"


class TableCall(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='table_calls'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='table_calls'
    )
    table_number = models.PositiveIntegerField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Table {self.table_number} - {self.restaurant.name}'


class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.restaurant.name} - {self.title}"


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"
