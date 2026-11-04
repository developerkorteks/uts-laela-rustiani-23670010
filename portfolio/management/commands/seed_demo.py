from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio.models import Profile, Skill, Experience, Project
from ecommerce.models import Category, Product


class Command(BaseCommand):
    help = 'Mengisi database dengan data demo awal untuk Profil Pribadi dan E-commerce'

    def handle(self, *args, **options):
        self.stdout.write('Menginisialisasi data demo...')

        # 1. Superuser / Admin
        admin_user, created = User.objects.get_or_create(username='admin')
        if created:
            admin_user.set_password('admin123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.email = 'admin@example.com'
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Superuser dibuat: username=admin, password=admin123'))
        else:
            self.stdout.write('Superuser admin sudah ada.')

        # 2. Profile Pribadi Dinamis
        profile, _ = Profile.objects.get_or_create(
            is_active=True,
            defaults={
                'full_name': 'Ahmad Fauzan S.Kom',
                'title': 'Senior Backend & Systems Engineer',
                'short_bio': 'Spesialis perancangan arsitektur backend Django, integrasi API, dan infrastruktur server berkinerja tinggi.',
                'about': (
                    'Halo! Saya Ahmad, seorang pengembang perangkat lunak dengan pengalaman 6+ tahun dalam membangun '
                    'sistem berbasis web, otomatisasi administrasi server, dan sistem pembayaran terintegrasi.\n\n'
                    'Fokus utama saya adalah efisiensi kode, keandalan sistem (*high availability*), dan antarmuka '
                    'yang fungsional tanpa kompleksitas berlebihan.'
                ),
                'email': 'ahmad.fauzan@example.com',
                'phone': '+62 812-9876-5432',
                'location': 'Jakarta Selatan, Indonesia',
                'github_url': 'https://github.com',
                'linkedin_url': 'https://linkedin.com',
            }
        )

        # Skills
        if not profile.skills.exists():
            skills_data = [
                ('Python 3.11 / Django', 'backend', 1),
                ('PostgreSQL & Redis', 'backend', 2),
                ('RESTful API & WebSockets', 'backend', 3),
                ('Tailwind CSS & HTMX', 'frontend', 4),
                ('JavaScript / Alpine.js', 'frontend', 5),
                ('Docker & Containerization', 'devops', 6),
                ('Linux Server & Nginx', 'devops', 7),
                ('Git & CI/CD Pipelines', 'devops', 8),
            ]
            for name, cat, order in skills_data:
                Skill.objects.create(profile=profile, name=name, category=cat, order=order)
            self.stdout.write('Data keahlian (skills) berhasil ditambahkan.')

        # Experiences
        if not profile.experiences.exists():
            exp_data = [
                (
                    'Lead Backend Engineer',
                    'PT Solusi Digital Nusantara',
                    '2022 - Sekarang',
                    'Mengarsiteki sistem inti administrasi transaksi dan otomasi server microservices dengan Django & Celery.',
                    1
                ),
                (
                    'Fullstack Web Developer',
                    'Inovasi Tekno Mandiri',
                    '2019 - 2022',
                    'Mengembangkan sistem portal e-commerce dan integrasi payment gateway perbankan nasional.',
                    2
                ),
            ]
            for role, comp, period, desc, order in exp_data:
                Experience.objects.create(profile=profile, role=role, company=comp, period=period, description=desc, order=order)
            self.stdout.write('Data pengalaman kerja berhasil ditambahkan.')

        # Projects
        if not profile.projects.exists():
            proj_data = [
                (
                    'Sistem Monitoring & Administrasi Server',
                    'Platform monitoring metrik server Linux secara real-time dengan alert notification dan dashboard analitik.',
                    'Python, Django, Redis, SQLite, Tailwind',
                    'https://github.com',
                    'https://example.com/demo1'
                ),
                (
                    'Engine Transaksi Toko Digital B2B',
                    'Sistem e-commerce modular dengan manajemen inventaris multi-gudang dan integrasi multi-gateway.',
                    'Django, PostgreSQL, Celery, Alpine.js',
                    'https://github.com',
                    'https://example.com/demo2'
                ),
                (
                    'Otomasi Backup Database Terjadwal',
                    'CLI dan web daemon untuk snapshot backup otomatis database terenkripsi ke penyimpanan S3.',
                    'Python, Shell Script, Docker',
                    'https://github.com',
                    ''
                )
            ]
            for title, desc, stack, repo, demo in proj_data:
                Project.objects.create(profile=profile, title=title, description=desc, tech_stack=stack, repo_url=repo, demo_url=demo)
            self.stdout.write('Data proyek portofolio berhasil ditambahkan.')

        # 3. Kategori & Produk E-commerce
        cat_server, _ = Category.objects.get_or_create(
            slug='server-hardware',
            defaults={'name': 'Server & Hardware', 'description': 'Perangkat keras server dan jaringan'}
        )
        cat_software, _ = Category.objects.get_or_create(
            slug='software-tools',
            defaults={'name': 'Software & Tools', 'description': 'Lisensi software utilitas dan sistem operasi'}
        )
        cat_aksesoris, _ = Category.objects.get_or_create(
            slug='aksesoris',
            defaults={'name': 'Aksesoris & Kabel', 'description': 'Kabel jaringan, adapter, dan aksesoris teknis'}
        )

        products_data = [
            (
                cat_server,
                'Home Server Micro-Node Intel N100',
                'Unit server kompak 4-Core efisien daya (6W-15W), 16GB DDR5, 512GB NVMe SSD, Dual 2.5GbE LAN. Sangat cocok untuk self-hosting dan server administrasi.',
                Decimal('2850000'),
                8
            ),
            (
                cat_server,
                'Managed Switch 8-Port Gigabit PoE',
                'Switch jaringan manageable dengan dukungan 8 port Gigabit PoE+ (802.3af/at) total budget 65W, web management VLAN, dan QoS.',
                Decimal('850000'),
                12
            ),
            (
                cat_software,
                'Lisensi Server Dashboard Pro (Perpetual)',
                'Lisensi software dashboard pemantauan performa server dan audit log terpusat untuk 5 node server.',
                Decimal('450000'),
                25
            ),
            (
                cat_aksesoris,
                'Kabel LAN Cat6 SFTP 10 Meter',
                'Kabel jaringan Cat6 Shielded Foiled Twisted Pair dengan konektor RJ45 berlapis emas, tahan interferensi sinyal elektromagnetik.',
                Decimal('95000'),
                30
            ),
        ]

        for cat, name, desc, price, stock in products_data:
            Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': cat,
                    'description': desc,
                    'price': price,
                    'stock': stock,
                    'is_active': True
                }
            )

        self.stdout.write(self.style.SUCCESS('Data demo selesai diinisialisasi dengan sukses!'))
