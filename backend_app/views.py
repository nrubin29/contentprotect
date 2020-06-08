import imagehash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template import loader
from PIL import Image

from backend_app.models import HashedImage, ImageMatch


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(resolve_url('home'))

    else:
        return HttpResponseRedirect(resolve_url('login'))


@login_required(login_url='/login')
def home(request):
    template = loader.get_template('home.html')
    context = {
        'me': request.user,
        'my_images': HashedImage.objects.filter(user=request.user),
        'my_matches': ImageMatch.objects.filter(hashed_image__user=request.user),
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login')
def add(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        HashedImage.objects.create(
            user=request.user,
            name=request.POST['name'],
            image_hash=imagehash.average_hash(Image.open(image_file)),
        )
        return HttpResponseRedirect(resolve_url('home'))

    template = loader.get_template('add.html')
    context = {
        'me': request.user,
    }
    return HttpResponse(template.render(context, request))
