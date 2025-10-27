from django.db import models
from django.contrib.auth.models import User
from mixins.models import TimestampMixin, SoftDeleteMixin

class Role(TimestampMixin, models.Model):
    nome = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nome do Papel'
    )

    class Meta:
        verbose_name = 'Papel'
        verbose_name_plural = 'Papéis'

    def __str__(self):
        return self.nome

class UserRole(TimestampMixin, models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_roles',
        verbose_name='Usuário'
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name='role_users',
        verbose_name='Papel'
    )

    class Meta:
        verbose_name = 'Papel do Usuário'
        verbose_name_plural = 'Papéis dos Usuários'
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.role.nome}"

class Profile(SoftDeleteMixin ,TimestampMixin, models.Model):
    """
    Caso queira separar dados extras do usuário/cadastro.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Usuário'
    )

    First_name = models.CharField(
        max_length=100,
        verbose_name='Nome',
        default='Não informado'

    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Sobrenome',
        default='Não informado'
    )

    email = models.EmailField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        verbose_name='E-mail'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Avatar'
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return self.nome or self.user.username
