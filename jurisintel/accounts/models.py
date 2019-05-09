# from auditlog.registry import auditlog
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


# class Escritorio(RandomPrimaryIdModel):
#     CRYPT_KEY_LEN_MIN = 5
#     CRYPT_KEY_LEN_MAX = 12
#
#     id = models.CharField(max_length=CRYPT_KEY_LEN_MAX + 1, unique=True, primary_key=True)
#     created_at = models.DateTimeField('Data de cadastro', default=timezone.now)
#
#     class Meta:
#         abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField('Nome', max_length=30)
    last_name = models.CharField('Sobrenome', max_length=80)
    email = models.EmailField('E-mail', max_length=255, unique=True)
    birthdate = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField('Staff - status', default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('Usuário ativo', default=True,
                                    help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('Data de inscrição', default=timezone.now)
    is_trusty = models.BooleanField('E-mail foi confirmado?', default=False,
                                    help_text='Designates whether this user has confirmed his account.')
    codigo_adesao = models.CharField('Código da adesão', max_length=32, blank=True)
    situacao_adesao = models.CharField('Situação da adesão', max_length=32, blank=True)
    telefone_contato = models.CharField('Telefone para contato', max_length=11, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthdate']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, 'nao_responda@Jurisintel.com.br', [self.email])

    @property
    def full_name(self):
        "Returns user full name"
        return '%s %s' % (self.first_name, self.last_name)


class Planos(models.Model):

    tipo = models.CharField(max_length=7, blank=True)
    preco = models.FloatField(blank=True)
    periodo = models.IntegerField(blank=True)

    def __str__(self):
        return 'Plano: %s. Valor: R$%s' % (self.tipo, self.preco)


class PlanGroup(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    plan = models.ForeignKey(Planos, on_delete=models.DO_NOTHING, blank=True)
    trial_status = models.BooleanField(blank=True)
    status_assinatura = models.BooleanField(blank=True)
    end_date = models.DateTimeField(blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_login_step = models.BooleanField(default=False)
    first_case_step = models.BooleanField(default=False)

    def __str__(self):
        return 'Usuário: %s - %s' % (self.user.full_name, self.user.email)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    instance.profile.save()

# auditlog.register(LawFirm)
