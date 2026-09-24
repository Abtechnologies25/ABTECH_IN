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
    VALIDITY = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f"{self.MoU_NO} - {self.ORGANIZATION_NAME}"


class ProjectCategory(models.Model):
    """Project categories (like GalleryCategory)"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    icon_class = models.CharField(max_length=100, blank=True, null=True, help_text="Bootstrap icon class (e.g., 'bi-laptop', 'bi-gear')")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"


class Project(models.Model):
    """Individual projects"""
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    project_id = models.CharField(max_length=50, unique=True)
    project_name = models.CharField(max_length=255)
    abstract = models.FileField(upload_to='project_abstracts/', help_text="Upload project abstract as PDF", blank=True, null=True)
    
    def __str__(self):
        return f"{self.project_id} - {self.project_name}"
    
    def get_abstract_filename(self):
        """Get the filename of the abstract PDF"""
        if self.abstract:
            return self.abstract.name.split('/')[-1]
        return None
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = "Projects"


class VAC(models.Model):
    """Value Added Course - Training and Workshop"""
    vac_no = models.CharField(max_length=50, unique=True, help_text="Unique VAC Number")
    college_name = models.CharField(max_length=255)
    department_name = models.CharField(max_length=255)
    vac_title = models.CharField(max_length=255)
    no_of_days = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    gallery_category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='vac_trainings')
    gallery_image = models.ForeignKey(GalleryImage, on_delete=models.SET_NULL, null=True, blank=True, related_name='vac_entries', help_text="Select the specific gallery image for this VAC")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vac_no} - {self.vac_title}"
    
    class Meta:
        ordering = ['-from_date']
        verbose_name = "Value Added Course"
        verbose_name_plural = "Value Added Courses"
