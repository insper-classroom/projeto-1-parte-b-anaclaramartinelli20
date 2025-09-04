from django.shortcuts import render, redirect
from .models import Note

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
