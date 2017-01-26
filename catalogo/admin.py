from django.contrib import admin
from .models import Category, Disease, Imageskin, Sourcedata, Commentimage
# Register your models here.

# Superuser
# Username: rikardocorp
# contraseña : rcorp***8

class ChoiceInline(admin.TabularInline):
    model = Disease
    extra = 2

class CategoryAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['name']}),
        ('Data Information', {'fields': ['state','pub_date']}),
    ]

    inlines = [ChoiceInline]
    list_display = ('name', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['name']
    # fields = ['pub_date', 'name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Disease)
admin.site.register(Imageskin)
admin.site.register(Sourcedata)
admin.site.register(Commentimage)
