from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from abtapp.models import ProjectCategory


class StaticPageSitemap(Sitemap):
    pages = (
        ('home', 1.0, 'weekly'),
        ('projects', 0.9, 'weekly'),
        ('research_guidance', 0.9, 'weekly'),
        ('training', 0.9, 'weekly'),
        ('value_added_courses', 0.8, 'monthly'),
        ('products', 0.8, 'monthly'),
        ('consultancy_projects', 0.8, 'monthly'),
        ('funded_projects', 0.8, 'monthly'),
        ('our_branches', 0.8, 'monthly'),
        ('branch_nagercoil', 0.9, 'monthly'),
        ('branch_tirunelveli', 0.9, 'monthly'),
        ('branch_chennai', 0.9, 'monthly'),
        ('branch_pudukkottai', 0.9, 'monthly'),
        ('branch_marthandam', 0.9, 'monthly'),
        ('mou', 0.6, 'monthly'),
        ('gallery', 0.6, 'daily'),
        ('videos', 0.6, 'daily'),
        ('career', 0.6, 'monthly'),
        ('our_team', 0.5, 'monthly'),
        ('contact_us', 0.7, 'yearly'),
    )

    def items(self):
        return self.pages

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]


class ProjectCategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return ProjectCategory.objects.all()

    def location(self, item):
        return reverse('project_category_detail', kwargs={'category_id': item.pk})
