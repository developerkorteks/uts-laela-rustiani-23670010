from django.db import models
from django.utils.text import slugify


class Profile(models.Model):
    full_name = models.CharField(max_length=150, default="Pengembang Web")
    title = models.CharField(max_length=200, default="Software Engineer & Backend Developer")
    short_bio = models.TextField(blank=True, default="Membangun sistem perangkat lunak yang andal, efisien, dan mudah dipelihara.")
    about = models.TextField(blank=True, default="Halo, saya adalah pengembang web yang fokus pada arsitektur backend, otomasi sistem, dan pengembangan web yang fungsional.")
    avatar = models.ImageField(upload_to="portfolio/avatars/", blank=True, null=True)
    email = models.EmailField(blank=True, default="developer@example.com")
    phone = models.CharField(max_length=30, blank=True, default="+62 812-3456-7890")
    location = models.CharField(max_length=150, blank=True, default="Jakarta, Indonesia")
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    resume_file = models.FileField(upload_to="portfolio/resume/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil Pribadi"
        verbose_name_plural = "Profil Pribadi"

    def __str__(self):
        return self.full_name

    @classmethod
    def get_profile(cls):
        profile = cls.objects.filter(is_active=True).first()
        if not profile:
            profile = cls.objects.create(
                full_name="Alex Kurniawan",
                title="Fullstack & Backend Developer",
                short_bio="Membangun sistem perangkat lunak yang andal dan terukur.",
                about="Saya seorang pengembang perangkat lunak yang berfokus pada Python, Django, dan arsitektur web modern yang efisien.",
                email="alex@example.com",
                location="Jakarta, Indonesia"
            )
        return profile


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('devops', 'DevOps & Tools'),
        ('other', 'Lainnya'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='backend')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Keahlian"
        verbose_name_plural = "Daftar Keahlian"

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="experiences")
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    period = models.CharField(max_length=100, help_text="Contoh: 2022 - Sekarang")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "Pengalaman Kerja"
        verbose_name_plural = "Riwayat Pengalaman"

    def __str__(self):
        return f"{self.role} at {self.company}"


class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=250, help_text="Pisahkan dengan koma, contoh: Python, Django, Tailwind")
    image = models.ImageField(upload_to="portfolio/projects/", blank=True, null=True)
    demo_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = "Proyek Portofolio"
        verbose_name_plural = "Proyek Portofolio"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or "project"
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Pesan Kontak"
        verbose_name_plural = "Kotak Masuk Pesan"

    def __str__(self):
        return f"Pesan dari {self.name} - {self.subject}"
