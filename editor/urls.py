from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'editor'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^crop$', views.EditorView.as_view(), name='editorView'),
    url(r'^imageskin/(?P<id>[0-9]+)/(?P<page>[0-9]+)/$', views.loadImageskin, name='loadImageskin'),
    url(r'^viewImageskin/(?P<id>[0-9]+)/$', login_required(views.viewImageskin), name='viewImageskin'),
    url(r'^saveCoord$', views.saveCoord, name='saveCoord'),
    url(r'^createCropImage/(?P<idx>[0-9]+)/$', views.createCropImage, name='createCropImage'),
    url(r'^transform_coord/(?P<idx>[0-9]+)/(?P<scale>[0-9]+)/$', views.transformCoord, name='transformCoord'),
    url(r'^generateCropAll/(?P<scale>[0-9]+)/(?P<directory>[\w\-]+)/(?P<resize>[0-9]+)/(?P<type>[\w\-]+)/(?P<select>[\w\-]+)/$', views.generateCropAll, name='generateCropAll'),
    url(r'^changeSelect$', views.changeSelect, name='changeSelect'),
    url(r'^count_crop_image$', views.count_crop_image_by_disease, name='count_crop_image_by_disease'),
]
