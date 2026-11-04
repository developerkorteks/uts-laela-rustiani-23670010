from django.contrib import admin
from .models import Profile, Skill, Experience, Project, ContactMessage


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 1


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'email', 'location', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    inlines = [SkillInline, ExperienceInline, ProjectInline]
    fieldsets = (
        ('Identitas Utama', {
            'fields': ('full_name', 'title', 'avatar', 'short_bio', 'about', 'is_active')
        }),
        ('Kontak & Media Sosial', {
            'fields': ('email', 'phone', 'location', 'github_url', 'linkedin_url', 'resume_file')
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'profile', 'order')
    list_filter = ('category', 'profile')
    list_editable = ('order',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'period', 'profile', 'order')
    list_filter = ('company', 'profile')
    list_editable = ('order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'tech_stack', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at')
    list_editable = ('is_featured',)
    search_fields = ('title', 'description', 'tech_stack')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
