from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.utils.html import format_html

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 5

class GalleryCategoryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]


class VideoAdmin(admin.ModelAdmin):
    list_display = ("CODE", "UPLOADED_DATE", "TITLE", "TYPE", "YOUTUBE_LINK", "video_preview")
    search_fields = ("TITLE", "CODE")
    list_filter = ("TITLE",)

    def video_preview(self, obj):
        return format_html(
            '<iframe width="200" height="120" src="{}" frameborder="0" allowfullscreen></iframe>',
            obj.embed_link(),
        )
    video_preview.short_description = "Preview"


class MoUAdmin(admin.ModelAdmin):
    list_display = ('MoU_NO', 'ORGANIZATION_NAME', 'LOCATION', 'OFFICIAL_WEBSITE', 'DATE_OF_MoU', 'VALIDITY')
    search_fields = ('MoU_NO', 'ORGANIZATION_NAME', 'LOCATION')
    list_filter = ('DATE_OF_MoU', 'VALIDITY')


class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_count')
    search_fields = ('name',)
    readonly_fields = ('project_count',)
    
    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = "Number of Projects"


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_name', 'category', 'abstract_file_link')
    list_filter = ('category',)
    search_fields = ('project_id', 'project_name')
    readonly_fields = ('id', 'abstract_preview')
    
    fieldsets = (
        ('Project Information', {
            'fields': ('category', 'project_id', 'project_name')
        }),
        ('Abstract (PDF)', {
            'fields': ('abstract', 'abstract_preview'),
            'description': 'Upload project abstract as PDF file'
        }),
    )
    
    def abstract_file_link(self, obj):
        """Show PDF file link in list view"""
        if obj.abstract:
            filename = obj.abstract.name.split('/')[-1]
            return format_html(
                '<a href="{}" target="_blank" style="color: #417690;"><i class="bi bi-file-pdf"></i> {}</a>',
                obj.abstract.url,
                filename
            )
        return "No file"
    abstract_file_link.short_description = "Abstract"
    
    def abstract_preview(self, obj):
        """Show PDF file link and info in form"""
        if obj.abstract:
            filename = obj.abstract.name.split('/')[-1]
            return format_html(
                '<a href="{}" target="_blank" download class="button" style="background-color: #417690; padding: 5px 10px; color: white; text-decoration: none; border-radius: 3px;">📥 Download PDF: {}</a>',
                obj.abstract.url,
                filename
            )
        return "No file uploaded yet"
    abstract_preview.short_description = "Current Abstract"


admin.site.register(Video, VideoAdmin)
admin.site.register(MoU, MoUAdmin)
admin.site.register(GalleryCategory, GalleryCategoryAdmin)
admin.site.register(GalleryImage)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
