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


class VACAdmin(admin.ModelAdmin):
    list_display = ('vac_no', 'vac_title', 'college_name', 'department_name', 'no_of_days', 'from_date', 'to_date', 'gallery_category', 'gallery_image_preview')
    list_filter = ('from_date', 'gallery_category')
    search_fields = ('vac_no', 'vac_title', 'college_name', 'department_name')
    readonly_fields = ('created_at', 'gallery_image_preview')
    
    fieldsets = (
        ('VAC Identification', {
            'fields': ('vac_no',)
        }),
        ('Course Information', {
            'fields': ('vac_title', 'college_name', 'department_name')
        }),
        ('Course Duration', {
            'fields': ('from_date', 'to_date', 'no_of_days')
        }),
        ('Gallery', {
            'fields': ('gallery_category', 'gallery_image', 'gallery_image_preview'),
            'description': 'Select the specific gallery image to link to this VAC entry. The image must belong to the selected category.'
        }),
        ('Meta Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def gallery_image_preview(self, obj):
        if obj.gallery_image and obj.gallery_image.image:
            return format_html(
                '<img src="{}" style="height:80px; border-radius:6px; border:1px solid #ddd;" />',
                obj.gallery_image.image.url
            )
        return "No image selected"
    gallery_image_preview.short_description = "Image Preview"
    
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields


admin.site.register(VAC, VACAdmin)


class ConsultancyProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'institution_name', 'staff_name', 'designation', 'department', 'fund_amount', 'date_of_transaction')
    search_fields = ('project_name', 'institution_name', 'staff_name', 'department')
    list_filter = ('institution_name', 'department', 'date_of_transaction')


class FundedProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'institution_name', 'staff_name', 'designation', 'department', 'fund_amount', 'date_of_transaction')
    search_fields = ('project_name', 'institution_name', 'staff_name', 'department')
    list_filter = ('institution_name', 'department', 'date_of_transaction')


admin.site.register(ConsultancyProject, ConsultancyProjectAdmin)
admin.site.register(FundedProject, FundedProjectAdmin)

