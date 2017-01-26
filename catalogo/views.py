from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic, View
from .models import Category, Disease, Imageskin, Sourcedata, Commentimage
from .forms import ImageskinForm
from django.db.models import Count
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import time

# Create your views here.


class IndexView (generic.ListView):
    template_name = 'catalogo/category.html'
    context_object_name = 'list'

    def get_queryset(self):
        return Category.objects.all()


def ObservView (request):
    imageskin = Imageskin.objects.all().filter(state=0)
    total = imageskin.count()
    template_name = 'catalogo/observ.html'
    images = render_to_string('catalogo/ajax/grid-image.html', {'imageskin': imageskin, 'userLog': True})
    return render(request, template_name, {'images': images, 'total':total})


class DiseasesView(generic.DetailView):
    model = Category
    template_name = 'catalogo/diseases.html'


class ImageskinView(generic.DetailView):
    model = Disease
    template_name = 'catalogo/imageskin.html'


def loadImageskin(request, id, page):

    if request.user.is_authenticated():
        userLog = True
    else:
        userLog = False

    image_list = Imageskin.objects.all().filter(disease=id)
    paginator = Paginator(image_list,15)
    data = {}
    if int(page) <= paginator.num_pages:
        try:
            imageskin = paginator.page(page)
        except PageNotAnInteger:
            imageskin = paginator.page(1)
        except EmptyPage:
            imageskin = paginator.page(paginator.num_pages)

        # usuario = User.is_authenticated
        data['data'] = render_to_string('catalogo/ajax/grid-image.html', {'imageskin': imageskin, 'userLog': userLog})
    else:
        data['data'] = False

    # time.sleep(1)
    return JsonResponse(data)


def viewImageskin(request, id):
    userLogId = request.user.id
    image = Imageskin.objects.get(id=id)
    message = Commentimage.objects.all().filter(imageskin=id)
    return render(request,'catalogo/ajax/view-image.html', {'image': image, 'message': message, 'userLogId': userLogId})


class ResultsView(generic.DetailView):
    model = Category
    template_name = 'catalogo/results.html'


class DragAndDropUploadView(View):

    def get(self, request):
        if request.user.is_superuser:
            disease_list = Disease.objects.all()
            source_list = Sourcedata.objects.all()
            image_list = Imageskin.objects.all()
            template_name = 'catalogo/drag_and_drop_upload.html'
            return render(self.request, template_name,
                          {'images': image_list, 'diseases': disease_list, 'sources': source_list})
        else:
            template_name = 'catalogo/404.html'
            return render(self.request, template_name)

    def post(self, request):
        form = ImageskinForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()

            data = {'is_valid': True, 'name': photo.docfile.name, 'url': photo.docfile.url}
        else:
            data = {'is_valid': False, 'msg': "Formulario incompleto."}
        return JsonResponse(data)

# def index(request):
#     _list = Category.objects.all()
#     context = {'list': _list}
#     return render(request, 'catalogo/index2.html',context)
#
#
# def detail(request, category_id):
#     category = get_object_or_404(Category,pk=category_id)
#     return render(request, 'catalogo/detail.html',{'category':category})

# def results(request, category_id):
#     category = get_object_or_404(Category, pk=category_id)
#     return render(request, 'catalogo/results.html', {'category': category})


def getStatusCategory(request):

    a = Imageskin.objects.values('disease__category').annotate(Count('disease__category'))

    idc = list(a.values_list('disease__category__id'))
    name = list(a.values_list('disease__category__name'))
    count = list(a.values_list('disease__category__count'))

    # return render(request, 'catalogo/results.html', {'data': JsonResponse(data)})

    data = {}
    data['datasets'] = {}
    # data['datasets']['data'] = [(200,),(50,),(600,),(150,),(410,)]
    data['datasets']['data'] = count
    # data['datasets']['backgroundColor'] = ['#ff6384','#ff9f40','#ffcd56','#4bc0c0','#36a2eb']
    data['datasets']['backgroundColor'] = ['#ff6384','#ff9f40','#ffcd56','#4bc0c0','#36a2eb']
    data['datasets']['label'] = 'Categoria'
    # data['labels'] = ["Red","Orange","Yellow","Green", "Blue"]
    data['labels'] = name
    data['idc'] = idc
    return JsonResponse(data)


def getStatusDisease_by_Category(request,id):

    a = Imageskin.objects.values('disease', 'disease__category').annotate(Count('disease')).filter(disease__category=id)

    # idc = list(a.values_list('disease__category__id'))
    name = list(a.values_list('disease__name'))
    count = list(a.values_list('disease__count'))

    data = {}
    data['datasets'] = {}
    data['datasets']['data'] = count
    data['datasets']['backgroundColor'] = ['#ff6384','#ff9f40','#ffcd56','#4bc0c0','#36a2eb']
    data['datasets']['label'] = 'Por tipo'
    data['labels'] = name
    return JsonResponse(data)


def getStatusSource_by_Category(request,id):

    a = Imageskin.objects.values('sourcedata', 'disease__category').annotate(Count('sourcedata')).filter(
        disease__category=id)

    # idc = list(a.values_list('disease__category__id'))
    name = list(a.values_list('sourcedata__name'))
    count = list(a.values_list('sourcedata__count'))

    data = {}
    data['datasets'] = {}
    data['datasets']['data'] = count
    data['datasets']['backgroundColor'] = ['#ff6384','#ff9f40','#ffcd56','#4bc0c0','#36a2eb']
    data['datasets']['label'] = 'Por fuente'
    data['labels'] = name
    return JsonResponse(data)


def changeState(request):

    model_opc = request.POST['model']
    idc = request.POST['id']
    data_state = request.POST['state']

    if model_opc == 'category':
        model_aux = get_object_or_404(Category, pk=idc)
    elif model_opc == 'disease':
        model_aux = get_object_or_404(Disease, pk=idc)
    elif model_opc == 'imageskin':
        model_aux = get_object_or_404(Imageskin, pk=idc)

    if data_state == "true":
        data_state = True
    else:
        data_state = False

    model_aux.state = data_state
    model_aux.save()

    data = {}
    data['status'] = True
    data['state'] = data_state
    data['msg'] = 'Cambio realizado.'
    return JsonResponse(data)


def state(request, category_id):
    category = get_object_or_404(Category,pk=category_id)

    if 'state' in request.POST:
        value = True
    else:
        value = False

    category.state = value
    category.save()

    return HttpResponseRedirect(reverse('catalogo:results', args=(category_id,)))


def commentPush(request):

    data = {}
    if request.user.is_authenticated():
        userLog = request.user.id
    else:
        userLog = False

    idU = User.objects.get(pk=request.user.id)
    idI = Imageskin.objects.get(pk=request.POST['idx'])
    text = request.POST['text']
    textCount = len(text)

    if textCount == 0:
        data['status'] = False
        data['msg'] = 'Debe digitar un mensaje'

    elif textCount > 400:
        data['status'] = False
        data['msg'] = 'El mensaje solo puede contener 400 caracteres'

    else:

        comment = Commentimage(user=idU, imageskin=idI, text=text)
        comment.save()

        data['status'] = True
        data['nameshort'] = idU.first_name.capitalize()[:1] + idU.last_name.capitalize()[:1]
        data['nameUser'] = idU.first_name.capitalize() + ' ' + idU.last_name.capitalize()[:1] + '.'
        # data['pub_date'] = comment.pub_date.strftime("%d/%m/%y %H:%M")

    return JsonResponse(data)
