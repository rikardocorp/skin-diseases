from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'catalogo'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^observ$', login_required(views.ObservView), name='observ'),

    url(r'^(?P<pk>[0-9]+)/$',views.DiseasesView.as_view(), name='diseases'),
    # url(r'^(?P<pk>[0-9]+)/$',views.ImageskinView.as_view(), name='imageskin'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<category_id>[0-9]+)/state/$', views.state, name='state'),
    url(r'^changeState$', views.changeState, name='changeState'),
    url(r'^commentPush$', views.commentPush, name='commentPush'),
    url(r'^getStatusCategory$', views.getStatusCategory, name='getStatusCategory'),
    url(r'^getStatusDisease_by_Category/(?P<id>[0-9]+)/$', views.getStatusDisease_by_Category, name='getStatusDisease_by_Category'),
    url(r'^getStatusSource_by_Category/(?P<id>[0-9]+)/$', views.getStatusSource_by_Category,
        name='getStatusSource_by_Category'),

    # url(r'^upload_image$', views.upload_image, name='uploadImage'),
    url(r'^disease/(?P<pk>[0-9]+)/$', views.ImageskinView.as_view(), name='imageskin'),
    url(r'^imageskin/(?P<id>[0-9]+)/(?P<page>[0-9]+)/$', views.loadImageskin, name='loadImageskin'),
    url(r'^viewImageskin/(?P<id>[0-9]+)/$', login_required(views.viewImageskin), name='viewImageskin'),
    url(r'^upload/$', login_required(views.DragAndDropUploadView.as_view()), name='drag_and_drop_upload'),
]