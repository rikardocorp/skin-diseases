from django.shortcuts import render, get_object_or_404
from skinWeb.settings import BASE_DIR
import os, shutil
# Create your views here.
from django.template.loader import render_to_string
from catalogo.models import Imageskin, Disease, Category
from editor.models import CropImage
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from django.views import generic, View
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from PIL import Image
from skinWeb.settings import BASE_DIR
from django.db.models import Count
import re


class Coordinate(object):
    def __init__(self, x, y, width, height, orig_w, orig_h):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.originalWidth = orig_w
        self.originalHeight = orig_h

    def show(self):
        return [self.x, self.y, self.width, self.height]


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class EditorView (generic.ListView):
    template_name = 'editor/tree.html'
    context_object_name = 'list'

    def get_queryset(self):
        return Disease.objects.all().order_by('category')


def count_crop_image_by_disease(request):
    opc = request.POST['opc']

    if int(opc) == 0:
        a = Imageskin.objects.values('disease').annotate(Count('disease')).filter(select=True)
    else:
        a = Imageskin.objects.values('disease').annotate(Count('disease'))

    id = list(a.values_list('disease__id'))
    # name = list(a.values_list('disease__name'))
    count = list(a.values_list('disease__count'))

    data = {}
    data['id'] = id
    # data['name'] = name
    data['count'] = count

    return JsonResponse(data)


def loadImageskin(request, id, page):

    if request.user.is_authenticated:
        userLog = True
    else:
        userLog = False

    image_list = Imageskin.objects.all().filter(disease=id)
    paginator = Paginator(image_list, 15)
    data = {}
    if int(page) <= paginator.num_pages:
        try:
            imageskin = paginator.page(page)
        except PageNotAnInteger:
            imageskin = paginator.page(1)
        except EmptyPage:
            imageskin = paginator.page(paginator.num_pages)

        # usuario = User.is_authenticated
        data['data'] = render_to_string('editor/ajax/grid-image.html', {'imageskin': imageskin, 'userLog': userLog})
    else:
        data['data'] = False

    # time.sleep(1)
    return JsonResponse(data)


def viewImageskin(request, id):
    userLogId = request.user.id
    image = Imageskin.objects.get(id=id)

    try:
        crop = CropImage.objects.get(imageskin=image)
    except:
        crop = False

    return render(request, 'editor/ajax/view-image-editor.html', {'image': image, 'crop': crop, 'userLogId': userLogId})


def saveCoord(request):

    x = request.POST['x']
    y = request.POST['y']
    w = request.POST['width']
    h = request.POST['height']
    orig_w = request.POST['originalWidth']
    orig_h = request.POST['originalHeight']
    idImage = request.POST['imageskin']
    transform = request.POST['transform']

    image = Imageskin.objects.all().filter(id=idImage)[0]
    data = {}

    a = image.id
    crop = CropImage.objects.all().filter(imageskin=image)
    if crop:
        # Existe
        crop = crop[0]
        crop.x = x
        crop.y = y
        crop.width = w
        crop.height = h
        crop.originalWidth = orig_w
        crop.originalHeight = orig_h
        crop.transform = transform
        crop.save()
        data['status'] = 'Update'
    else:
        # No existe
        newCrop = CropImage(imageskin=image, x=x, y=y, width=w, height=h, originalWidth=orig_w, originalHeight=orig_h, transform=transform)
        newCrop.save()
        data['status'] = 'Create'

    return JsonResponse(data)


def generate_imageskin_directories(opc):

    if opc == 'category':
        List = Category.objects.all()
        for idx in List:
            generate_imageskin_directory_by_category(idx.id)

        print('Directorio de Imagenes por Categoria creado!.')

    elif opc == 'disease':
        List = Disease.objects.all()
        for idx in List:
            generate_imageskin_directory_by_disease(idx.id)

        print('Directorio de Imagenes por tipo de enfermedad creado!.')

    else:
        print('No existe esta opción.')


def createCropImage(request, idx):

    img = Imageskin.objects.get(id=idx)
    nameLong = img.docfile.name
    nameShort = nameLong.split('/')[1].split('.')[0]
    data = {}

    try:
        crop = CropImage.objects.get(imageskin=idx)
        # data['state'] = 'coordenadas.'
    except:
        data['state'] = 'Debe guardar las coordenadas.'
        return JsonResponse(data)

    imgOpen = Image.open(img.docfile)
    cropped_image = imgOpen.crop((crop.x, crop.y, crop.width + crop.x, crop.height + crop.y))
    # resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)

    pathShort = 'crop/' + nameShort + '.jpg'
    pathLong = BASE_DIR+'/media/' + pathShort

    try:
        cropped_image.save(pathLong)
        crop.path = pathShort
        crop.save()
        data['state'] = True

    except:
        data['state'] = False

    return JsonResponse(data)


