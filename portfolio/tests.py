from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Skill, Experience, Project, ContactMessage


class PortfolioAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile = Profile.objects.create(
            full_name="Budi Pratama",
            title="Senior Python Engineer",
            short_bio="Spesialis arsitektur backend dan otomasi.",
            about="Pengalaman 5+ tahun membangun sistem skala menengah ke atas.",
            email="budi@example.com",
            location="Bandung, Indonesia",
            is_active=True
        )
        self.skill = Skill.objects.create(
            profile=self.profile,
            name="Django",
            category="backend",
            order=1
        )
        self.experience = Experience.objects.create(
            profile=self.profile,
            role="Backend Lead",
            company="Tech Corp",
            period="2021 - Sekarang",
            description="Memimpin pengembangan sistem microservices."
        )
        self.project = Project.objects.create(
            profile=self.profile,
            title="Sistem Monitoring IoT",
            description="Platform pemantauan sensor real-time dengan WebSockets.",
            tech_stack="Python, Django, Redis, Celery",
            is_featured=True
        )

        self.staff_user = User.objects.create_user(
            username="adminuser",
            password="adminpassword123",
            is_staff=True
        )

    def test_get_profile_returns_active(self):
        profile = Profile.get_profile()
        self.assertEqual(profile.full_name, "Budi Pratama")

    def test_profile_index_view(self):
        url = reverse('portfolio:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Budi Pratama")
        self.assertContains(response, "Senior Python Engineer")
        self.assertContains(response, "Sistem Monitoring IoT")
        self.assertContains(response, "Django")

    def test_contact_form_submission(self):
        url = reverse('portfolio:index')
        post_data = {
            'name': 'Klien Potensial',
            'email': 'klien@perusahaan.com',
            'subject': 'Tawaran Kerja Sama Proyek',
            'message': 'Halo Budi, kami tertarik berkolaborasi untuk proyek backend.'
        }
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ContactMessage.objects.filter(email='klien@perusahaan.com').exists())
        self.assertContains(response, "Pesan Anda berhasil dikirim")

    def test_project_detail_view(self):
        url = reverse('portfolio:project_detail', kwargs={'slug': self.project.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sistem Monitoring IoT")
        self.assertContains(response, "Platform pemantauan sensor real-time")

    def test_profile_edit_requires_staff(self):
        url = reverse('portfolio:edit')
        # Anonymous user should be redirected to login
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # Staff user should be able to access
        self.client.login(username='adminuser', password='adminpassword123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manajemen Profil Dinamis")

        # Staff user can update profile dynamically
        post_data = {
            'form_type': 'profile',
            'full_name': 'Budi Pratama S.Kom',
            'title': 'Lead Software Architect',
            'short_bio': 'Bio baru yang telah diperbarui secara dinamis.',
            'about': 'Tentang saya yang baru.',
            'email': 'budi.baru@example.com',
            'phone': '+62 811-1234-567',
            'location': 'Jakarta Selatan',
            'github_url': '',
            'linkedin_url': '',
        }
        post_resp = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(post_resp.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.full_name, 'Budi Pratama S.Kom')
        self.assertEqual(self.profile.title, 'Lead Software Architect')

    def test_dynamic_skill_crud(self):
        self.client.login(username='adminuser', password='adminpassword123')
        # Create
        create_url = reverse('portfolio:skill_create')
        resp = self.client.post(create_url, {
            'name': 'Kubernetes',
            'category': 'devops',
            'order': 5
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        new_skill = Skill.objects.filter(name='Kubernetes').first()
        self.assertIsNotNone(new_skill)

        # Delete
        del_url = reverse('portfolio:skill_delete', kwargs={'skill_id': new_skill.id})
        del_resp = self.client.post(del_url, follow=True)
        self.assertEqual(del_resp.status_code, 200)
        self.assertFalse(Skill.objects.filter(name='Kubernetes').exists())

    def test_dynamic_experience_and_project_crud(self):
        self.client.login(username='adminuser', password='adminpassword123')
        # Create Experience
        exp_url = reverse('portfolio:experience_create')
        self.client.post(exp_url, {
            'role': 'DevOps Architect',
            'company': 'Cloud Media',
            'period': '2019 - 2021',
            'description': 'Mengelola Kubernetes cluster',
            'order': 3
        }, follow=True)
        exp = Experience.objects.filter(role='DevOps Architect').first()
        self.assertIsNotNone(exp)

        # Delete Experience
        self.client.post(reverse('portfolio:experience_delete', kwargs={'exp_id': exp.id}), follow=True)
        self.assertFalse(Experience.objects.filter(role='DevOps Architect').exists())

        # Create Project
        proj_url = reverse('portfolio:project_create')
        self.client.post(proj_url, {
            'title': 'Sistem Audit Otomatis',
            'tech_stack': 'Python, SQLite',
            'description': 'Audit log parser mandiri.',
            'demo_url': '',
            'repo_url': '',
            'is_featured': True
        }, follow=True)
        proj = Project.objects.filter(title='Sistem Audit Otomatis').first()
        self.assertIsNotNone(proj)

        # Delete Project
        self.client.post(reverse('portfolio:project_delete', kwargs={'project_id': proj.id}), follow=True)
        self.assertFalse(Project.objects.filter(title='Sistem Audit Otomatis').exists())
