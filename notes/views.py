from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Tag

def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')

        # cria a nova nota no banco
        Note.objects.create(title=title, content=content)

        return redirect('index')  # redireciona para a lista

    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})

def delete(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    note.delete()
    return redirect('index')

def _get_or_create_tag(tag_raw: str):
    if not tag_raw:
        return None
    name = tag_raw.strip()
    if not name:
        return None
    from .models import Tag
    tag = Tag.objects.filter(name__iexact=name).first()
    return tag or Tag.objects.create(name=name)

def edit(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        note.title = request.POST.get('titulo', note.title).strip()
        note.content = request.POST.get('detalhes', note.content)
        tag_input = request.POST.get('tag', '')

        note.tag = _get_or_create_tag(tag_input)  # vazio → None; texto → Tag
        note.save()
        return redirect('index')
    return render(request, 'notes/edit.html', {'note': note})

def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo', '').strip()
        content = request.POST.get('detalhes', '')
        tag_input = request.POST.get('tag', '')

        tag = _get_or_create_tag(tag_input)
        Note.objects.create(title=title, content=content, tag=tag)
        return redirect('index')

    all_notes = Note.objects.all().order_by('-id')
    return render(request, 'notes/index.html', {'notes': all_notes})

def tag_list(request):
    tags = Tag.objects.order_by('name')
    return render(request, 'notes/tag_list.html', {'tags': tags})

def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    notes = Note.objects.filter(tag=tag).order_by('-id')
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})
