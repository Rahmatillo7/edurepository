from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.resources.models import Resource
from .models import Comment, Favorite, Report


@login_required
def add_comment(request, resource_id):
    if request.method == "POST":
        resource = get_object_or_404(Resource, id=resource_id)
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, resource=resource, text=text)
    return redirect('resources:detail', pk=resource_id)


@login_required
def toggle_favorite(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, resource=resource)

    if not created:
        favorite.delete()

    return redirect('resources:detail', pk=resource_id)
