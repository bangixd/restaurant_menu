from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class BlogCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)
    cover_image = models.ImageField(upload_to='blog_categories/covers/', null=True, blank=True)

    class Meta:
        verbose_name = "دسته‌بندی بلاگ"
        verbose_name_plural = "دسته‌بندی‌های بلاگ"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)
    content = RichTextField()
    cover_image = models.ImageField(upload_to='blogs/covers/')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='blogs')
    reading_time = models.PositiveSmallIntegerField(blank=True, null=True)

    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "بلاگ"
        verbose_name_plural = "بلاگ‌ها"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
