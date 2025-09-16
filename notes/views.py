from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Note, Tag


def _split_to_tags(raw: str):
    """
    Recebe a string digitada no input (ex.: "oi, teste ,  escola")
    e retorna uma lista de instâncias Tag (criando quando necessário).
    """
    if not raw:
        return []

    names = [
        # remove espaços extras, ignora vazios
        part.strip()
        for part in raw.split(",")
    ]
    names = [n for n in names if n]

    tags = []
    for name in names:
        tag, _created = Tag.objects.get_or_create(name=name)
        tags.append(tag)
    return tags

def _tags_as_csv(note: Note) -> str:
    """
    Converte as tags da nota para uma string separada por vírgulas,
    usada para pré-popular o campo no edit.
    """
    return ", ".join(note.tags.values_list("name", flat=True))


def index(request):
    if request.method == "POST":
        title = request.POST.get("titulo", "").strip()
        content = request.POST.get("detalhes", "").strip()
        tag_input = request.POST.get("tag", "")

        with transaction.atomic():
            note = Note.objects.create(title=title, content=content)
            # ManyToMany: set após criar a Note
            note.tags.set(_split_to_tags(tag_input))

        return redirect("index")

    # lista com prefetch das tags para evitar N+1
    notes = Note.objects.all().prefetch_related("tags")
    return render(request, "notes/index.html", {"notes": notes})


def delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect("index")


def edit(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":
        note.title = request.POST.get("titulo", "").strip()
        note.content = request.POST.get("detalhes", "").strip()
        note.save()

        tag_input = request.POST.get("tag", "")
        note.tags.set(_split_to_tags(tag_input))

        return redirect("index")

    # GET: renderiza formulário pré-preenchido
    context = {
        "note": note,
        "tags_csv": _tags_as_csv(note),  
    }
    return render(request, "notes/edit.html", context)


def tag_detail(request, name: str):
    """
    Página de uma tag específica mostrando suas notas.
    """
    tag = get_object_or_404(Tag, name=name)
    notes = tag.notes.all().prefetch_related("tags")
    return render(request, "notes/tag_detail.html", {"tag": tag, "notes": notes})


def tag_list(request):
    """
    Lista de todas as tags (opcional, caso você tenha a rota/template).
    """
    tags = Tag.objects.all().order_by("name")
    return render(request, "notes/tag_list.html", {"tags": tags})
