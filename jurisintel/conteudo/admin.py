from django.contrib import admin
from django import forms
from django.contrib.admin import AdminSite
from django.conf.urls import url
from .models import *
from .views import TemasView, get_tema_admin, edit_tema, CaseAdminView
# Register your models here.


class TemaSite(AdminSite):
    def get_urls(self):
        urls = super(TemaSite, self).get_urls()
        custom_urls = [
            url(r'^temas/$', self.admin_view(TemasView.as_view()), name='temas'),
            url(r'^find-tema/$', self.admin_view(get_tema_admin), name='get_tema'),
            url(r'^edit_tema/$', self.admin_view(edit_tema), name='edit_tema'),
        ]
        return urls + custom_urls


class CaseSite(AdminSite):
    def get_urls(self):
        urls = super(CaseSite, self).get_urls()
        custom_urls = [
            url(r'^casos/$', self.admin_view(CaseAdminView.as_view()), name='casos'),
        ]
        return urls + custom_urls


class CaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'titulo', 'created_at']
    raw_id_fields = ['ementas']


# admin_site = TemaSite(name='temas_admin')
admin_site = CaseSite(name='cases_admin')
admin.site.register(File)
admin.site.register(Ementa)
admin.site.register(Case, CaseAdmin)
admin.site.register(Tags)
admin.site.register(Tema)
admin.site.register(Thumbnail)