def transformCoord(request, idx, scale):

    data = {}
    try:
        crop = CropImage.objects.get(imageskin=idx)
        data['state'] = 'coordenadas.'
    except:
        data['state'] = 'Debe guardar las coordenadas.'
        return JsonResponse(data)

    # Coordenadas Originales
    data['original'] = {'x': crop.x,
                        'y': crop.y,
                        'w': crop.width,
                        'h': crop.height}

    # Coordenadas de cuadrado
    dif = abs((crop.height - crop.width) / 2)
    if crop.width < crop.height:
        crop.x = int(crop.x - dif)
        crop.width = crop.height
    else:
        crop.y = int(crop.y - dif)
        crop.height = crop.width

    data['recuadro'] = {'x': crop.x,
                        'y': crop.y,
                        'w': crop.width,
                        'h': crop.height}

    # Coordenadas con escala
    incremento = crop.width * float(int(scale)/100)
    crop.width = int(crop.width + incremento)
    crop.height = crop.width
    crop.x = crop.x - int(incremento / 2)
    crop.y = crop.y - int(incremento / 2)

    data['escala'] = {'x': crop.x,
                      'y': crop.y,
                      'w': crop.width,
                      'h': crop.height}

    # Casos de desborde
    if crop.x < 0:
        aux = abs(crop.x)
        crop.x = 0
        crop.y = crop.y + aux
        crop.width = crop.width - 2 * aux
        crop.height = crop.height - 2 * aux

    if crop.y < 0:
        aux = abs(crop.y)
        crop.x = crop.x + aux
        crop.y = 0
        crop.width = crop.width - 2 * aux
        crop.height = crop.height - 2 * aux

    if (crop.x + crop.width) > crop.originalWidth:
        aux = (crop.x + crop.width) - crop.originalWidth
        crop.x = crop.x + aux
        crop.y = crop.y + aux
        crop.width = crop.width - 2 * aux
        crop.height = crop.height - 2 * aux

    if (crop.y + crop.height) > crop.originalHeight:
        aux = (crop.y + crop.height) - crop.originalHeight
        crop.x = crop.x + aux
        crop.y = crop.y + aux
        crop.width = crop.width - 2 * aux
        crop.height = crop.height - 2 * aux

    data['corregido'] = {'x': crop.x,
                         'y': crop.y,
                         'w': crop.width,
                         'h': crop.height}

    return JsonResponse(data)


def changeSelect(request):
    data = {}
    model_opc = request.POST['model']
    idc = request.POST['id']
    data_select = request.POST['select']

    model_aux = get_object_or_404(Imageskin, pk=idc)

    if data_select == "true":
        data_select = True
        # try:
        #     crop = CropImage.objects.get(imageskin=idc)
        # except:
        #     data['status'] = False
        #     data['msg'] = 'Debe guardar las coordenadas.'
        #     return JsonResponse(data)
    else:
        data_select = False

    model_aux.select = data_select
    model_aux.save()

    data['status'] = True
    data['select'] = data_select
    data['msg'] = 'Cambio realizado.'
    return JsonResponse(data)


# Generar Imagenes por Categorias y Enfermedades

def generateCropAll(request, scale, directory, resize, type, select):
    data = {}
    images_list = []
    select = select.split('o')
    for idx in select:
        listAux = CropImage.objects.all().filter(imageskin__select=True).filter(imageskin__disease__category=idx)
        images_list.extend(listAux)

    data['total'] = len(images_list)
    resize = int(resize)

    # Creamos el directorio
    directory_exist(BASE_DIR + '/media/' + directory + '/')
    if type == 'category' or type == 'disease':
        generateDirectory(type, directory)

    # Procesamiento de imagenes
    for image in images_list:
        id = image.imageskin.id
        data[id] = {}
        data[id]['name'] = str(id) + str(image.imageskin.name)

        file_image = image.imageskin.docfile
        nameLong = image.imageskin.docfile.name
        nameShort = nameLong.split('/')[1].split('.')[0]

        # Resize coord crop
        crop = Coordinate(image.x,image.y,image.width,image.height,image.originalWidth, image.originalHeight)
        crop = adjustCoord(crop,scale)

        # Crop Image
        imgOpen = Image.open(file_image)
        cropped_image = imgOpen.crop((crop.x, crop.y, crop.width + crop.x, crop.height + crop.y))

        if resize > 50:
            resized_image = cropped_image.resize((resize, resize), Image.ANTIALIAS)
            new_image = resized_image
        else:
            new_image = cropped_image

        # Para asignar la sub carpeta
        if type == 'category':
            subDir = image.imageskin.disease.category.name + '_' + str(image.imageskin.disease.category.id)
            subDir = re.sub(r"[^A-Za-z0-9]+", "_", subDir, 0)
            pathShort = directory + '/' + subDir + '/' + nameShort
            pathCSV = directory + '/' + subDir + '/' + subDir + '.csv'
            label = image.imageskin.disease.id

        elif type == 'disease':
            subDir = image.imageskin.disease.name + '_' + str(image.imageskin.disease.id)
            subDir = re.sub(r"[^A-Za-z0-9]+", "_", subDir, 0)
            pathShort = directory + '/' + subDir + '/' + nameShort
            pathCSV = directory + '/' + subDir + '/' + subDir + '.csv'
            label = image.imageskin.disease.id

        else:
            pathShort = directory + '/' + nameShort
            pathCSV = directory + '/Default.csv'
            label = image.imageskin.disease.id

        pathLong = BASE_DIR + '/media/' + pathShort
        pathLongCSV = BASE_DIR + '/media/' + pathCSV

        transform = image.transform
        if transform == '':
            data[id]['state'] = saveCropImage(new_image, image, nameShort, pathLong+'.jpg', pathLongCSV, label)
        else:
            res = list(map(int, transform.split('_')))

            if res[0] == 1:
                data[id]['90'] = saveCropImage(new_image, image, nameShort+'_0', pathLong+'_0.jpg', pathLongCSV, label)
            if res[1] == 1:
                imgAux = new_image.rotate(90)
                data[id]['90'] = saveCropImage(imgAux, image, nameShort+'_90', pathLong+'_90.jpg', pathLongCSV, label)
            if res[2] == 1:
                imgAux = new_image.rotate(180)
                data[id]['90'] = saveCropImage(imgAux, image, nameShort+'_180', pathLong+'_180.jpg', pathLongCSV, label)
            if res[3] == 1:
                imgAux = new_image.rotate(270)
                data[id]['90'] = saveCropImage(imgAux, image, nameShort+'_270', pathLong+'_270.jpg', pathLongCSV, label)

    return JsonResponse(data)


