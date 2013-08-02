from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.views.generic import CreateView, DeleteView

from . import models

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

@permission_required('galleries.change_galleryimage')
def manage_gallery(request, id):
	gallery = models.Gallery.objects.get(pk=id)
	images = models.GalleryImage.objects.filter(gallery=gallery).order_by('order')
	
	if request.method == 'POST':
		print request.FILES
		galleryImage = models.GalleryImage(image = request.FILES['file'], gallery=gallery)
		galleryImage.save()
		
	return render(request, "galleries/gallery.html", {'gallery': gallery, 'images': images})

@permission_required('galleries.change_galleryimage')
def take_upload(request):
	form = UploadImageform(request.POST, request.FILES)
	
	if form.is_valid():
		return "Valid!"