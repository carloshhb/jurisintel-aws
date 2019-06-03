import secrets

from accounts.models import User
from django.db import models
from django.dispatch import receiver
from jurisintel.storage_backends import PublicMediaStorage, ThumbnailStorage

from .random_primary import RandomPrimaryIdModel


# Create your models here.


class Ementa(models.Model):
    orgao = models.CharField(max_length=150, blank=True, null=True)
    texto = models.TextField()
    citacao = models.CharField(max_length=255, blank=True, null=True)
    data_sessao = models.DateField(blank=True, null=True)
    tipo_recurso = models.CharField(max_length=150, blank=True, null=True)
    numero_processo = models.CharField(max_length=150, blank=True, null=True)
    numero_acordao = models.CharField(max_length=150, blank=True, null=True)
    relator = models.CharField(max_length=150, blank=True, null=True)
    materia = models.CharField(max_length=255, blank=True, null=True)
    decisao = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.texto


class Thumbnail(models.Model):
    thumbnail = models.ImageField(storage=ThumbnailStorage(), max_length=255)

    def __str__(self):
        return '%s' % self.thumbnail


class File(models.Model):
    file = models.FileField(max_length=255)
    thumbnail = models.ForeignKey(Thumbnail, null=True, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    resumo = models.TextField(null=True)

    def __str__(self):
        return '%s' % self.file

    # def save(self, *args, **kwargs):
    #     super(File, self).save(*args, **kwargs)
    #     self.generate_thumbnail()
    #
    # def generate_thumbnail(self):
    #     file = str(self.file)
    #     pdf = wi(filename=file, resolution=300)
    #     thumbnail_image = pdf.convert("jpeg")
    #
    #     thumbnail_name = '%s.%s' % (file.split('.pdf')[0], 'jpg')
    #
    #     with thumbnail_image.sequence[0] as img:
    #         page = wi(image=img)
    #         resized_img = page.resize(200, 150)
    #         resized_img.save(filename=thumbnail_name)
    #
    #     thumbnail = Thumbnail()
    #     thumbnail.thumbnail = resized_img
    #
    #     self.thumbnail = thumbnail.save()
    #     # self.save()


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from Fileystem
    when model object is deleted
    """
    if instance.file:
        s3 = PublicMediaStorage()
        if s3.exists(instance.file.name):
            s3.delete(instance.file.name)


class Tags(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % self.tag


class Case(RandomPrimaryIdModel):
    CRYPT_KEY_LEN_MIN = 5
    CRYPT_KEY_LEN_MAX = 12

    id = models.CharField(max_length=CRYPT_KEY_LEN_MAX + 1, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    docs = models.ManyToManyField(File, blank=True)
    ementas = models.ManyToManyField(Ementa, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    resumo = models.TextField()
    titulo = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_creation = models.BooleanField(default=False)

    def __str__(self):
        return '%s: %s' % (self.titulo, self.user.first_name)


@receiver(models.signals.pre_delete, sender=Case)
def auto_delete_arquivo_on_delete(sender, instance, **kwargs):
    """
    Deletes file from Fileystem
    when model object is deleted
    """
    File = instance.docs.all()
    for file in File:
        file.delete()


def gerar_id_code():
    return secrets.token_hex(8)


class Tema(models.Model):

    titulo_tema = models.CharField(max_length=255)
    descricao_tema = models.TextField()
    documentos = models.ManyToManyField(File, blank=True)
    ementas = models.ManyToManyField(Ementa, blank=True)
    identifier_code = models.CharField(max_length=150, unique=True, default=gerar_id_code())
    usuarios = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return '%s' % self.titulo_tema

# class Escritorio(RandomPrimaryIdModel):
#     CRYPT_KEY_LEN_MIN = 5
#     CRYPT_KEY_LEN_MAX = 12
#
#     id = models.CharField(max_length=CRYPT_KEY_LEN_MAX + 1, unique=True, primary_key=True)
#     created_at = models.DateTimeField('Data de cadastro', default=timezone.now)
#     membros = models.ManyToManyField(User, blank=True)
#     cases = models.ManyToManyField(Case, blank=True)