def saveCropImage(new_image, image, nameImage, pathDest, pathCsv, label):

    try:
        new_image.save(pathDest)
        image.path = nameImage
        image.save()
        result = True

        f = open(pathCsv, "a+")
        f.write(",".join(map(str, [nameImage, label])) + "\n")
        f.close()
        print(nameImage + '.jpg')

    except:
        result = False
        print('Error: ', nameImage + '.jpg')
    return result


def generateDirectory(type, directory):

    if type == 'category':
        data = Category.objects.all()
    elif type == 'disease':
        data = Disease.objects.all()

    for di in data:
        name = di.name + '_' + str(di.id)
        name = re.sub(r"[^A-Za-z0-9]+", "_", name, 0)
        directory_exist(BASE_DIR + '/media/' + directory + '/' + name + '/')


def adjustCoord(crop, scale):

    # Coordenadas de cuadrado
    # -----------------------
    dif = abs((crop.height - crop.width) / 2)
    if crop.width < crop.height:
        crop.x = int(crop.x - dif)
        crop.width = crop.height
    else:
        crop.y = int(crop.y - dif)
        crop.height = crop.width

    # Coordenadas con escala
    # ----------------------
    incremento = crop.width * float(int(scale) / 100)
    crop.width = int(crop.width + incremento)
    crop.height = crop.width
    crop.x = crop.x - int(incremento / 2)
    crop.y = crop.y - int(incremento / 2)

    # Casos de desborde
    # -----------------
    if crop.x < 0:
        aux = abs(crop.x)
        crop.x = 0
        crop.y = crop.y + aux
        crop.width = crop.width - 2 * aux
        crop.height = crop.height - 2 * aux

    if crop.y < 0:
        aux = abs(crop.y)
        crop.x = crop.x + aux
        crop.y = 0
        crop.width = crop.width - 2 * aux
        crop.height = crop.height - 2 * aux

    if (crop.x + crop.width) > crop.originalWidth:
        aux = (crop.x + crop.width) - crop.originalWidth
        crop.x = crop.x + aux
        crop.y = crop.y + aux
        crop.width = crop.width - 2 * aux
        crop.height = crop.height - 2 * aux

    if (crop.y + crop.height) > crop.originalHeight:
        aux = (crop.y + crop.height) - crop.originalHeight
        crop.x = crop.x + aux
        crop.y = crop.y + aux
        crop.width = crop.width - 2 * aux
        crop.height = crop.height - 2 * aux

    return crop


def generate_imageskin_directory_by_category(index):

    listFile  = Imageskin.objects.all().filter(disease__category=index)
    root_dest = os.path.join(BASE_DIR,'media','temp','category_'+str(index))
    directory_exist(root_dest)
    for file in listFile:
        image_source = file.docfile._get_path()
        shutil.copy(image_source,root_dest)


def generate_imageskin_directory_by_disease(index):

    listFile  = Imageskin.objects.all().filter(disease=index)
    root_dest = os.path.join(BASE_DIR,'media','temp','disease_'+str(index))
    directory_exist(root_dest)
    for file in listFile:
        image_source = file.docfile._get_path()
        shutil.copy(image_source,root_dest)


def directory_exist(pathname):
    directory = Path(pathname)
    if not directory.exists():
        os.makedirs(pathname)
        print('El directorio {0} ha sido creado.'.format(pathname))
    else:
        print('El directorio {0} existe.'.format(pathname))
