from django.shortcuts import render
from .models import *

def photos_view(request):
    photos = Photo.objects.filter(user=request.user)
    return render(request,'content/photos.html', {'photos': photos})

def notes_view(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'content/notes.html',{'notes': notes})

def coding_problems_view(request):
    problems = CodingProblem.objects.filter(user=request.user)
    return render(request, 'content/coding_problems.html', {'problems': problems})