from django.db import models
from django.utils.text import slugify
import os
import uuid

def gallery_image_upload_path(instance, filename):
    """Auto-generate SEO-friendly filename on upload."""
    ext = filename.split('.')[-1].lower()
    name_slug = slugify(instance.name) if instance.name else str(uuid.uuid4().hex[:6])
    seo_filename = f"{name_slug}-abtechnologies.{ext}"
    return os.path.join('gallery_images', seo_filename)

class GalleryCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=gallery_image_upload_path)
    name = models.CharField(max_length=255, blank=True)
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="SEO alt text for this image. Example: 'Industrial Control Panel Hardware - AB Technologies'. Leave blank to auto-generate."
    )

    def get_seo_alt(self):
        """Returns the best available alt text for SEO."""
        if self.alt_text:
            return self.alt_text
        if self.name:
            return f"{self.name} - AB Technologies"
        return "AB Technologies Gallery Image"

    def __str__(self):
        return self.name if self.name else "Unnamed Image"

class Video(models.Model):
    CODE = models.CharField(max_length=20, unique=True)
    UPLOADED_DATE = models.DateField(null=True, blank=True)
    TITLE = models.CharField(max_length=200)
    TYPE_CHOICES = [
        ('BASICS', 'BASICS'),
        ('PROJECTS', 'PROJECTS'),
        ('PRODUCTS', 'PRODUCTS'),
    ]
    TYPE=models.CharField(max_length=50, choices=TYPE_CHOICES,default=0)
    YOUTUBE_LINK = models.URLField()

    def embed_link(self):
        # Convert normal YouTube link to embed format
        if "watch?v=" in self.YOUTUBE_LINK:
            return self.YOUTUBE_LINK.replace("watch?v=", "embed/")
        elif "youtu.be/" in self.YOUTUBE_LINK:
            return self.YOUTUBE_LINK.replace("youtu.be/", "youtube.com/embed/")
        return self.YOUTUBE_LINK

    def __str__(self):
        return self.TITLE

class MoU(models.Model):
    MoU_NO = models.CharField(max_length=100, unique=True)
    ORGANIZATION_NAME = models.CharField(max_length=255)
    LOCATION = models.CharField(max_length=255, blank=True, null=True)
    OFFICIAL_WEBSITE = models.URLField(blank=True, null=True)
    DATE_OF_MoU = models.DateField(blank=True,null=True)
    VALIDITY = models.CharField(max_length=100,blank=True,null=True)  # Or models.DateField if it’s a date range

    def __str__(self):
        return f"{self.MoU_NO} - {self.ORGANIZATION_NAME}"