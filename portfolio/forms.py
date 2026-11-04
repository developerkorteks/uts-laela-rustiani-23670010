from django import forms
from .models import Profile, ContactMessage, Skill, Experience, Project


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-400',
                'placeholder': 'Nama Anda'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-400',
                'placeholder': 'nama@example.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-400',
                'placeholder': 'Subjek perihal / kebutuhan proyek'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 placeholder-neutral-500 focus:outline-none focus:border-neutral-400',
                'rows': 4,
                'placeholder': 'Tuliskan pesan Anda...'
            }),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'title', 'short_bio', 'about', 'avatar',
            'email', 'phone', 'location', 'github_url', 'linkedin_url', 'resume_file'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400'}),
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400'}),
            'short_bio': forms.Textarea(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'rows': 2}),
            'about': forms.Textarea(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'rows': 5}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400'}),
            'github_url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'placeholder': 'Nama Keahlian'}),
            'category': forms.Select(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['role', 'company', 'period', 'description', 'order']
        widgets = {
            'role': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'placeholder': 'Posisi / Role'}),
            'company': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'placeholder': 'Perusahaan / Organisasi'}),
            'period': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'placeholder': 'Contoh: 2021 - Sekarang'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'rows': 3, 'placeholder': 'Deskripsi pekerjaan/tanggung jawab'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400'}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'tech_stack', 'description', 'image', 'demo_url', 'repo_url', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'placeholder': 'Judul Proyek'}),
            'tech_stack': forms.TextInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'placeholder': 'Python, Django, Tailwind'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'rows': 4, 'placeholder': 'Rincian deskripsi proyek...'}),
            'demo_url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'placeholder': 'https://demo.example.com'}),
            'repo_url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 text-sm bg-neutral-900 border border-neutral-700 rounded text-neutral-100 focus:border-neutral-400', 'placeholder': 'https://github.com/...'}),
        }
