from django.core.management.base import BaseCommand
from abtapp.models import ProjectDomain


class Command(BaseCommand):
    help = 'Populate initial project domains'

    def handle(self, *args, **options):
        domains_data = [
            {
                'domain_type': 'IEEE_NON_IEEE',
                'title': 'IEEE & Non-IEEE Real-Time Projects',
                'description': 'We specialize in the latest IEEE transactions and non-IEEE cutting-edge domains, ensuring your project meets global academic and industry standards. Our real-time implementations bridge the gap between complex algorithms and practical utility.',
                'icon_class': 'bi-laptop'
            },
            {
                'domain_type': 'SCHOOL_MINI',
                'title': 'School & Mini-Projects',
                'description': 'Building foundational skills for young innovators through hands-on learning modules, simplified engineering models, and creative working prototypes.',
                'icon_class': 'bi-mortarboard'
            },
            {
                'domain_type': 'PATENT',
                'title': 'Novel Projects for Patent',
                'description': 'Transform your original research into valuable intellectual property. Our experts guide you through novelty search, prototype refinement, and patent filing support.',
                'icon_class': 'bi-award'
            },
            {
                'domain_type': 'FUNDED',
                'title': 'Funded Projects, Research Proposals & Prototypes',
                'description': 'Expert guidance for securing government and private grants. We assist in academic documentation, feasibility studies, research proposals, and developing working hardware/software prototypes.',
                'icon_class': 'bi-journal-check'
            }
        ]

        for domain_data in domains_data:
            domain, created = ProjectDomain.objects.get_or_create(
                domain_type=domain_data['domain_type'],
                defaults={
                    'title': domain_data['title'],
                    'description': domain_data['description'],
                    'icon_class': domain_data['icon_class']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created domain: {domain.title}'))
            else:
                self.stdout.write(f'Domain already exists: {domain.title}')

        self.stdout.write(self.style.SUCCESS('All domains populated successfully!'))
