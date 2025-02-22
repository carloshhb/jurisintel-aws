# Register your models here.
from django.contrib import admin
from django import forms
# Register your models here.
from .models import User, PlanGroup, Plano, Profile, Escritorio


class UserAdmin(admin.ModelAdmin):
    
    def ativar_bulk(self, request, queryset):
        quantidade = queryset.count()
        for obj in queryset:    
            obj.situacao_adesao = 'Ativo'
            obj.save()

        message_bit = "%s usuários foram ativados e podem logar no sistema" % quantidade
        self.message_user(request, "%s ativados com sucesso." % message_bit)
    ativar_bulk.short_description = "Ativar usuários selecionados"
    actions = [ativar_bulk]

    list_display = ('email', 'first_name', 'last_name', 'last_login')
    search_fields = ['email', 'first_name', 'last_name']


class EscritorioForm(forms.ModelForm):

    class Meta:
        model = Escritorio
        fields = ['escritorio']


class EscritorioAdmin(admin.ModelAdmin):

    form = EscritorioForm


admin.site.register(User, UserAdmin)
admin.site.register(Plano)
admin.site.register(PlanGroup)
admin.site.register(Profile)
admin.site.register(Escritorio, EscritorioAdmin)
