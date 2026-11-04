from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from .models import Profile, Project, ContactMessage, Skill, Experience
from .forms import ContactForm, ProfileEditForm, SkillForm, ExperienceForm, ProjectForm


def profile_index(request):
    profile = Profile.get_profile()
    skills = profile.skills.all()
    experiences = profile.experiences.all()
    projects = profile.projects.all()

    # Skill grouped by category for clean, structured display
    skills_by_category = {}
    for skill in skills:
        cat = skill.get_category_display()
        skills_by_category.setdefault(cat, []).append(skill.name)

    contact_form = ContactForm()

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Pesan Anda berhasil dikirim. Terima kasih telah menghubungi.')
            return redirect('portfolio:index')
        else:
            messages.error(request, 'Mohon periksa kembali formulir Anda.')

    context = {
        'profile': profile,
        'skills_by_category': skills_by_category,
        'experiences': experiences,
        'projects': projects,
        'contact_form': contact_form,
    }
    return render(request, 'portfolio/index.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'portfolio/project_detail.html', {'project': project})


@staff_member_required
def profile_edit(request):
    profile = Profile.get_profile()
    tab = request.GET.get('tab', 'bio')

    if request.method == 'POST' and request.POST.get('form_type') == 'profile':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui secara dinamis.')
            return redirect(f"{request.path}?tab=bio")
    else:
        form = ProfileEditForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
        'skills': profile.skills.all(),
        'experiences': profile.experiences.all(),
        'projects': profile.projects.all(),
        'skill_form': SkillForm(),
        'experience_form': ExperienceForm(),
        'project_form': ProjectForm(),
        'active_tab': tab,
    }
    return render(request, 'portfolio/profile_edit.html', context)


@staff_member_required
@require_POST
def skill_create(request):
    profile = Profile.get_profile()
    form = SkillForm(request.POST)
    if form.is_valid():
        skill = form.save(commit=False)
        skill.profile = profile
        skill.save()
        messages.success(request, f'Keahlian "{skill.name}" berhasil ditambahkan.')
    else:
        messages.error(request, 'Gagal menambahkan keahlian. Mohon periksa input.')
    return redirect('/edit/?tab=skills')


@staff_member_required
@require_POST
def skill_delete(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    name = skill.name
    skill.delete()
    messages.info(request, f'Keahlian "{name}" telah dihapus.')
    return redirect('/edit/?tab=skills')


@staff_member_required
@require_POST
def experience_create(request):
    profile = Profile.get_profile()
    form = ExperienceForm(request.POST)
    if form.is_valid():
        exp = form.save(commit=False)
        exp.profile = profile
        exp.save()
        messages.success(request, f'Pengalaman "{exp.role}" di {exp.company} berhasil ditambahkan.')
    else:
        messages.error(request, 'Gagal menambahkan pengalaman kerja.')
    return redirect('/edit/?tab=experiences')


@staff_member_required
@require_POST
def experience_delete(request, exp_id):
    exp = get_object_or_404(Experience, id=exp_id)
    role = exp.role
    exp.delete()
    messages.info(request, f'Pengalaman "{role}" telah dihapus.')
    return redirect('/edit/?tab=experiences')


@staff_member_required
@require_POST
def project_create(request):
    profile = Profile.get_profile()
    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
        proj = form.save(commit=False)
        proj.profile = profile
        proj.save()
        messages.success(request, f'Proyek "{proj.title}" berhasil ditambahkan ke portofolio.')
    else:
        messages.error(request, 'Gagal menambahkan proyek portofolio.')
    return redirect('/edit/?tab=projects')


@staff_member_required
@require_POST
def project_delete(request, project_id):
    proj = get_object_or_404(Project, id=project_id)
    title = proj.title
    proj.delete()
    messages.info(request, f'Proyek "{title}" telah dihapus.')
    return redirect('/edit/?tab=projects')
