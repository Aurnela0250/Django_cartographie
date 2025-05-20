Hoshiaki40: comment implementer La gestion des utilisateur et la gestion des permisseion dans ma code base ?

### Introduction

Ce rapport fournit une analyse détaillée et exhaustive sur la configuration de la gestion des groupes et des permissions en utilisant le système natif de Django. Il aborde l'implémentation des permissions via les modèles intégrés (User, Group, Permission, et ContentType), la manière d'attribuer et de vérifier les permissions dans le code Django, et l'intégration de ces mécanismes dans Django Ninja Extra. En outre, le rapport présente des exemples complets et des bonnes pratiques pour gérer les groupes d’utilisateurs, ainsi que des conseils d’architecture pour structurer un projet Django selon les principes de la Clean Architecture, en séparant clairement entités, cas d’utilisation, interfaces et implémentations concrètes.

### 1. Gestion native des permissions et groupes dans Django

#### 1.1 Modèles et permissions par défaut

Django fournit un système intégré de gestion des permissions reposant sur plusieurs modèles clés. Le modèle `User` représente l’utilisateur final, tandis que le modèle `Group` permet de regrouper plusieurs utilisateurs et de leur attribuer des permissions collectives. Chaque modèle enregistré dans Django génère automatiquement quatre permissions (add, change, delete, view) qui sont associées au modèle via le modèle `Permission`. Le modèle `ContentType` permet de lier ces permissions aux modèles spécifiques.

Par exemple, si un modèle appelé `Article` est défini, Django crée les permissions `add_article`, `change_article`, `delete_article` et `view_article` automatiquement lors de l’exécution de `makemigrations` et `migrate`.

#### 1.2 Permissions personnalisées

Il est possible de créer des permissions personnalisées en les déclarant dans la classe `Meta` du modèle. Un exemple d’implémentation est le suivant :

from django.db import models

class Document(models.Model):
title = models.CharField(max_length=100)
content = models.TextField()

    class Meta:
        permissions = [
            ('can_publish', 'Can publish documents'),
            ('can_archive', 'Can archive documents'),
        ]

Ces permissions personnalisées viendront s’ajouter aux permissions par défaut et pourront être attribuées aux utilisateurs ou aux groupes, aussi bien via l’administration de Django que par code.

#### 1.3 Attribution et vérification des permissions

Les permissions peuvent être attribuées de manière programmatique. Par exemple, pour ajouter une permission personnalisée à un utilisateur :

from django.contrib.auth.models import User, Permission

user = User.objects.get(username='john')
permission = Permission.objects.get(codename='can_publish')
user.user_permissions.add(permission)

if user.has_perm('app_name.can_publish'):
print("L'utilisateur dispose de la permission de publier.")

Des vérifications similaires peuvent être effectuées au sein des vues, des formulaires ou même dans les templates de Django grâce à la variable `perms` :

```html
{% if perms.app_name.can_publish %}
<p>Vous êtes autorisé à publier des documents.</p>
{% endif %}
```

### 2. Gestion des permissions dans Django Ninja Extra

#### 2.1 Intégration des permissions natives dans les endpoints

Bien que Django Ninja Extra ne fournisse pas un système de permissions aussi complet que Django REST Framework, il propose la possibilité d’intégrer les permissions natives de Django dans les endpoints de l’API. L’utilisation de `user.has_perm('app.permission_codename')` permet de vérifier les permissions directement dans la logique des vues.

#### 2.2 Décorateurs personnalisés pour protéger les routes

L’un des moyens d’intégrer la vérification de permissions consiste à créer des décorateurs personnalisés. Le code ci-dessous illustre un décorateur simple qui vérifie si l’utilisateur authentifié possède la permission requise avant d’exécuter la route :

from django.contrib.auth.models import AnonymousUser
from ninja.errors import HttpError
from http import HTTPStatus

def permission_required(permission_codename):
def decorator(func):
def wrapper(request, *args, \*\*kwargs):
user = getattr(request, 'auth', AnonymousUser)
if not user.has_perm(permission_codename):
raise HttpError(HTTPStatus.FORBIDDEN, "Permission denied")
return func(request, *args, \*\*kwargs)
return wrapper
return decorator

Par exemple, une route protégée dans Django Ninja Extra pourrait ressembler à ceci :

@router.get("/secure-data")
@permission_required('app_name.view_model')
def secure_data(request):
return {"message": "Accès autorisé aux données sécurisées"}

#### 2.3 Utilisation de classes de permission personnalisées

Pour des scénarios plus complexes, il est recommandé d’encapsuler la logique de vérification dans des classes de permission. Ces classes offrent une meilleure réutilisabilité et une clarté dans l’application des règles de sécurité.

class IsSuperUser:
def **init**(self, request, user):
self.request = request
self.user = user

    def has_permission(self):
        return self.user.is_superuser

def permission_required(permission_class):
def decorator(func):
def wrapper(request, *args, \*\*kwargs):
user = getattr(request, 'auth', AnonymousUser)
if not permission_class(request, user).has_permission():
raise HttpError(HTTPStatus.FORBIDDEN, "Permission denied")
return func(request, *args, \*\*kwargs)
return wrapper
return decorator

Cette approche permet de créer des couches de vérification de permission flexibles qui peuvent être appliquées à plusieurs endpoints.

### 3. Gestion des groupes d’utilisateurs dans Django

#### 3.1 Création et attribution des groupes

Les groupes offrent un moyen de regrouper des utilisateurs et de leur attribuer des permissions collectivement. Ils simplifient considérablement la gestion des rôles au sein d'une application.

La création d’un groupe peut se faire via l’interface d’administration ou via du code programmatique :

from django.contrib.auth.models import Group, Permission

# Création d'un groupe

editors_group = Group.objects.create(name='Editors')

# Attribution d’une permission au groupe

publish_permission = Permission.objects.get(codename='can_publish')
editors_group.permissions.add(publish_permission)

Pour ajouter un utilisateur à un groupe :

from django.contrib.auth.models import User

user = User.objects.get(username='john')
editors_group = Group.objects.get(name='Editors')
editors_group.user_set.add(user)

Les utilisateurs héritent automatiquement des permissions définies au niveau du groupe, ce qui permet d’unifier la gestion d’accès et de simplifier la maintenance.

#### 3.2 Utilisation des groupes dans la logique d’accès API

L’appartenance à un groupe peut être vérifiée directement dans le code et utilisée pour contrôler l’accès aux endpoints API. Par exemple, pour restreindre l’accès à un endpoint à un groupe spécifique, la vérification peut se faire ainsi :

# Vérifier l'appartenance à un groupe

if request.user.groups.filter(name='Editors').exists(): # Continuer le traitement de la demande
...
else:
raise HttpError(HTTPStatus.FORBIDDEN, "Accès refusé")

Il est également possible de créer un décorateur spécial ou une classe de permission dédiée pour cette vérification, rendant le code plus réutilisable et cohérent.

### 4. Intégration de la Clean Architecture dans un projet Django

La Clean Architecture vise à séparer les responsabilités en différentes couches, de manière à isoler la logique métier de l'infrastructure et de l'interface utilisateur. Cette approche améliore la maintenabilité, la testabilité et la clarté du code.

#### 4.1 Structure recommandée

Une structure projet typique basée sur la Clean Architecture pourrait être organisée de la manière suivante :

```
project/
├── domain/          # Contient les entités et la logique métier pure
│   ├── models.py
│   ├── services.py
├── usecases/        # Cas d'utilisation qui orchestrent la logique métier
│   ├── user_usecases.py
├── interfaces/      # Interfaces telles que les APIs et les repositories
│   ├── api/
│   │   ├── user_api.py
│   ├── repositories/
│       ├── user_repository.py
├── infrastructure/  # Implémentations concrètes pour l'accès aux données et services externes
│   ├── database/
│   │   ├── user_models.py
│   ├── services/
│       ├── email_service.py
```

Cette séparation permet d’intégrer de manière transparente la gestion des permissions et des groupes dans les cas d’utilisation sans que la logique métier dépende directement de l’implémentation de Django.

#### 4.2 Exemples d’entités et de cas d’utilisation

Une entité représente un objet métier pur et indépendant de l’infrastructure :

# domain/models.py

class User:
def **init**(self, username: str, email: str):
self.username = username
self.email = email

Les cas d’utilisation orchestrent les opérations sur ces entités. Par exemple, pour la création d’un utilisateur :

# usecases/user_usecases.py

class CreateUserUseCase:
def **init**(self, user_repository):
self.user_repository = user_repository

    def execute(self, username, email):
        user = User(username, email)
        self.user_repository.save(user)

#### 4.3 Interfaces et implémentations concrètes

Définir des interfaces permet d’isoler la logique métier des détails d’implémentation. L’interface définit un contrat que l’implémentation concrète devra respecter.

# interfaces/repositories/user_repository.py

class UserRepository:
def save(self, user):
raise NotImplementedError

L’implémentation concrète en utilisant le modèle Django pourra ressembler à :

# infrastructure/database/user_models.py

from django.contrib.auth.models import User as DjangoUser
from interfaces.repositories.user_repository import UserRepository

class DjangoUserRepository(UserRepository):
def save(self, user):
DjangoUser.objects.create(username=user.username, email=user.email)

Cette approche garantit que la logique métier des cas d’utilisation reste indépendante des détails d’implémentation.

### 5. Conseils d’architecture et bonnes pratiques

L’intégration des permissions et des groupes dans un projet Django, tout en respectant les principes de la Clean Architecture, nécessite de suivre certaines bonnes pratiques :

#### 5.1 Séparation claire des responsabilités

Il est crucial de séparer les entités, les cas d’utilisation et les interfaces. Les entités et la logique métier ne doivent pas dépendre des détails d’implémentation de Django. Placer la logique de gestion des permissions au niveau des cas d’utilisation permet de garder ce code indépendant et facilement testable.

#### 5.2 Utilisation de l'injection de dépendances

L’injection de dépendances est essentielle pour isoler et remplacer les implémentations concrètes au moment des tests ou de l’évolution du projet. Par exemple, Django Ninja Extra intègre la notion d’injection de dépendances pour séparer la logique de contrôle de celle de la logique métier.

#### 5.3 Centralisation des permissions et des groupes

Centraliser la gestion des permissions et des groupes dans des services dédiés ou des classes utilitaires permet d’éviter la duplication de code et facilite les modifications futures. Une classe de service peut gérer à la fois l’attribution, la vérification, et la modification des permissions et des groupes.

#### 5.4 Tests unitaires et d'intégration

Chaque couche de l’architecture devrait être testée de manière isolée. Tester les cas d’utilisation de manière unitaire et les implémentations concrètes via des tests d’intégration garantit que la gestion des permissions et des groupes fonctionne correctement dans l’ensemble de l’application.

### 6. Exemple complet d’implémentation

Ce cas pratique illustre comment configurer un endpoint protégé par une permission spécifique et restreint à un groupe, en suivant les principes de la Clean Architecture avec Django Ninja Extra.

#### 6.1 Définition de la permission et création du groupe

Dans un modèle Django, déclarez une permission personnalisée :

# domain/models.py

from django.db import models

class Article(models.Model):
title = models.CharField(max_length=100)
content = models.TextField()

    class Meta:
        permissions = [
            ('can_publish', 'Can publish articles'),
        ]

Créez ensuite un groupe et attribuez-lui cette permission :

# infrastructure/database/setup.py

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from domain.models import Article

# Création du groupe 'Editors'

editors*group, * = Group.objects.get_or_create(name='Editors')

# Attribution de la permission 'can_publish' au groupe

content_type = ContentType.objects.get_for_model(Article)
publish_permission = Permission.objects.get(codename='can_publish', content_type=content_type)
editors_group.permissions.add(publish_permission)

#### 6.2 Définition d’un cas d’utilisation

Un cas d’utilisation pour publier un article pourrait ressembler à :

# usecases/article_usecases.py

class PublishArticleUseCase:
def **init**(self, article_repository):
self.article_repository = article_repository

    def execute(self, article_id, user):
        # Vérifier la permission liée à la publication
        if not user.has_perm('app_name.can_publish'):
            raise Exception("Droits insuffisants pour publier cet article.")
        article = self.article_repository.get(article_id)
        # Logique de publication de l'article
        article.publish()
        self.article_repository.save(article)
        return article

#### 6.3 Implémentation concrète de l’interface API avec Django Ninja Extra

Utilisez Django Ninja Extra pour créer un endpoint protégé par la permission et restreint à un groupe spécifique :

# interfaces/api/article_api.py

from ninja_extra import api_controller, http_post
from ninja_extra.permissions import IsAuthenticated
from django.contrib.auth.models import AnonymousUser
from http import HTTPStatus
from ninja.errors import HttpError

def group_required(group_name):
def decorator(func):
def wrapper(request, *args, \*\*kwargs):
user = getattr(request, 'auth', AnonymousUser)
if not user.groups.filter(name=group_name).exists():
raise HttpError(HTTPStatus.FORBIDDEN, "Groupe requis non présent.")
return func(request, *args, \*\*kwargs)
return wrapper
return decorator

@api_controller('/articles', tags=['Articles'], permissions=[IsAuthenticated])
class ArticleController:
@http_post('/publish/{article_id}')
@group_required('Editors')
def publish_article(self, request, article_id: int): # L'injection ou récupération du repository se fait via le conteneur d'injection ou manuellement
article = publish_article_usecase.execute(article_id, request.user)
return {"message": "Article publié avec succès", "article_id": article_id}

Cet exemple démontre l’intégration complète entre la gestion native des permissions, la gestion des groupes via des décorateurs personnalisés et l’utilisation des principes de la Clean Architecture dans un projet Django.

GitHub Copilot: # Implémentation de la gestion des utilisateurs et des permissions

En analysant votre code existant, je vois que vous avez déjà une bonne base pour l'authentification mais qu'il vous manque la gestion des permissions et des rôles. Je vais vous proposer une solution qui s'intègre parfaitement dans votre architecture.

## 1. Extension des entités et interfaces

### Entité de rôle/permission

D'abord, créons une entité pour représenter les rôles et permissions:

```python
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class PermissionEntity(BaseModel):
    id: Optional[int] = None
    name: str
    codename: str

    model_config = ConfigDict(from_attributes=True)


class RoleEntity(BaseModel):
    id: Optional[int] = None
    name: str
    permissions: List[PermissionEntity] = []

    model_config = ConfigDict(from_attributes=True)
```

### Extension de l'entité utilisateur

Ajoutons les rôles à l'entité utilisateur:

```python
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity


class UserEntity(BaseModel):
    id: Optional[int] = None
    email: str
    password: str
    active: bool = True
    roles: List[RoleEntity] = []
    permissions: List[PermissionEntity] = []
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    def has_permission(self, permission_codename: str) -> bool:
        # Vérification directe des permissions utilisateur
        if any(p.codename == permission_codename for p in self.permissions):
            return True

        # Vérification des permissions via rôles
        for role in self.roles:
            if any(p.codename == permission_codename for p in role.permissions):
                return True

        return False

    def has_role(self, role_name: str) -> bool:
        return any(r.name == role_name for r in self.roles)
```

### Interface du repository de permissions

```python
from abc import abstractmethod
from typing import List, Optional

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.interfaces.unit_of_work import BaseRepository


class PermissionRepository(BaseRepository):
    @abstractmethod
    def create_permission(self, permission: PermissionEntity) -> PermissionEntity:
        pass

    @abstractmethod
    def get_permission_by_codename(self, codename: str) -> Optional[PermissionEntity]:
        pass

    @abstractmethod
    def create_role(self, role: RoleEntity) -> RoleEntity:
        pass

    @abstractmethod
    def get_role_by_name(self, name: str) -> Optional[RoleEntity]:
        pass

    @abstractmethod
    def add_permission_to_role(self, role_name: str, permission_codename: str) -> bool:
        pass
```

### Extension de l'interface du repository utilisateur

```python
from abc import abstractmethod
from typing import List, Optional

from core.domain.entities.user_entity import UserEntity
from core.interfaces.unit_of_work import BaseRepository


class UserRepository(BaseRepository[UserEntity]):
    @abstractmethod
    def create_user(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def add_role_to_user(self, user_id: int, role_name: str) -> bool:
        pass

    @abstractmethod
    def add_permission_to_user(self, user_id: int, permission_codename: str) -> bool:
        pass

    @abstractmethod
    def has_permission(self, user_id: int, permission_codename: str) -> bool:
        pass
```

## 2. Implémentation des repositories Django

### Implémentation du repository de permissions

```python
from typing import List, Optional

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.interfaces.permission_repository import PermissionRepository


class DjangoPermissionRepository(PermissionRepository):

    def create_permission(self, permission: PermissionEntity) -> PermissionEntity:
        # On utilise généralement les permissions créées automatiquement par Django
        # Cette méthode est surtout pour des permissions personnalisées
        app_label, model = permission.codename.split('.')
        content_type = ContentType.objects.get(app_label=app_label, model=model)

        django_permission, created = Permission.objects.get_or_create(
            codename=permission.codename,
            name=permission.name,
            content_type=content_type
        )

        return self._permission_to_entity(django_permission)

    def get_permission_by_codename(self, codename: str) -> Optional[PermissionEntity]:
        try:
            permission = Permission.objects.get(codename=codename)
            return self._permission_to_entity(permission)
        except Permission.DoesNotExist:
            return None

    def create_role(self, role: RoleEntity) -> RoleEntity:
        # Dans Django, les rôles correspondent aux groupes
        group, created = Group.objects.get_or_create(name=role.name)

        # Ajouter les permissions au groupe
        for permission in role.permissions:
            django_permission = Permission.objects.get(codename=permission.codename)
            group.permissions.add(django_permission)

        return self._role_to_entity(group)

    def get_role_by_name(self, name: str) -> Optional[RoleEntity]:
        try:
            group = Group.objects.get(name=name)
            return self._role_to_entity(group)
        except Group.DoesNotExist:
            return None

    def add_permission_to_role(self, role_name: str, permission_codename: str) -> bool:
        try:
            group = Group.objects.get(name=role_name)
            permission = Permission.objects.get(codename=permission_codename)
            group.permissions.add(permission)
            return True
        except (Group.DoesNotExist, Permission.DoesNotExist):
            return False

    def _permission_to_entity(self, django_permission: Permission) -> PermissionEntity:
        return PermissionEntity(
            id=django_permission.id,
            name=django_permission.name,
            codename=django_permission.codename
        )

    def _role_to_entity(self, django_group: Group) -> RoleEntity:
        permissions = [self._permission_to_entity(p) for p in django_group.permissions.all()]
        return RoleEntity(
            id=django_group.id,
            name=django_group.name,
            permissions=permissions
        )
```

### Extension du repository utilisateur Django

```python
from typing import Any, List, Optional
from uuid import UUID

from django.contrib.auth.models import Group, Permission
from apps.users.models import User

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.domain.entities.user_entity import UserEntity
from core.interfaces.user_repository import UserRepository


class DjangoUserRepository(UserRepository):

    def create_user(self, user: UserEntity) -> UserEntity:
        django_user = User(
            email=user.email,
        )
        django_user.set_password(user.password)
        django_user.save()
        return self._to_entity(django_user)

    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            user = User.objects.get(email=email)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        try:
            user = User.objects.get(id=user_id)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        # Vérifier uniquement par email
        user = User.objects.filter(email=login).first()
        if user and user.check_password(password):
            return self._to_entity(user)
        return None

    def add_role_to_user(self, user_id: int, role_name: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name=role_name)
            user.groups.add(group)
            user.save()
            return True
        except (User.DoesNotExist, Group.DoesNotExist):
            return False

    def add_permission_to_user(self, user_id: int, permission_codename: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            permission = Permission.objects.get(codename=permission_codename)
            user.user_permissions.add(permission)
            user.save()
            return True
        except (User.DoesNotExist, Permission.DoesNotExist):
            return False

    def has_permission(self, user_id: int, permission_codename: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            # has_perm vérifie à la fois les permissions directes et celles des groupes
            return user.has_perm(permission_codename)
        except User.DoesNotExist:
            return False

    def _to_entity(self, django_user: User) -> UserEntity:
        # Récupérer les rôles (groupes) de l'utilisateur
        roles = []
        for group in django_user.groups.all():
            permissions = [
                PermissionEntity(id=p.id, name=p.name, codename=p.codename)
                for p in group.permissions.all()
            ]
            roles.append(RoleEntity(id=group.id, name=group.name, permissions=permissions))

        # Récupérer les permissions directes de l'utilisateur
        permissions = [
            PermissionEntity(id=p.id, name=p.name, codename=p.codename)
            for p in django_user.user_permissions.all()
        ]

        return UserEntity(
            id=django_user.id,
            email=django_user.email,
            password="",  # We don't return the password
            active=django_user.active,
            roles=roles,
            permissions=permissions,
            updated_by=django_user.updated_by,
            created_at=django_user.created_at,
            updated_at=django_user.updated_at,
        )

    # ... autres méthodes existantes
```

## 3. Cas d'utilisation pour la gestion des permissions

```python
import logging
from typing import List, Optional

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.interfaces.permission_repository import PermissionRepository
from core.interfaces.unit_of_work import UnitOfWork
from core.interfaces.user_repository import UserRepository


class PermissionUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ):
        self.unit_of_work = unit_of_work
        self.logger = logging.getLogger(__name__)

    def create_role(self, role_name: str) -> RoleEntity:
        """Crée un nouveau rôle"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository

            # Vérifier si le rôle existe déjà
            existing_role = permission_repo.get_role_by_name(role_name)
            if existing_role:
                return existing_role

            # Créer un nouveau rôle
            role = RoleEntity(name=role_name)
            created_role = permission_repo.create_role(role)

            return created_role

    def assign_permission_to_role(
        self, role_name: str, permission_codename: str
    ) -> bool:
        """Assigne une permission à un rôle"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository

            result = permission_repo.add_permission_to_role(
                role_name, permission_codename
            )

            if not result:
                self.logger.warning(
                    f"Échec lors de l'attribution de la permission '{permission_codename}' au rôle '{role_name}'"
                )

            return result

    def assign_role_to_user(self, user_id: int, role_name: str) -> bool:
        """Assigne un rôle à un utilisateur"""
        with self.unit_of_work as uow:
            user_repo = uow.user_repository

            result = user_repo.add_role_to_user(user_id, role_name)

            if not result:
                self.logger.warning(
                    f"Échec lors de l'attribution du rôle '{role_name}' à l'utilisateur ID:{user_id}"
                )

            return result

    def assign_permission_to_user(
        self, user_id: int, permission_codename: str
    ) -> bool:
        """Assigne une permission directement à un utilisateur"""
        with self.unit_of_work as uow:
            user_repo = uow.user_repository

            result = user_repo.add_permission_to_user(
                user_id, permission_codename
            )

            if not result:
                self.logger.warning(
                    f"Échec lors de l'attribution de la permission '{permission_codename}' à l'utilisateur ID:{user_id}"
                )

            return result

    def check_user_permission(
        self, user_id: int, permission_codename: str
    ) -> bool:
        """Vérifie si un utilisateur a une permission spécifique"""
        with self.unit_of_work as uow:
            user_repo = uow.user_repository
            return user_repo.has_permission(user_id, permission_codename)
```

## 4. Mise à jour de l'unité de travail (UnitOfWork)

```python
from core.interfaces.permission_repository import PermissionRepository
from core.interfaces.unit_of_work import UnitOfWork

from infrastructure.db.django_permission_repository import DjangoPermissionRepository
from infrastructure.db.django_user_repository import DjangoUserRepository


class DjangoUnitOfWork(UnitOfWork):
    def __init__(self):
        self._user_repository = None
        self._permission_repository = None

    def __enter__(self):
        # Initialisation des repositories
        self._user_repository = DjangoUserRepository()
        self._permission_repository = DjangoPermissionRepository()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Nettoyage si nécessaire
        self._user_repository = None
        self._permission_repository = None

    @property
    def user_repository(self):
        return self._user_repository

    @property
    def permission_repository(self) -> PermissionRepository:
        return self._permission_repository
```

## 5. Décorateur de permission pour les API

```python
import functools
from typing import Callable

from ninja.errors import HttpError
from http import HTTPStatus


def permission_required(permission_codename: str) -> Callable:
    """
    Décorateur pour vérifier si l'utilisateur a la permission requise.
    À utiliser avec les endpoints Django Ninja.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(controller, request, *args, **kwargs):
            # Vérifier si l'utilisateur est authentifié
            if not hasattr(request, 'auth') or not request.auth:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Non authentifié")

            user_id = request.auth.get("user_id")
            if not user_id:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "ID utilisateur non trouvé")

            # Vérifier la permission
            unit_of_work = controller.unit_of_work
            with unit_of_work as uow:
                user_repo = uow.user_repository
                has_permission = user_repo.has_permission(user_id, permission_codename)

                if not has_permission:
                    raise HttpError(
                        HTTPStatus.FORBIDDEN,
                        f"Permission refusée: {permission_codename}"
                    )

            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator


def role_required(role_name: str) -> Callable:
    """
    Décorateur pour vérifier si l'utilisateur a le rôle requis.
    À utiliser avec les endpoints Django Ninja.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(controller, request, *args, **kwargs):
            # Vérifier si l'utilisateur est authentifié
            if not hasattr(request, 'auth') or not request.auth:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Non authentifié")

            user_id = request.auth.get("user_id")
            if not user_id:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "ID utilisateur non trouvé")

            # Vérifier le rôle
            unit_of_work = controller.unit_of_work
            with unit_of_work as uow:
                user_repo = uow.user_repository
                user = user_repo.get_user_by_id(user_id)

                if not user or not any(r.name == role_name for r in user.roles):
                    raise HttpError(
                        HTTPStatus.FORBIDDEN,
                        f"Rôle requis non présent: {role_name}"
                    )

            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator
```

## 6. Exemple d'utilisation dans un contrôleur API

```python
import logging

from ninja_extra import api_controller, http_get, http_post, route

from core.use_cases.permission_use_case import PermissionUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.decorators.permission_decorators import permission_required, role_required
from presentation.exceptions import InternalServerError
from presentation.schemas.permission_schema import RoleSchema


@api_controller("/roles", tags=["Roles & Permissions"], auth=jwt_auth)
class RoleController:
    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.permission_use_case = PermissionUseCase(self.unit_of_work)
        self.logger = logging.getLogger(__name__)

    @http_post("/create")
    @permission_required("auth.add_group")
    def create_role(self, request, role_name: str):
        try:
            role = self.permission_use_case.create_role(role_name)
            return {"message": f"Rôle '{role_name}' créé avec succès", "role_id": role.id}
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du rôle: {str(e)}", exc_info=True)
            raise InternalServerError()

    @http_post("/assign_permission")
    @role_required("Admin")
    def assign_permission_to_role(self, request, role_name: str, permission_codename: str):
        try:
            result = self.permission_use_case.assign_permission_to_role(
                role_name, permission_codename
            )
            if result:
                return {"message": f"Permission '{permission_codename}' ajoutée au rôle '{role_name}'"}
            return {"message": "Échec de l'attribution de la permission"}
        except Exception as e:
            self.logger.error(f"Erreur lors de l'attribution de la permission: {str(e)}", exc_info=True)
            raise InternalServerError()

    @http_post("/assign_role_to_user")
    @role_required("Admin")
    def assign_role_to_user(self, request, user_id: int, role_name: str):
        try:
            result = self.permission_use_case.assign_role_to_user(user_id, role_name)
            if result:
                return {"message": f"Rôle '{role_name}' attribué à l'utilisateur ID:{user_id}"}
            return {"message": "Échec de l'attribution du rôle"}
        except Exception as e:
            self.logger.error(f"Erreur lors de l'attribution du rôle: {str(e)}", exc_info=True)
            raise InternalServerError()
```

## 7. Schéma Pydantic pour les permissions

```python
from typing import List, Optional
from ninja import Schema


class PermissionSchema(Schema):
    id: Optional[int] = None
    name: str
    codename: str


class RoleSchema(Schema):
    id: Optional[int] = None
    name: str
    permissions: List[PermissionSchema] = []


class RoleAssignmentSchema(Schema):
    role_name: str
    user_id: int


class PermissionAssignmentSchema(Schema):
    permission_codename: str
    role_name: str
```

## 8. Modification du schéma utilisateur

```python
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ninja import Schema
from pydantic import ConfigDict, EmailStr

from presentation.schemas.base_schema import BaseSchema
from presentation.schemas.permission_schema import PermissionSchema, RoleSchema


# ... Code existant ...

class UserAuthSchema(BaseSchema):
    id: Optional[int] = None
    email: EmailStr
    active: bool = True
    roles: List[RoleSchema] = []
    permissions: List[PermissionSchema] = []
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
```

## 9. Configuration initiale et commandes de gestion

Créez une commande Django pour initialiser les rôles et permissions de base:

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.users.models import User


class Command(BaseCommand):
    help = 'Configure les rôles et permissions de base'

    def handle(self, *args, **kwargs):
        self.stdout.write('Configuration des rôles et permissions...')

        # Création des groupes de base
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        editor_group, _ = Group.objects.get_or_create(name='Editor')
        viewer_group, _ = Group.objects.get_or_create(name='Viewer')

        # Récupération des permissions importantes
        user_permissions = Permission.objects.filter(
            content_type__app_label='users',
            content_type__model='user'
        )

        # Attribution des permissions aux groupes
        # Admin peut tout faire
        for perm in Permission.objects.all():
            admin_group.permissions.add(perm)

        # Éditeurs peuvent modifier les données mais pas les utilisateurs
        for perm in Permission.objects.filter(codename__startswith='change_'):
            if not perm.content_type.app_label == 'users':
                editor_group.permissions.add(perm)

        # Viewers peuvent seulement voir
        for perm in Permission.objects.filter(codename__startswith='view_'):
            viewer_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Rôles et permissions configurés avec succès !'))
```

## Comment utiliser ce système de permissions

1. Initialisez les rôles et permissions:

   ```bash
   python manage.py setup_permissions
   ```

2. Protégez vos endpoints avec les décorateurs:

   ```python
   @permission_required("users.change_user")
   def update_user(self, request, user_id: int):
       # Votre code ici
   ```

   ```python
   @role_required("Admin")
   def admin_only_action(self, request):
       # Votre code ici
   ```

3. Vérifiez les permissions dans votre logique métier:
   ```python
   def some_business_logic(self, user_id):
       if not self.permission_use_case.check_user_permission(user_id, "users.add_user"):
           raise Exception("Permission insuffisante")
       # Continuer avec la logique métier
   ```

Cette implémentation s'intègre parfaitement dans votre architecture existante tout en respectant les principes de Clean Architecture en séparant les entités, les cas d'utilisation, les interfaces et l'infrastructure.

Hoshiaki40: Comment est-ce que on peut ameliorer cette implementation ?

GitHub Copilot: Voici plusieurs axes d’amélioration pour renforcer, fiabiliser et rendre plus maintenable votre gestion des utilisateurs et des permissions :

---

### 1. **Centraliser la logique d’autorisation**

- **Service dédié** : Créez un service d’autorisation (`AuthorizationService`) qui encapsule toutes les vérifications de permissions et de rôles. Cela évite la duplication de logique dans les décorateurs, les contrôleurs et les cas d’utilisation.
- **Exemple** :

  ```python
  class AuthorizationService:
      def __init__(self, user_repo):
          self.user_repo = user_repo

      def user_has_permission(self, user_id, permission_codename):
          return self.user_repo.has_permission(user_id, permission_codename)

      def user_has_role(self, user_id, role_name):
          user = self.user_repo.get_user_by_id(user_id)
          return any(r.name == role_name for r in user.roles)
  ```

---

### 2. **Utiliser les permissions Django natives partout**

- **has_perm** : Utilisez systématiquement `user.has_perm('app_label.codename')` pour bénéficier de la gestion native (permissions directes et héritées via groupes).
- **Synchronisation** : Assurez-vous que vos entités métiers (UserEntity, RoleEntity) reflètent bien l’état réel des permissions Django.

---

### 3. **Décorateurs et permissions paramétrables**

- **Décorateurs génériques** : Rendez vos décorateurs capables de prendre plusieurs permissions ou rôles, et de gérer des permissions conditionnelles (ex : accès en lecture OU écriture).
- **Exemple** :
  ```python
  def permissions_required(*perms):
      ...
  ```

---

### 4. **Gestion fine des permissions sur objets**

- **Object-level permissions** : Pour certains modèles (ex : Article), implémentez des permissions par objet (ownership, etc.) via des méthodes comme `has_object_permission(user, obj)`.
- **Exemple** : Ajoutez une méthode dans vos repositories ou services pour vérifier les droits d’un utilisateur sur un objet précis.

---

### 5. **Tests automatisés**

- **Tests unitaires** : Testez toutes les branches de la logique d’autorisation (succès, échec, cas limites).
- **Tests d’intégration** : Vérifiez que les endpoints protégés réagissent correctement selon le rôle/permission de l’utilisateur.

---

### 6. **Optimisation des accès en base**

- **Préfetch** : Utilisez `select_related` et `prefetch_related` pour charger les groupes et permissions en une seule requête lors de la récupération d’un utilisateur.
- **Cache** : Pour les permissions fréquemment vérifiées, mettez en place un cache court (ex : via Django cache ou un décorateur).

---

### 7. **Administration et gestion dynamique**

- **Endpoints d’administration** : Proposez des endpoints API pour lister, créer, modifier et supprimer rôles et permissions, afin de ne pas dépendre uniquement de l’admin Django.
- **Audit** : Ajoutez un historique des modifications de rôles/permissions pour la traçabilité.

---

### 8. **Documentation et conventions**

- **Docstring et doc API** : Documentez chaque permission, chaque rôle, et les endpoints protégés.
- **Conventions de nommage** : Adoptez une convention stricte pour les codenames de permissions (`app_label.action_model`).

---

### 9. **Sécurité**

- **Vérification systématique** : Ne faites jamais confiance à l’input côté client pour les rôles/permissions : tout doit être vérifié côté serveur.
- **Revocation** : Prévoyez la révocation immédiate des droits (ex : logout forcé si un rôle critique est retiré).

---

### 10. **Scalabilité et évolutivité**

- **Gestion multi-applications** : Si votre projet grandit, centralisez la gestion des permissions dans une app dédiée.
- **Support des scopes OAuth2** : Pour des API publiques, pensez à mapper vos permissions à des scopes OAuth2.

---

**En résumé** :  
Centralisez la logique d’autorisation, optimisez les accès, testez, documentez, et exposez des outils d’administration pour garantir robustesse et évolutivité.  
Cela vous permettra de garder une architecture claire, sécurisée et facile à maintenir.

Hoshiaki40: - Comment faire si je veux directement utiliser des classes a la place d'une chaine de caractère ?

```python
    @permission_required("auth.add_group")
```

```python
@role_required("Admin")
```

GitHub Copilot: Très bonne question !  
Pour utiliser directement des **classes** au lieu de chaînes de caractères dans vos décorateurs, il faut :

1. **Définir une classe pour chaque permission ou rôle** (ex : `AddGroupPermission`, `AdminRole`).
2. **Modifier vos décorateurs** pour accepter une classe (ou une instance), et appeler une méthode standard (ex : `has_permission(user)` ou `has_role(user)`).

---

### Exemple : Permissions sous forme de classes

```python
class AddGroupPermission:
    codename = "auth.add_group"

    @staticmethod
    def has_permission(user):
        return user.has_perm(AddGroupPermission.codename)
```

### Exemple : Rôle sous forme de classe

```python
class AdminRole:
    name = "Admin"

    @staticmethod
    def has_role(user):
        return user.groups.filter(name=AdminRole.name).exists()
```

---

### Nouveau décorateur générique

```python
import functools
from ninja.errors import HttpError
from http import HTTPStatus

def permission_required(permission_class):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(controller, request, *args, **kwargs):
            user = getattr(request, 'auth', None)
            if not user or not permission_class.has_permission(user):
                raise HttpError(HTTPStatus.FORBIDDEN, "Permission refusée")
            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator

def role_required(role_class):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(controller, request, *args, **kwargs):
            user = getattr(request, 'auth', None)
            if not user or not role_class.has_role(user):
                raise HttpError(HTTPStatus.FORBIDDEN, "Rôle requis non présent")
            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator
```

---

### Utilisation

```python
from presentation.permissions import AddGroupPermission
from presentation.roles import AdminRole

@permission_required(AddGroupPermission)
def my_view(...):
    ...

@role_required(AdminRole)
def admin_view(...):
    ...
```

---

**Avantages** :

- Centralisation de la logique de vérification.
- Facilité de test et de réutilisation.
- Plus de sécurité et de lisibilité.

N’hésitez pas à demander un exemple complet adapté à votre code si besoin !

Hoshiaki40: et si je veux plusieurs groupe ou plusieurs permission ?

GitHub Copilot: Pour gérer **plusieurs groupes** ou **plusieurs permissions** dans vos décorateurs, il suffit d’accepter une liste de classes et de vérifier que l’utilisateur possède **au moins une** (ou toutes, selon votre besoin).

---

### 1. Plusieurs permissions (au moins une requise)

```python
import functools
from ninja.errors import HttpError
from http import HTTPStatus

def permissions_required(*permission_classes):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(controller, request, *args, **kwargs):
            user = getattr(request, 'auth', None)
            if not user or not any(perm.has_permission(user) for perm in permission_classes):
                raise HttpError(HTTPStatus.FORBIDDEN, "Permission refusée")
            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator
```

---

### 2. Plusieurs rôles (au moins un requis)

```python
def roles_required(*role_classes):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(controller, request, *args, **kwargs):
            user = getattr(request, 'auth', None)
            if not user or not any(role.has_role(user) for role in role_classes):
                raise HttpError(HTTPStatus.FORBIDDEN, "Rôle requis non présent")
            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator
```

---

### 3. Utilisation

```python
from presentation.permissions import AddGroupPermission, ChangeUserPermission
from presentation.roles import AdminRole, EditorRole

@permissions_required(AddGroupPermission, ChangeUserPermission)
def my_view(...):
    ...

@roles_required(AdminRole, EditorRole)
def admin_or_editor_view(...):
    ...
```

---

**Remarque :**

- Si vous voulez que **toutes** les permissions/roles soient requises, remplacez `any(...)` par `all(...)` dans le décorateur.
- Cette approche reste très lisible et facilement extensible !

Hoshiaki40: - Maintenant Comment implementer cette suggestion ?

- Montre moi etape par etape commen implementer chaque brique,class, quels dossier
- Je veux que l'implementation soit adapté à mon architecture

GitHub Copilot: Pour implémenter cette suggestion de gestion des utilisateurs et des permissions avec des classes plutôt que des chaînes de caractères, je vais analyser d'abord le code existant pour comprendre l'architecture actuelle. # Implémentation de la gestion des permissions basée sur les classes

D'après mon analyse de votre code, je vois que vous avez une architecture Clean suivant un style bien défini avec une séparation claire entre les entités, les interfaces, les cas d'utilisation et l'infrastructure. Je vais vous montrer comment implémenter une gestion des permissions basée sur des classes qui s'intègre parfaitement dans cette architecture.

Commençons par créer chaque composant étape par étape :

## 1. Création des entités pour les permissions (core/domain/entities/) Pour implémenter la gestion des permissions avec des classes plutôt que des chaînes de caractères, tout en respectant votre architecture Clean existante, je vais vous guider étape par étape. Analysons d'abord votre code existant pour comprendre comment intégrer cette nouvelle fonctionnalité. # Implémentation de la gestion des permissions avec des classes

Je vais vous guider étape par étape pour implémenter un système de gestion de permissions complet basé sur des classes. Cette implémentation suivra votre architecture Clean existante.

## 1. Entités pour les permissions

Commençons par créer les entités de base nécessaires à la gestion des permissions. Je vais vous guider pas à pas pour implémenter un système de permissions basé sur des classes, en l'adaptant parfaitement à votre architecture Clean existante.

## 1. Création des entités pour les permissions et les rôles

Commençons par créer les entités de base dans le dossier core/domain/entities/. # Implémentation d'un système de permissions basé sur des classes - Guide étape par étape

Je vais vous guider à travers l'implémentation d'un système complet de gestion des permissions et des rôles basé sur des classes plutôt que des chaînes de caractères, tout en respectant votre architecture Clean existante.

## 1. Création des entités pour les permissions et les rôles

D'abord, créons les entités nécessaires dans le dossier `core/domain/entities/`. # Implémentation de la gestion des permissions/rôles avec classes pour Django Cartographie

Je vais vous présenter une implémentation complète et détaillée, étape par étape, qui s'adapte parfaitement à votre architecture Clean. Cette approche utilisera des classes (plutôt que des chaînes) pour les permissions et les rôles.

## 1. Création des entités (Core Domain)

### 1.1 Entités pour permissions et rôles

```python
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class PermissionEntity(BaseModel):
    """Représentation d'une permission dans le système"""
    id: Optional[int] = None
    codename: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class RoleEntity(BaseModel):
    """Représentation d'un rôle (groupe) dans le système"""
    id: Optional[int] = None
    name: str
    permissions: List[PermissionEntity] = []

    model_config = ConfigDict(from_attributes=True)
```

### 1.2 Étendre l'entité utilisateur

```python
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity


class UserEntity(BaseModel):
    id: Optional[int] = None
    email: str
    password: str
    active: bool = True
    roles: List[RoleEntity] = []
    permissions: List[PermissionEntity] = []
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    def has_permission(self, permission_codename: str) -> bool:
        """Vérifie si l'utilisateur possède une permission spécifique"""
        # Vérification directe des permissions utilisateur
        if any(p.codename == permission_codename for p in self.permissions):
            return True

        # Vérification des permissions via les rôles
        for role in self.roles:
            if any(p.codename == permission_codename for p in role.permissions):
                return True

        return False

    def has_role(self, role_name: str) -> bool:
        """Vérifie si l'utilisateur a un rôle spécifique"""
        return any(r.name == role_name for r in self.roles)
```

## 2. Interfaces des Repositories (Core Interfaces)

### 2.1 Interface du repository pour les permissions et rôles

```python
from abc import abstractmethod
from typing import List, Optional

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.interfaces.base_repository import BaseRepository


class PermissionRepository(BaseRepository):
    @abstractmethod
    def get_permission_by_codename(self, codename: str) -> Optional[PermissionEntity]:
        """Récupère une permission par son code"""
        pass

    @abstractmethod
    def get_all_permissions(self) -> List[PermissionEntity]:
        """Récupère toutes les permissions disponibles"""
        pass

    @abstractmethod
    def get_role_by_name(self, name: str) -> Optional[RoleEntity]:
        """Récupère un rôle par son nom"""
        pass

    @abstractmethod
    def get_all_roles(self) -> List[RoleEntity]:
        """Récupère tous les rôles disponibles"""
        pass

    @abstractmethod
    def create_role(self, role: RoleEntity) -> RoleEntity:
        """Crée un nouveau rôle"""
        pass

    @abstractmethod
    def add_permission_to_role(self, role_name: str, permission_codename: str) -> bool:
        """Ajoute une permission à un rôle"""
        pass

    @abstractmethod
    def remove_permission_from_role(self, role_name: str, permission_codename: str) -> bool:
        """Retire une permission d'un rôle"""
        pass
```

### 2.2 Extension de l'interface du repository utilisateur

```python
from abc import abstractmethod
from typing import List, Optional

from core.domain.entities.user_entity import UserEntity
from core.interfaces.base_repository import BaseRepository


class UserRepository(BaseRepository[UserEntity]):
    @abstractmethod
    def create_user(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def add_role_to_user(self, user_id: int, role_name: str) -> bool:
        """Ajoute un rôle à un utilisateur"""
        pass

    @abstractmethod
    def remove_role_from_user(self, user_id: int, role_name: str) -> bool:
        """Retire un rôle à un utilisateur"""
        pass

    @abstractmethod
    def add_permission_to_user(self, user_id: int, permission_codename: str) -> bool:
        """Ajoute une permission directement à un utilisateur"""
        pass

    @abstractmethod
    def remove_permission_from_user(self, user_id: int, permission_codename: str) -> bool:
        """Retire une permission directement d'un utilisateur"""
        pass

    @abstractmethod
    def has_permission(self, user_id: int, permission_codename: str) -> bool:
        """Vérifie si un utilisateur a une permission"""
        pass

    @abstractmethod
    def has_role(self, user_id: int, role_name: str) -> bool:
        """Vérifie si un utilisateur a un rôle"""
        pass
```

## 3. Classes de permissions et rôles (Presentation)

### 3.1 Classes de base pour définir les permissions et les rôles

```python
from django.contrib.auth.models import User

class BasePermission:
    """Classe de base pour toutes les permissions"""
    codename = None
    name = None

    @classmethod
    def has_permission(cls, user: User) -> bool:
        """Vérifie si l'utilisateur a cette permission"""
        if not cls.codename:
            raise NotImplementedError("Permission codename must be defined")
        return user.has_perm(cls.codename)


# Définition des permissions concrètes
class AddUserPermission(BasePermission):
    """Permission pour ajouter un utilisateur"""
    codename = "users.add_user"
    name = "Can add user"


class ChangeUserPermission(BasePermission):
    """Permission pour modifier un utilisateur"""
    codename = "users.change_user"
    name = "Can change user"


class DeleteUserPermission(BasePermission):
    """Permission pour supprimer un utilisateur"""
    codename = "users.delete_user"
    name = "Can delete user"


class ViewUserPermission(BasePermission):
    """Permission pour voir un utilisateur"""
    codename = "users.view_user"
    name = "Can view user"


# Permissions pour les établissements
class AddEstablishmentPermission(BasePermission):
    """Permission pour ajouter un établissement"""
    codename = "establishment.add_establishment"
    name = "Can add establishment"


class ChangeEstablishmentPermission(BasePermission):
    """Permission pour modifier un établissement"""
    codename = "establishment.change_establishment"
    name = "Can change establishment"


class DeleteEstablishmentPermission(BasePermission):
    """Permission pour supprimer un établissement"""
    codename = "establishment.delete_establishment"
    name = "Can delete establishment"


class ViewEstablishmentPermission(BasePermission):
    """Permission pour voir un établissement"""
    codename = "establishment.view_establishment"
    name = "Can view establishment"


# Ajoutez d'autres permissions selon vos besoins
class AddDomainPermission(BasePermission):
    """Permission pour ajouter un domaine"""
    codename = "domain.add_domain"
    name = "Can add domain"
```

### 3.2 Classes pour les rôles

```python
from django.contrib.auth.models import User

class BaseRole:
    """Classe de base pour tous les rôles"""
    name = None

    @classmethod
    def has_role(cls, user: User) -> bool:
        """Vérifie si l'utilisateur a ce rôle"""
        if not cls.name:
            raise NotImplementedError("Role name must be defined")
        return user.groups.filter(name=cls.name).exists()


# Définition des rôles concrets
class AdminRole(BaseRole):
    """Rôle d'administrateur"""
    name = "Admin"


class SuperAdminRole(BaseRole):
    """Rôle de super administrateur"""
    name = "SuperAdmin"


class SectorAdminRole(BaseRole):
    """Rôle d'administrateur de secteur"""
    name = "AdminSecteur"


class EstablishmentAdminRole(BaseRole):
    """Rôle d'administrateur d'établissement"""
    name = "AdminEtablissement"


class SimpleUserRole(BaseRole):
    """Rôle d'utilisateur simple"""
    name = "SimpleUser"
```

## 4. Implémentation des repositories Django (Infrastructure)

### 4.1 Repository pour les permissions

```python
import logging
from typing import List, Optional

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.interfaces.permission_repository import PermissionRepository
from presentation.exceptions import ConflictError, DatabaseError, NotFoundError

logger = logging.getLogger(__name__)


class DjangoPermissionRepository(PermissionRepository):
    """Implémentation Django du repository pour les permissions et rôles"""

    def get_permission_by_codename(self, codename: str) -> Optional[PermissionEntity]:
        """Récupère une permission par son code"""
        try:
            # Les codenames Django sont généralement au format 'app_label.permission_name'
            app_label, perm_codename = codename.split(".")

            permission = Permission.objects.get(
                content_type__app_label=app_label,
                codename=perm_codename
            )
            return self._permission_to_entity(permission)
        except Permission.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting permission by codename: {e}", exc_info=True)
            raise DatabaseError()

    def get_all_permissions(self) -> List[PermissionEntity]:
        """Récupère toutes les permissions disponibles"""
        try:
            permissions = Permission.objects.all()
            return [self._permission_to_entity(p) for p in permissions]
        except Exception as e:
            logger.error(f"Error getting all permissions: {e}", exc_info=True)
            raise DatabaseError()

    def get_role_by_name(self, name: str) -> Optional[RoleEntity]:
        """Récupère un rôle par son nom"""
        try:
            group = Group.objects.get(name=name)
            return self._role_to_entity(group)
        except Group.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting role by name: {e}", exc_info=True)
            raise DatabaseError()

    def get_all_roles(self) -> List[RoleEntity]:
        """Récupère tous les rôles disponibles"""
        try:
            groups = Group.objects.all().prefetch_related('permissions')
            return [self._role_to_entity(g) for g in groups]
        except Exception as e:
            logger.error(f"Error getting all roles: {e}", exc_info=True)
            raise DatabaseError()

    def create_role(self, role: RoleEntity) -> RoleEntity:
        """Crée un nouveau rôle avec ses permissions"""
        try:
            # Vérifier si le rôle existe déjà
            if Group.objects.filter(name=role.name).exists():
                logger.warning(f"Role with name {role.name} already exists")
                raise ConflictError()

            # Créer le groupe
            group = Group.objects.create(name=role.name)

            # Ajouter les permissions si spécifiées
            if role.permissions:
                for perm_entity in role.permissions:
                    try:
                        app_label, perm_codename = perm_entity.codename.split(".")
                        perm = Permission.objects.get(
                            content_type__app_label=app_label,
                            codename=perm_codename
                        )
                        group.permissions.add(perm)
                    except Permission.DoesNotExist:
                        logger.warning(f"Permission {perm_entity.codename} not found")
                        continue

            return self._role_to_entity(group)
        except ConflictError:
            raise
        except Exception as e:
            logger.error(f"Error creating role: {e}", exc_info=True)
            raise DatabaseError()

    def add_permission_to_role(self, role_name: str, permission_codename: str) -> bool:
        """Ajoute une permission à un rôle"""
        try:
            # Récupérer le groupe
            group = Group.objects.get(name=role_name)

            # Récupérer la permission
            app_label, perm_codename = permission_codename.split(".")
            permission = Permission.objects.get(
                content_type__app_label=app_label,
                codename=perm_codename
            )

            # Ajouter la permission
            group.permissions.add(permission)
            return True
        except Group.DoesNotExist:
            logger.warning(f"Role {role_name} not found")
            raise NotFoundError()
        except Permission.DoesNotExist:
            logger.warning(f"Permission {permission_codename} not found")
            raise NotFoundError()
        except Exception as e:
            logger.error(f"Error adding permission to role: {e}", exc_info=True)
            raise DatabaseError()

    def remove_permission_from_role(self, role_name: str, permission_codename: str) -> bool:
        """Retire une permission d'un rôle"""
        try:
            # Récupérer le groupe
            group = Group.objects.get(name=role_name)

            # Récupérer la permission
            app_label, perm_codename = permission_codename.split(".")
            permission = Permission.objects.get(
                content_type__app_label=app_label,
                codename=perm_codename
            )

            # Retirer la permission
            group.permissions.remove(permission)
            return True
        except Group.DoesNotExist:
            logger.warning(f"Role {role_name} not found")
            raise NotFoundError()
        except Permission.DoesNotExist:
            logger.warning(f"Permission {permission_codename} not found")
            raise NotFoundError()
        except Exception as e:
            logger.error(f"Error removing permission from role: {e}", exc_info=True)
            raise DatabaseError()

    def _permission_to_entity(self, permission: Permission) -> PermissionEntity:
        """Convertit un objet Permission Django en PermissionEntity"""
        return PermissionEntity(
            id=permission.id,
            codename=f"{permission.content_type.app_label}.{permission.codename}",
            name=permission.name
        )

    def _role_to_entity(self, group: Group) -> RoleEntity:
        """Convertit un objet Group Django en RoleEntity"""
        permissions = [self._permission_to_entity(p) for p in group.permissions.all()]
        return RoleEntity(
            id=group.id,
            name=group.name,
            permissions=permissions
        )

    # Méthodes abstraites héritées de BaseRepository
    # Ces méthodes ne sont généralement pas utilisées directement avec ce repository
    def create(self, data):
        raise NotImplementedError("Use specific create methods instead")

    def update(self, id, data):
        raise NotImplementedError("Use specific update methods instead")

    def get(self, id):
        raise NotImplementedError("Use specific get methods instead")

    def get_all(self, pagination_params=None):
        raise NotImplementedError("Use get_all_roles or get_all_permissions instead")

    def delete(self, id):
        raise NotImplementedError("Use specific delete methods instead")

    def filter(self, **kwargs):
        raise NotImplementedError("Use specific filter methods instead")

    def count(self, **kwargs):
        raise NotImplementedError("Use specific count methods instead")
```

### 4.2 Extension du repository utilisateur

```python
from typing import Any, List, Optional
from uuid import UUID

from django.contrib.auth.models import Group, Permission
from apps.users.models import User
from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.domain.entities.user_entity import UserEntity
from core.interfaces.user_repository import UserRepository
from presentation.exceptions import NotFoundError, DatabaseError


class DjangoUserRepository(UserRepository):

    def create_user(self, user: UserEntity) -> UserEntity:
        django_user = User(
            email=user.email,
        )
        django_user.set_password(user.password)
        django_user.save()
        return self._to_entity(django_user)

    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            user = User.objects.get(email=email)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        try:
            user = User.objects.get(id=user_id)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        # Vérifier uniquement par email
        user = User.objects.filter(email=login).first()
        if user and user.check_password(password):
            return self._to_entity(user)
        return None

    def add_role_to_user(self, user_id: int, role_name: str) -> bool:
        """Ajoute un rôle à un utilisateur"""
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name=role_name)
            user.groups.add(group)
            return True
        except User.DoesNotExist:
            raise NotFoundError()
        except Group.DoesNotExist:
            raise NotFoundError()
        except Exception:
            raise DatabaseError()

    def remove_role_from_user(self, user_id: int, role_name: str) -> bool:
        """Retire un rôle d'un utilisateur"""
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name=role_name)
            user.groups.remove(group)
            return True
        except User.DoesNotExist:
            raise NotFoundError()
        except Group.DoesNotExist:
            raise NotFoundError()
        except Exception:
            raise DatabaseError()

    def add_permission_to_user(self, user_id: int, permission_codename: str) -> bool:
        """Ajoute une permission directement à un utilisateur"""
        try:
            user = User.objects.get(id=user_id)
            app_label, codename = permission_codename.split(".")
            perm = Permission.objects.get(
                content_type__app_label=app_label,
                codename=codename
            )
            user.user_permissions.add(perm)
            return True
        except User.DoesNotExist:
            raise NotFoundError()
        except Permission.DoesNotExist:
            raise NotFoundError()
        except Exception:
            raise DatabaseError()

    def remove_permission_from_user(self, user_id: int, permission_codename: str) -> bool:
        """Retire une permission directement d'un utilisateur"""
        try:
            user = User.objects.get(id=user_id)
            app_label, codename = permission_codename.split(".")
            perm = Permission.objects.get(
                content_type__app_label=app_label,
                codename=codename
            )
            user.user_permissions.remove(perm)
            return True
        except User.DoesNotExist:
            raise NotFoundError()
        except Permission.DoesNotExist:
            raise NotFoundError()
        except Exception:
            raise DatabaseError()

    def has_permission(self, user_id: int, permission_codename: str) -> bool:
        """Vérifie si un utilisateur a une permission (directe ou via groupe)"""
        try:
            user = User.objects.get(id=user_id)
            return user.has_perm(permission_codename)
        except User.DoesNotExist:
            return False
        except Exception:
            raise DatabaseError()

    def has_role(self, user_id: int, role_name: str) -> bool:
        """Vérifie si un utilisateur a un rôle"""
        try:
            user = User.objects.get(id=user_id)
            return user.groups.filter(name=role_name).exists()
        except User.DoesNotExist:
            return False
        except Exception:
            raise DatabaseError()

    def _to_entity(self, django_user: User) -> UserEntity:
        """Convertit un modèle Django User en UserEntity avec rôles et permissions"""
        # Récupérer les rôles (groupes)
        roles = []
        for group in django_user.groups.all():
            permissions = []
            for perm in group.permissions.all():
                perm_codename = f"{perm.content_type.app_label}.{perm.codename}"
                permissions.append(
                    PermissionEntity(
                        id=perm.id,
                        name=perm.name,
                        codename=perm_codename
                    )
                )

            roles.append(
                RoleEntity(
                    id=group.id,
                    name=group.name,
                    permissions=permissions
                )
            )

        # Récupérer les permissions directes
        direct_permissions = []
        for perm in django_user.user_permissions.all():
            perm_codename = f"{perm.content_type.app_label}.{perm.codename}"
            direct_permissions.append(
                PermissionEntity(
                    id=perm.id,
                    name=perm.name,
                    codename=perm_codename
                )
            )

        # Créer l'entité utilisateur
        return UserEntity(
            id=django_user.id,
            email=django_user.email,
            password="",  # We don't return the password
            active=django_user.active,
            roles=roles,
            permissions=direct_permissions,
            updated_by=django_user.updated_by,
            created_at=django_user.created_at,
            updated_at=django_user.updated_at,
        )

    def create(self, data: Any) -> Any:
        raise NotImplementedError

    def get(self, id: UUID | int) -> Any | None:
        raise NotImplementedError

    def get_all(self) -> List[Any]:
        raise NotImplementedError

    def update(self, id: UUID | int, data: Any) -> Any | None:
        raise NotImplementedError

    def delete(self, id: UUID | int) -> bool:
        raise NotImplementedError

    def filter(self, **kwargs) -> List[Any]:
        raise NotImplementedError

    def count(self, **kwargs) -> int:
        raise NotImplementedError
```

## 5. Mise à jour de l'UnitOfWork pour intégrer le nouveau repository

```python
from typing import Dict, Type, TypeVar

from django.db import transaction

from core.interfaces.base_repository import BaseRepository
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_permission_repository import DjangoPermissionRepository

T = TypeVar("T")


class DjangoUnitOfWork(UnitOfWork):
    def __init__(self):
        self._repositories: Dict[Type[BaseRepository], BaseRepository] = {}
        # Initialisation directe du repository de permission pour un accès facile
        self._permission_repository = None

    def __enter__(self) -> "DjangoUnitOfWork":
        transaction.set_autocommit(False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            try:
                self.commit()
            except:
                self.rollback()
                raise
            finally:
                transaction.set_autocommit(True)
        self._repositories.clear()
        self._permission_repository = None

    def commit(self):
        transaction.commit()

    def rollback(self):
        transaction.rollback()

    def get_repository(
        self, repository_class: Type[BaseRepository[T]]
    ) -> BaseRepository[T]:
        if repository_class not in self._repositories:
            self._repositories[repository_class] = repository_class()
        return self._repositories[repository_class]

    @property
    def permission_repository(self) -> DjangoPermissionRepository:
        """Accès facile au repository de permissions"""
        if self._permission_repository is None:
            self._permission_repository = DjangoPermissionRepository()
        return self._permission_repository
```

## 6. Cas d'utilisation pour la gestion des permissions

```python
import logging
from typing import List, Optional

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.domain.entities.user_entity import UserEntity
from core.interfaces.unit_of_work import UnitOfWork
from infrastructure.db.django_permission_repository import DjangoPermissionRepository
from infrastructure.db.django_user_repository import DjangoUserRepository
from presentation.exceptions import ConflictError, NotFoundError


class PermissionUseCase:
    """Cas d'utilisation pour gérer les permissions et rôles"""

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work
        self.logger = logging.getLogger(__name__)

    def get_all_permissions(self) -> List[PermissionEntity]:
        """Récupère toutes les permissions disponibles"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository
            return permission_repo.get_all_permissions()

    def get_all_roles(self) -> List[RoleEntity]:
        """Récupère tous les rôles disponibles"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository
            return permission_repo.get_all_roles()

    def get_role_permissions(self, role_name: str) -> List[PermissionEntity]:
        """Récupère les permissions d'un rôle spécifique"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository
            role = permission_repo.get_role_by_name(role_name)
            if not role:
                raise NotFoundError()
            return role.permissions

    def create_role(self, role_data: RoleEntity) -> RoleEntity:
        """Crée un nouveau rôle"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository

            # Vérifier si le rôle existe déjà
            existing_role = permission_repo.get_role_by_name(role_data.name)
            if existing_role:
                self.logger.warning(f"Role with name '{role_data.name}' already exists")
                raise ConflictError()

            # Créer le rôle
            return permission_repo.create_role(role_data)

    def assign_permission_to_role(self, role_name: str, permission_codename: str) -> bool:
        """Assigne une permission à un rôle"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository
            return permission_repo.add_permission_to_role(role_name, permission_codename)

    def remove_permission_from_role(self, role_name: str, permission_codename: str) -> bool:
        """Retire une permission d'un rôle"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository
            return permission_repo.remove_permission_from_role(role_name, permission_codename)

    def get_user_roles(self, user_id: int) -> List[RoleEntity]:
        """Récupère les rôles d'un utilisateur"""
        with self.unit_of_work as uow:
            user_repo = uow.get_repository(DjangoUserRepository)
            user = user_repo.get_user_by_id(user_id)
            if not user:
                raise NotFoundError()
            return user.roles

    def get_user_permissions(self, user_id: int) -> List[PermissionEntity]:
        """Récupère les permissions directes d'un utilisateur"""
        with self.unit_of_work as uow:
            user_repo = uow.get_repository(DjangoUserRepository)
            user = user_repo.get_user_by_id(user_id)
            if not user:
                raise NotFoundError()
            return user.permissions

    def assign_role_to_user(self, user_id: int, role_name: str) -> bool:
        """Assigne un rôle à un utilisateur"""
        with self.unit_of_work as uow:
            user_repo = uow.get_repository(DjangoUserRepository)
            return user_repo.add_role_to_user(user_id, role_name)

    def remove_role_from_user(self, user_id: int, role_name: str) -> bool:
        """Retire un rôle d'un utilisateur"""
        with self.unit_of_work as uow:
            user_repo = uow.get_repository(DjangoUserRepository)
            return user_repo.remove_role_from_user(user_id, role_name)

    def assign_permission_to_user(self, user_id: int, permission_codename: str) -> bool:
        """Assigne une permission directement à un utilisateur"""
        with self.unit_of_work as uow:
            user_repo = uow.get_repository(DjangoUserRepository)
            return user_repo.add_permission_to_user(user_id, permission_codename)

    def remove_permission_from_user(self, user_id: int, permission_codename: str) -> bool:
        """Retire une permission directement d'un utilisateur"""
        with self.unit_of_work as uow:
            user_repo = uow.get_repository(DjangoUserRepository)
            return user_repo.remove_permission_from_user(user_id, permission_codename)

    def check_user_has_permission(self, user_id: int, permission_codename: str) -> bool:
        """Vérifie si un utilisateur possède une permission spécifique"""
        with self.unit_of_work as uow:
            user_repo = uow.get_repository(DjangoUserRepository)
            return user_repo.has_permission(user_id, permission_codename)

    def check_user_has_role(self, user_id: int, role_name: str) -> bool:
        """Vérifie si un utilisateur possède un rôle spécifique"""
        with self.unit_of_work as uow:
            user_repo = uow.get_repository(DjangoUserRepository)
            return user_repo.has_role(user_id, role_name)

    def get_current_user_with_permissions(self, user_id: int) -> Optional[UserEntity]:
        """Récupère l'utilisateur courant avec ses permissions"""
        with self.unit_of_work as uow:
            user_repo = uow.get_repository(DjangoUserRepository)
            return user_repo.get_user_by_id(user_id)
```

## 7. Décorateurs pour les permissions et rôles avec des classes

```python
import functools
import logging
from http import HTTPStatus
from typing import Any, Callable, List, Type, Union

from django.contrib.auth.models import AnonymousUser
from ninja.errors import HttpError

from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from presentation.permissions import BasePermission
from presentation.roles import BaseRole

logger = logging.getLogger(__name__)


def permission_required(permission_class: Type[BasePermission]):
    """
    Décorateur qui vérifie qu'un utilisateur possède une permission spécifique.

    Args:
        permission_class: Une classe dérivée de BasePermission

    Returns:
        Le décorateur qui vérifie la permission
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(controller: Any, request: Any, *args: Any, **kwargs: Any) -> Any:
            # Vérifier si l'utilisateur est authentifié
            if not hasattr(request, 'auth') or not request.auth:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Non authentifié")

            user_id = request.auth.get("user_id")
            if not user_id:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "ID utilisateur non trouvé")

            # Récupérer l'utilisateur Django
            from apps.users.models import User
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Utilisateur invalide")

            # Vérifier la permission
            if not permission_class.has_permission(user):
                # Journaliser le refus d'accès
                logger.warning(
                    f"Permission refusée: {permission_class.codename} pour l'utilisateur {user_id}"
                )
                raise HttpError(
                    HTTPStatus.FORBIDDEN,
                    f"Permission refusée: {permission_class.name}"
                )

            # La permission est validée, exécuter la fonction
            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator


def permissions_required(*permission_classes: Type[BasePermission], require_all: bool = False):
    """
    Décorateur qui vérifie qu'un utilisateur possède une ou plusieurs permissions.

    Args:
        *permission_classes: Une ou plusieurs classes dérivées de BasePermission
        require_all: Si True, toutes les permissions sont requises; sinon, une seule suffit

    Returns:
        Le décorateur qui vérifie les permissions
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(controller: Any, request: Any, *args: Any, **kwargs: Any) -> Any:
            # Vérifier si l'utilisateur est authentifié
            if not hasattr(request, 'auth') or not request.auth:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Non authentifié")

            user_id = request.auth.get("user_id")
            if not user_id:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "ID utilisateur non trouvé")

            # Récupérer l'utilisateur Django
            from apps.users.models import User
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Utilisateur invalide")

            # Vérifier les permissions
            permission_results = [perm_class.has_permission(user) for perm_class in permission_classes]

            if require_all and not all(permission_results):
                # Toutes les permissions sont requises mais au moins une est manquante
                missing_permissions = [
                    perm_class.name
                    for perm_class, has_perm in zip(permission_classes, permission_results)
                    if not has_perm
                ]
                logger.warning(
                    f"Permissions manquantes: {', '.join(missing_permissions)} "
                    f"pour l'utilisateur {user_id}"
                )
                raise HttpError(
                    HTTPStatus.FORBIDDEN,
                    "Permissions insuffisantes"
                )
            elif not require_all and not any(permission_results):
                # Au moins une permission est requise mais aucune n'est présente
                logger.warning(
                    f"Aucune des permissions requises pour l'utilisateur {user_id}"
                )
                raise HttpError(
                    HTTPStatus.FORBIDDEN,
                    "Permission refusée"
                )

            # Les permissions sont validées, exécuter la fonction
            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator


def role_required(role_class: Type[BaseRole]):
    """
    Décorateur qui vérifie qu'un utilisateur possède un rôle spécifique.

    Args:
        role_class: Une classe dérivée de BaseRole

    Returns:
        Le décorateur qui vérifie le rôle
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(controller: Any, request: Any, *args: Any, **kwargs: Any) -> Any:
            # Vérifier si l'utilisateur est authentifié
            if not hasattr(request, 'auth') or not request.auth:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Non authentifié")

            user_id = request.auth.get("user_id")
            if not user_id:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "ID utilisateur non trouvé")

            # Récupérer l'utilisateur Django
            from apps.users.models import User
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Utilisateur invalide")

            # Vérifier le rôle
            if not role_class.has_role(user):
                logger.warning(
                    f"Rôle requis non présent: {role_class.name} pour l'utilisateur {user_id}"
                )
                raise HttpError(
                    HTTPStatus.FORBIDDEN,
                    f"Rôle requis: {role_class.name}"
                )

            # Le rôle est validé, exécuter la fonction
            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator


def roles_required(*role_classes: Type[BaseRole], require_all: bool = False):
    """
    Décorateur qui vérifie qu'un utilisateur possède un ou plusieurs rôles.

    Args:
        *role_classes: Une ou plusieurs classes dérivées de BaseRole
        require_all: Si True, tous les rôles sont requis; sinon, un seul suffit

    Returns:
        Le décorateur qui vérifie les rôles
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(controller: Any, request: Any, *args: Any, **kwargs: Any) -> Any:
            # Vérifier si l'utilisateur est authentifié
            if not hasattr(request, 'auth') or not request.auth:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Non authentifié")

            user_id = request.auth.get("user_id")
            if not user_id:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "ID utilisateur non trouvé")

            # Récupérer l'utilisateur Django
            from apps.users.models import User
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Utilisateur invalide")

            # Vérifier les rôles
            role_results = [role_class.has_role(user) for role_class in role_classes]

            if require_all and not all(role_results):
                # Tous les rôles sont requis mais au moins un est manquant
                missing_roles = [
                    role_class.name
                    for role_class, has_role in zip(role_classes, role_results)
                    if not has_role
                ]
                logger.warning(
                    f"Rôles manquants: {', '.join(missing_roles)} "
                    f"pour l'utilisateur {user_id}"
                )
                raise HttpError(
                    HTTPStatus.FORBIDDEN,
                    "Rôles insuffisants"
                )
            elif not require_all and not any(role_results):
                # Au moins un rôle est requis mais aucun n'est présent
                logger.warning(
                    f"Aucun des rôles requis pour l'utilisateur {user_id}"
                )
                raise HttpError(
                    HTTPStatus.FORBIDDEN,
                    "Rôles requis"
                )

            # Les rôles sont validés, exécuter la fonction
            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator
```

## 8. Schémas pour API (Presentation)

```python
from typing import List, Optional

from ninja import Schema
from pydantic import ConfigDict


class PermissionSchema(Schema):
    """Schéma de permission pour l'API"""
    id: Optional[int] = None
    codename: str
    name: str


class RoleSchema(Schema):
    """Schéma de rôle pour l'API"""
    id: Optional[int] = None
    name: str
    permissions: Optional[List[PermissionSchema]] = None

    model_config = ConfigDict(from_attributes=True)


class CreateRoleSchema(Schema):
    """Schéma pour créer un nouveau rôle"""
    name: str
    permission_codenames: Optional[List[str]] = None


class AddPermissionToRoleSchema(Schema):
    """Schéma pour ajouter une permission à un rôle"""
    permission_codename: str


class AssignRoleToUserSchema(Schema):
    """Schéma pour assigner un rôle à un utilisateur"""
    role_name: str


class AssignPermissionToUserSchema(Schema):
    """Schéma pour assigner une permission à un utilisateur"""
    permission_codename: str
```

## 9. Contrôleur pour gérer les permissions et rôles via l'API

```python
import logging
from typing import List

from ninja_extra import api_controller, http_get, http_post, http_delete
from ninja.errors import HttpError

from core.use_cases.permission_use_case import PermissionUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.decorators.permission_decorators import permission_required, role_required
from presentation.exceptions import ConflictError, InternalServerError, NotFoundError
from presentation.permissions import AddUserPermission, ChangeUserPermission
from presentation.roles import AdminRole, SuperAdminRole
from presentation.schemas.permission_schema import (
    AddPermissionToRoleSchema,
    AssignPermissionToUserSchema,
    AssignRoleToUserSchema,
    CreateRoleSchema,
    PermissionSchema,
    RoleSchema,
)


@api_controller("/permissions", tags=["Permissions"], auth=jwt_auth)
class PermissionController:
    """Contrôleur pour gérer les permissions et rôles"""

    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.permission_use_case = PermissionUseCase(self.unit_of_work)
        self.logger = logging.getLogger(__name__)

    @http_get("/", response=List[PermissionSchema])
    @permission_required(ViewUserPermission)
    def get_all_permissions(self, request):
        """Récupère toutes les permissions disponibles"""
        try:
            permissions = self.permission_use_case.get_all_permissions()
            return [
                PermissionSchema(id=p.id, codename=p.codename, name=p.name)
                for p in permissions
            ]
        except Exception as e:
            self.logger.error(f"Error getting permissions: {e}", exc_info=True)
            raise InternalServerError()

    @http_get("/roles", response=List[RoleSchema])
    @permission_required(ViewUserPermission)
    def get_all_roles(self, request):
        """Récupère tous les rôles disponibles"""
        try:
            roles = self.permission_use_case.get_all_roles()
            return [
                RoleSchema(
                    id=r.id,
                    name=r.name,
                    permissions=[
                        PermissionSchema(id=p.id, codename=p.codename, name=p.name)
                        for p in r.permissions
                    ]
                )
                for r in roles
            ]
        except Exception as e:
            self.logger.error(f"Error getting roles: {e}", exc_info=True)
            raise InternalServerError()

    @http_get("/roles/{role_name}", response=List[PermissionSchema])
    @permission_required(ViewUserPermission)
    def get_role_permissions(self, request, role_name: str):
        """Récupère les permissions d'un rôle spécifique"""
        try:
            permissions = self.permission_use_case.get_role_permissions(role_name)
            return [
                PermissionSchema(id=p.id, codename=p.codename, name=p.name)
                for p in permissions
            ]
        except NotFoundError:
            raise HttpError(404, f"Rôle {role_name} non trouvé")
        except Exception as e:
            self.logger.error(f"Error getting role permissions: {e}", exc_info=True)
            raise InternalServerError()

    @http_post("/roles", response={201: RoleSchema})
    @role_required(SuperAdminRole)
    def create_role(self, request, data: CreateRoleSchema):
        """Crée un nouveau rôle"""
        try:
            # Créer l'entité RoleEntity
            from core.domain.entities.permission_entity import RoleEntity
            role_entity = RoleEntity(name=data.name, permissions=[])

            # Créer le rôle
            created_role = self.permission_use_case.create_role(role_entity)

            # Ajouter les permissions si spécifiées
            if data.permission_codenames:
                for perm_codename in data.permission_codenames:
                    self.permission_use_case.assign_permission_to_role(
                        created_role.name, perm_codename
                    )

                # Récupérer le rôle avec ses permissions
                role_permissions = self.permission_use_case.get_role_permissions(created_role.name)
                created_role.permissions = role_permissions

            return 201, RoleSchema(
                id=created_role.id,
                name=created_role.name,
                permissions=[
                    PermissionSchema(id=p.id, codename=p.codename, name=p.name)
                    for p in created_role.permissions
                ]
            )
        except ConflictError:
            raise HttpError(409, f"Le rôle {data.name} existe déjà")
        except Exception as e:
            self.logger.error(f"Error creating role: {e}", exc_info=True)
            raise InternalServerError()

    @http_post("/roles/{role_name}/permissions", response={200: dict})
    @role_required(SuperAdminRole)
    def add_permission_to_role(self, request, role_name: str, data: AddPermissionToRoleSchema):
        """Ajoute une permission à un rôle"""
        try:
            result = self.permission_use_case.assign_permission_to_role(
                role_name, data.permission_codename
            )
            return {"success": result, "message": "Permission ajoutée au rôle"}
        except NotFoundError:
            raise HttpError(404, "Rôle ou permission non trouvé")
        except Exception as e:
            self.logger.error(f"Error adding permission to role: {e}", exc_info=True)
            raise InternalServerError()

    @http_delete("/roles/{role_name}/permissions/{permission_codename}", response={200: dict})
    @role_required(SuperAdminRole)
    def remove_permission_from_role(self, request, role_name: str, permission_codename: str):
        """Retire une permission d'un rôle"""
        try:
            result = self.permission_use_case.remove_permission_from_role(
                role_name, permission_codename
            )
            return {"success": result, "message": "Permission retirée du rôle"}
        except NotFoundError:
            raise HttpError(404, "Rôle ou permission non trouvé")
        except Exception as e:
            self.logger.error(f"Error removing permission from role: {e}", exc_info=True)
            raise InternalServerError()

    @http_get("/users/{user_id}/roles", response=List[RoleSchema])
    @permission_required(ViewUserPermission)
    def get_user_roles(self, request, user_id: int):
        """Récupère les rôles d'un utilisateur"""
        try:
            roles = self.permission_use_case.get_user_roles(user_id)
            return [
                RoleSchema(
                    id=r.id,
                    name=r.name,
                    permissions=[
                        PermissionSchema(id=p.id, codename=p.codename, name=p.name)
                        for p in r.permissions
                    ]
                )
                for r in roles
            ]
        except NotFoundError:
            raise HttpError(404, "Utilisateur non trouvé")
        except Exception as e:
            self.logger.error(f"Error getting user roles: {e}", exc_info=True)
            raise InternalServerError()

    @http_get("/users/{user_id}/permissions", response=List[PermissionSchema])
    @permission_required(ViewUserPermission)
    def get_user_permissions(self, request, user_id: int):
        """Récupère les permissions directes d'un utilisateur"""
        try:
            permissions = self.permission_use_case.get_user_permissions(user_id)
            return [
                PermissionSchema(id=p.id, codename=p.codename, name=p.name)
                for p in permissions
            ]
        except NotFoundError:
            raise HttpError(404, "Utilisateur non trouvé")
        except Exception as e:
            self.logger.error(f"Error getting user permissions: {e}", exc_info=True)
            raise InternalServerError()

    @http_post("/users/{user_id}/roles", response={200: dict})
    @role_required(AdminRole)
    def assign_role_to_user(self, request, user_id: int, data: AssignRoleToUserSchema):
        """Assigne un rôle à un utilisateur"""
        try:
            result = self.permission_use_case.assign_role_to_user(
                user_id, data.role_name
            )
            return {"success": result, "message": "Rôle assigné à l'utilisateur"}
        except NotFoundError:
            raise HttpError(404, "Utilisateur ou rôle non trouvé")
        except Exception as e:
            self.logger.error(f"Error assigning role to user: {e}", exc_info=True)
            raise InternalServerError()

    @http_delete("/users/{user_id}/roles/{role_name}", response={200: dict})
    @role_required(AdminRole)
    def remove_role_from_user(self, request, user_id: int, role_name: str):
        """Retire un rôle d'un utilisateur"""
        try:
            result = self.permission_use_case.remove_role_from_user(user_id, role_name)
            return {"success": result, "message": "Rôle retiré de l'utilisateur"}
        except NotFoundError:
            raise HttpError(404, "Utilisateur ou rôle non trouvé")
        except Exception as e:
            self.logger.error(f"Error removing role from user: {e}", exc_info=True)
            raise InternalServerError()

    @http_post("/users/{user_id}/permissions", response={200: dict})
    @role_required(AdminRole)
    def assign_permission_to_user(self, request, user_id: int, data: AssignPermissionToUserSchema):
        """Assigne une permission directement à un utilisateur"""
        try:
            result = self.permission_use_case.assign_permission_to_user(
                user_id, data.permission_codename
            )
            return {"success": result, "message": "Permission assignée à l'utilisateur"}
        except NotFoundError:
            raise HttpError(404, "Utilisateur ou permission non trouvé")
        except Exception as e:
            self.logger.error(f"Error assigning permission to user: {e}", exc_info=True)
            raise InternalServerError()

    @http_delete("/users/{user_id}/permissions/{permission_codename}", response={200: dict})
    @role_required(AdminRole)
    def remove_permission_from_user(self, request, user_id: int, permission_codename: str):
        """Retire une permission directement d'un utilisateur"""
        try:
            result = self.permission_use_case.remove_permission_from_user(
                user_id, permission_codename
            )
            return {"success": result, "message": "Permission retirée de l'utilisateur"}
        except NotFoundError:
            raise HttpError(404, "Utilisateur ou permission non trouvé")
        except Exception as e:
            self.logger.error(f"Error removing permission from user: {e}", exc_info=True)
            raise InternalServerError()
```

## 10. Commande de gestion Django pour l'initialisation

```python
import logging

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from presentation.permissions import (
    AddUserPermission,
    ChangeUserPermission,
    DeleteUserPermission,
    ViewUserPermission,
    AddEstablishmentPermission,
    ChangeEstablishmentPermission,
    DeleteEstablishmentPermission,
    ViewEstablishmentPermission,
    AddDomainPermission,
)
from presentation.roles import (
    AdminRole,
    SuperAdminRole,
    SectorAdminRole,
    EstablishmentAdminRole,
    SimpleUserRole,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Commande Django pour configurer les rôles et permissions de base.
    Usage: python manage.py setup_permissions
    """

    help = "Configure les rôles et permissions prédéfinis"

    def handle(self, *args, **kwargs):
        self.stdout.write("Initialisation des rôles et permissions...")

        # Création des rôles (groupes)
        super_admin_group, _ = Group.objects.get_or_create(name=SuperAdminRole.name)
        admin_group, _ = Group.objects.get_or_create(name=AdminRole.name)
        sector_admin_group, _ = Group.objects.get_or_create(name=SectorAdminRole.name)
        establishment_admin_group, _ = Group.objects.get_or_create(name=EstablishmentAdminRole.name)
        simple_user_group, _ = Group.objects.get_or_create(name=SimpleUserRole.name)

        # Attribution des permissions selon la logique métier

        # 1. SuperAdmin: accès complet à tout
        all_permissions = Permission.objects.all()
        for perm in all_permissions:
            super_admin_group.permissions.add(perm)

        # 2. Admin: accès à la gestion des utilisateurs et certaines entités
        user_permissions = [
            AddUserPermission.codename,
            ChangeUserPermission.codename,
            DeleteUserPermission.codename,
            ViewUserPermission.codename
        ]

        for perm_codename in user_permissions:
            app_label, codename = perm_codename.split('.')
            try:
                perm = Permission.objects.get(
                    content_type__app_label=app_label,
                    codename=codename
                )
                admin_group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Permission {perm_codename} introuvable")
                )

        # 3. AdminSecteur: gestion des établissements de son secteur
        establishment_permissions = [
            AddEstablishmentPermission.codename,
            ChangeEstablishmentPermission.codename,
            ViewEstablishmentPermission.codename,
        ]

        for perm_codename in establishment_permissions:
            app_label, codename = perm_codename.split('.')
            try:
                perm = Permission.objects.get(
                    content_type__app_label=app_label,
                    codename=codename
                )
                sector_admin_group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Permission {perm_codename} introuvable")
                )

        # 4. AdminEtablissement: gestion de son propre établissement
        establishment_admin_permissions = [
            ChangeEstablishmentPermission.codename,
            ViewEstablishmentPermission.codename,
        ]

        for perm_codename in establishment_admin_permissions:
            app_label, codename = perm_codename.split('.')
            try:
                perm = Permission.objects.get(
                    content_type__app_label=app_label,
                    codename=codename
                )
                establishment_admin_group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Permission {perm_codename} introuvable")
                )

        # 5. SimpleUser: accès en lecture seule
        view_permissions = Permission.objects.filter(codename__startswith='view_')
        for perm in view_permissions:
            simple_user_group.permissions.add(perm)

        self.stdout.write(
            self.style.SUCCESS("Configuration des rôles et permissions terminée!")
        )
```

## 11. Mise à jour des routes API

```python
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from presentation.api.v1.endpoints.auth_controller import AuthController
from presentation.api.v1.endpoints.permission_controller import PermissionController
# Importez vos autres contrôleurs ici

api = NinjaExtraAPI(title="Django Cartographie API", version="1.0.0")

# Ajouter les contrôleurs à l'API
api.register_controllers(
    AuthController,
    PermissionController,
    NinjaJWTDefaultController,
    # Autres contrôleurs
)
```

## 12. Exemple d'utilisation dans un contrôleur existant

`````python
# Extrait d'un fichier controller existant avec les nouveaux décorateurs
from presentation.decorators.permission_decorators import (
    permission_required,
    permissions_required,
    role_required,
    roles# Extrait d'un fichier controller existant avec les nouveaux décorateurs
from presentation.decorators.permission_decorators import (
    permission_required,
    permissions_required,
    role_required,
    roles

Hoshiaki40: continue

GitHub Copilot: # Implémentation étape par étape

Voici comment adapter l'implémentation de la gestion des rôles et permissions à votre architecture Clean Architecture, en suivant la structure de dossiers existante.

## 1. Définition des modèles de domaine

### 1.1. Entités de permission et de rôle

````python
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class PermissionEntity(BaseModel):
    id: Optional[int] = None
    name: str
    codename: str

    model_config = ConfigDict(from_attributes=True)


class RoleEntity(BaseModel):
    id: Optional[int] = None
    name: str
    permissions: List[PermissionEntity] = []

    model_config = ConfigDict(from_attributes=True)
`````

### 1.2. Mise à jour de l'entité utilisateur

```python
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity


class UserEntity(BaseModel):
    id: Optional[int] = None
    email: str
    password: str
    active: bool = True
    roles: List[RoleEntity] = []
    permissions: List[PermissionEntity] = []
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    def has_permission(self, permission_codename: str) -> bool:
        # Vérification directe des permissions utilisateur
        if any(p.codename == permission_codename for p in self.permissions):
            return True

        # Vérification des permissions via rôles
        for role in self.roles:
            if any(p.codename == permission_codename for p in role.permissions):
                return True

        return False

    def has_role(self, role_name: str) -> bool:
        return any(r.name == role_name for r in self.roles)
```

## 2. Interfaces des repositories

### 2.1. Interface PermissionRepository

```python
from abc import abstractmethod
from typing import List, Optional

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.interfaces.unit_of_work import BaseRepository


class PermissionRepository(BaseRepository):
    @abstractmethod
    def create_permission(self, permission: PermissionEntity) -> PermissionEntity:
        pass

    @abstractmethod
    def get_permission_by_codename(self, codename: str) -> Optional[PermissionEntity]:
        pass

    @abstractmethod
    def create_role(self, role: RoleEntity) -> RoleEntity:
        pass

    @abstractmethod
    def get_role_by_name(self, name: str) -> Optional[RoleEntity]:
        pass

    @abstractmethod
    def add_permission_to_role(self, role_name: str, permission_codename: str) -> bool:
        pass

    @abstractmethod
    def get_all_roles(self) -> List[RoleEntity]:
        pass

    @abstractmethod
    def get_all_permissions(self) -> List[PermissionEntity]:
        pass
```

### 2.2. Extension du UserRepository

```python
from abc import abstractmethod
from typing import List, Optional

from core.domain.entities.user_entity import UserEntity
from core.interfaces.unit_of_work import BaseRepository


class UserRepository(BaseRepository[UserEntity]):
    @abstractmethod
    def create_user(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def add_role_to_user(self, user_id: int, role_name: str) -> bool:
        pass

    @abstractmethod
    def add_permission_to_user(self, user_id: int, permission_codename: str) -> bool:
        pass

    @abstractmethod
    def has_permission(self, user_id: int, permission_codename: str) -> bool:
        pass

    @abstractmethod
    def has_role(self, user_id: int, role_name: str) -> bool:
        pass
```

## 3. Mise à jour de l'unité de travail

```python
from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from core.interfaces.permission_repository import PermissionRepository
from core.interfaces.user_repository import UserRepository

T = TypeVar("T")


class BaseRepository(Generic[T]):
    @abstractmethod
    def create(self, data: T) -> T:
        pass

    @abstractmethod
    def get(self, id) -> T:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def update(self, id, data: T) -> T:
        pass

    @abstractmethod
    def delete(self, id) -> bool:
        pass

    @abstractmethod
    def filter(self, **kwargs) -> list[T]:
        pass

    @abstractmethod
    def count(self, **kwargs) -> int:
        pass


class UnitOfWork(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    @abstractmethod
    def user_repository(self) -> UserRepository:
        pass

    @property
    @abstractmethod
    def permission_repository(self) -> PermissionRepository:
        pass
```

## 4. Implémentation des repositories

### 4.1. DjangoPermissionRepository

```python
from typing import List, Optional

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.interfaces.permission_repository import PermissionRepository


class DjangoPermissionRepository(PermissionRepository):

    def create_permission(self, permission: PermissionEntity) -> PermissionEntity:
        # Cette méthode est plus complexe car Django crée généralement les permissions
        # automatiquement pour les modèles enregistrés
        # Mais pour des permissions personnalisées, on peut faire:
        app_label, model = permission.codename.split('.')
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            # Créer un content type générique si nécessaire
            content_type = ContentType.objects.get_or_create(
                app_label='custom',
                model='permission'
            )[0]

        django_permission, created = Permission.objects.get_or_create(
            codename=permission.codename,
            name=permission.name,
            content_type=content_type
        )

        return self._permission_to_entity(django_permission)

    def get_permission_by_codename(self, codename: str) -> Optional[PermissionEntity]:
        try:
            permission = Permission.objects.get(codename=codename)
            return self._permission_to_entity(permission)
        except Permission.DoesNotExist:
            return None

    def create_role(self, role: RoleEntity) -> RoleEntity:
        # Dans Django, les rôles correspondent aux groupes
        group, created = Group.objects.get_or_create(name=role.name)

        # Ajouter les permissions au groupe
        for permission in role.permissions:
            try:
                django_permission = Permission.objects.get(codename=permission.codename)
                group.permissions.add(django_permission)
            except Permission.DoesNotExist:
                continue

        return self._role_to_entity(group)

    def get_role_by_name(self, name: str) -> Optional[RoleEntity]:
        try:
            group = Group.objects.get(name=name)
            return self._role_to_entity(group)
        except Group.DoesNotExist:
            return None

    def add_permission_to_role(self, role_name: str, permission_codename: str) -> bool:
        try:
            group = Group.objects.get(name=role_name)
            permission = Permission.objects.get(codename=permission_codename)
            group.permissions.add(permission)
            return True
        except (Group.DoesNotExist, Permission.DoesNotExist):
            return False

    def get_all_roles(self) -> List[RoleEntity]:
        groups = Group.objects.all().prefetch_related('permissions')
        return [self._role_to_entity(group) for group in groups]

    def get_all_permissions(self) -> List[PermissionEntity]:
        permissions = Permission.objects.all()
        return [self._permission_to_entity(permission) for permission in permissions]

    def _permission_to_entity(self, django_permission: Permission) -> PermissionEntity:
        return PermissionEntity(
            id=django_permission.id,
            name=django_permission.name,
            codename=django_permission.codename
        )

    def _role_to_entity(self, django_group: Group) -> RoleEntity:
        permissions = [self._permission_to_entity(p) for p in django_group.permissions.all()]
        return RoleEntity(
            id=django_group.id,
            name=django_group.name,
            permissions=permissions
        )

    def create(self, data):
        raise NotImplementedError("Utilisez create_role ou create_permission")

    def get(self, id):
        raise NotImplementedError()

    def get_all(self):
        return self.get_all_roles()

    def update(self, id, data):
        raise NotImplementedError()

    def delete(self, id):
        raise NotImplementedError()

    def filter(self, **kwargs):
        raise NotImplementedError()

    def count(self, **kwargs):
        raise NotImplementedError()
```

### 4.2. Extension du DjangoUserRepository

```python
from typing import Any, List, Optional
from uuid import UUID

from apps.users.models import User
from django.contrib.auth.models import Group, Permission
from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.domain.entities.user_entity import UserEntity
from core.interfaces.user_repository import UserRepository


class DjangoUserRepository(UserRepository):

    def create_user(self, user: UserEntity) -> UserEntity:
        django_user = User(
            email=user.email,
        )
        django_user.set_password(user.password)
        django_user.save()

        # Ajouter les rôles et permissions si spécifiés
        for role in user.roles:
            try:
                group = Group.objects.get(name=role.name)
                django_user.groups.add(group)
            except Group.DoesNotExist:
                continue

        for permission in user.permissions:
            try:
                perm = Permission.objects.get(codename=permission.codename)
                django_user.user_permissions.add(perm)
            except Permission.DoesNotExist:
                continue

        return self._to_entity(django_user)

    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            user = User.objects.get(email=email)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        try:
            user = User.objects.get(id=user_id)
            return self._to_entity(user)
        except User.DoesNotExist:
            return None

    def authenticate_user(self, login: str, password: str) -> Optional[UserEntity]:
        # Vérifier uniquement par email
        user = User.objects.filter(email=login).first()
        if user and user.check_password(password):
            return self._to_entity(user)
        return None

    def add_role_to_user(self, user_id: int, role_name: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(name=role_name)
            user.groups.add(group)
            user.save()
            return True
        except (User.DoesNotExist, Group.DoesNotExist):
            return False

    def add_permission_to_user(self, user_id: int, permission_codename: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            permission = Permission.objects.get(codename=permission_codename)
            user.user_permissions.add(permission)
            user.save()
            return True
        except (User.DoesNotExist, Permission.DoesNotExist):
            return False

    def has_permission(self, user_id: int, permission_codename: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            # has_perm vérifie à la fois les permissions directes et celles des groupes
            return user.has_perm(permission_codename)
        except User.DoesNotExist:
            return False

    def has_role(self, user_id: int, role_name: str) -> bool:
        try:
            user = User.objects.get(id=user_id)
            return user.groups.filter(name=role_name).exists()
        except User.DoesNotExist:
            return False

    def _to_entity(self, django_user: User) -> UserEntity:
        # Récupérer les rôles (groupes) de l'utilisateur
        roles = []
        for group in django_user.groups.all():
            permissions = [
                PermissionEntity(id=p.id, name=p.name, codename=p.codename)
                for p in group.permissions.all()
            ]
            roles.append(RoleEntity(id=group.id, name=group.name, permissions=permissions))

        # Récupérer les permissions directes de l'utilisateur
        permissions = [
            PermissionEntity(id=p.id, name=p.name, codename=p.codename)
            for p in django_user.user_permissions.all()
        ]

        return UserEntity(
            id=django_user.id,
            email=django_user.email,
            password="",  # We don't return the password
            active=django_user.active,
            roles=roles,
            permissions=permissions,
            updated_by=django_user.updated_by,
            created_at=django_user.created_at,
            updated_at=django_user.updated_at,
        )

    # ... autres méthodes existantes
```

### 4.3. Mise à jour du DjangoUnitOfWork

```python
from core.interfaces.permission_repository import PermissionRepository
from core.interfaces.unit_of_work import UnitOfWork
from core.interfaces.user_repository import UserRepository

from infrastructure.db.django_permission_repository import DjangoPermissionRepository
from infrastructure.db.django_user_repository import DjangoUserRepository


class DjangoUnitOfWork(UnitOfWork):
    def __init__(self):
        self._user_repository = None
        self._permission_repository = None

    def __enter__(self):
        # Initialisation des repositories
        self._user_repository = DjangoUserRepository()
        self._permission_repository = DjangoPermissionRepository()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Nettoyage si nécessaire
        self._user_repository = None
        self._permission_repository = None

    @property
    def user_repository(self) -> UserRepository:
        return self._user_repository

    @property
    def permission_repository(self) -> PermissionRepository:
        return self._permission_repository
```

## 5. Classes de permissions et rôles

### 5.1 Classes de base

```python
from abc import ABC, abstractmethod
from typing import List

from core.interfaces.unit_of_work import UnitOfWork


class BasePermission(ABC):
    codename: str = None

    @classmethod
    @abstractmethod
    def has_permission(cls, user_id: int, unit_of_work: UnitOfWork) -> bool:
        """Vérifie si l'utilisateur a cette permission"""
        pass


class BaseRole(ABC):
    name: str = None

    @classmethod
    @abstractmethod
    def has_role(cls, user_id: int, unit_of_work: UnitOfWork) -> bool:
        """Vérifie si l'utilisateur a ce rôle"""
        pass


class Permission(BasePermission):
    """
    Classe de base pour les permissions standard utilisant le système de permission Django
    """

    @classmethod
    def has_permission(cls, user_id: int, unit_of_work: UnitOfWork) -> bool:
        """Vérifie si l'utilisateur a cette permission via le repository"""
        if not cls.codename:
            raise ValueError(f"La classe {cls.__name__} doit définir un attribut codename")

        with unit_of_work as uow:
            user_repo = uow.user_repository
            return user_repo.has_permission(user_id, cls.codename)


class Role(BaseRole):
    """
    Classe de base pour les rôles standard utilisant le système de groupes Django
    """

    @classmethod
    def has_role(cls, user_id: int, unit_of_work: UnitOfWork) -> bool:
        """Vérifie si l'utilisateur a ce rôle via le repository"""
        if not cls.name:
            raise ValueError(f"La classe {cls.__name__} doit définir un attribut name")

        with unit_of_work as uow:
            user_repo = uow.user_repository
            return user_repo.has_role(user_id, cls.name)
```

### 5.2 Permissions spécifiques

```python
from presentation.permissions_and_roles import Permission, Role


class AddGroupPermission(Permission):
    codename = "auth.add_group"


class ChangeUserPermission(Permission):
    codename = "users.change_user"


class ViewUserPermission(Permission):
    codename = "users.view_user"


class AdminRole(Role):
    name = "Admin"


class EditorRole(Role):
    name = "Editor"


class ViewerRole(Role):
    name = "Viewer"
```

## 6. Cas d'utilisation pour la gestion des permissions

```python
import logging
from typing import List, Optional

from core.domain.entities.permission_entity import PermissionEntity, RoleEntity
from core.interfaces.unit_of_work import UnitOfWork


class PermissionUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
    ):
        self.unit_of_work = unit_of_work
        self.logger = logging.getLogger(__name__)

    def create_role(self, role_name: str) -> RoleEntity:
        """Crée un nouveau rôle"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository

            # Vérifier si le rôle existe déjà
            existing_role = permission_repo.get_role_by_name(role_name)
            if existing_role:
                return existing_role

            # Créer un nouveau rôle
            role = RoleEntity(name=role_name)
            created_role = permission_repo.create_role(role)

            return created_role

    def assign_permission_to_role(
        self, role_name: str, permission_codename: str
    ) -> bool:
        """Assigne une permission à un rôle"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository

            result = permission_repo.add_permission_to_role(
                role_name, permission_codename
            )

            if not result:
                self.logger.warning(
                    f"Échec lors de l'attribution de la permission '{permission_codename}' au rôle '{role_name}'"
                )

            return result

    def assign_role_to_user(self, user_id: int, role_name: str) -> bool:
        """Assigne un rôle à un utilisateur"""
        with self.unit_of_work as uow:
            user_repo = uow.user_repository

            result = user_repo.add_role_to_user(user_id, role_name)

            if not result:
                self.logger.warning(
                    f"Échec lors de l'attribution du rôle '{role_name}' à l'utilisateur ID:{user_id}"
                )

            return result

    def assign_permission_to_user(
        self, user_id: int, permission_codename: str
    ) -> bool:
        """Assigne une permission directement à un utilisateur"""
        with self.unit_of_work as uow:
            user_repo = uow.user_repository

            result = user_repo.add_permission_to_user(
                user_id, permission_codename
            )

            if not result:
                self.logger.warning(
                    f"Échec lors de l'attribution de la permission '{permission_codename}' à l'utilisateur ID:{user_id}"
                )

            return result

    def check_user_permission(
        self, user_id: int, permission_codename: str
    ) -> bool:
        """Vérifie si un utilisateur a une permission spécifique"""
        with self.unit_of_work as uow:
            user_repo = uow.user_repository
            return user_repo.has_permission(user_id, permission_codename)

    def check_user_role(
        self, user_id: int, role_name: str
    ) -> bool:
        """Vérifie si un utilisateur a un rôle spécifique"""
        with self.unit_of_work as uow:
            user_repo = uow.user_repository
            return user_repo.has_role(user_id, role_name)

    def get_all_roles(self) -> List[RoleEntity]:
        """Récupère tous les rôles"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository
            return permission_repo.get_all_roles()

    def get_all_permissions(self) -> List[PermissionEntity]:
        """Récupère toutes les permissions"""
        with self.unit_of_work as uow:
            permission_repo = uow.permission_repository
            return permission_repo.get_all_permissions()
```

## 7. Décorateurs de permission basés sur des classes

```python
import functools
from typing import List, Type, Union

from django.contrib.auth.models import AnonymousUser
from ninja.errors import HttpError
from http import HTTPStatus

from presentation.permissions_and_roles import BasePermission, BaseRole


def permissions_required(*permission_classes: Type[BasePermission]):
    """
    Décorateur qui vérifie si l'utilisateur a au moins une des permissions spécifiées.
    Utilise des classes de permission au lieu de chaînes.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(controller, request, *args, **kwargs):
            # Vérifier si l'utilisateur est authentifié
            if not hasattr(request, 'auth') or not request.auth:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Non authentifié")

            user_id = request.auth.get("user_id")
            if not user_id:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "ID utilisateur non trouvé")

            # Vérifier au moins une permission
            unit_of_work = controller.unit_of_work

            if not any(perm.has_permission(user_id, unit_of_work) for perm in permission_classes):
                permission_names = ", ".join([p.__name__ for p in permission_classes])
                raise HttpError(
                    HTTPStatus.FORBIDDEN,
                    f"Permissions insuffisantes. Requises: {permission_names}"
                )

            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator


def all_permissions_required(*permission_classes: Type[BasePermission]):
    """
    Décorateur qui vérifie si l'utilisateur a toutes les permissions spécifiées.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(controller, request, *args, **kwargs):
            # Vérifier si l'utilisateur est authentifié
            if not hasattr(request, 'auth') or not request.auth:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Non authentifié")

            user_id = request.auth.get("user_id")
            if not user_id:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "ID utilisateur non trouvé")

            # Vérifier toutes les permissions
            unit_of_work = controller.unit_of_work

            missing_permissions = []
            for perm in permission_classes:
                if not perm.has_permission(user_id, unit_of_work):
                    missing_permissions.append(perm.__name__)

            if missing_permissions:
                raise HttpError(
                    HTTPStatus.FORBIDDEN,
                    f"Permissions manquantes: {', '.join(missing_permissions)}"
                )

            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator


def roles_required(*role_classes: Type[BaseRole]):
    """
    Décorateur qui vérifie si l'utilisateur a au moins un des rôles spécifiés.
    Utilise des classes de rôle au lieu de chaînes.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(controller, request, *args, **kwargs):
            # Vérifier si l'utilisateur est authentifié
            if not hasattr(request, 'auth') or not request.auth:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Non authentifié")

            user_id = request.auth.get("user_id")
            if not user_id:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "ID utilisateur non trouvé")

            # Vérifier au moins un rôle
            unit_of_work = controller.unit_of_work

            if not any(role.has_role(user_id, unit_of_work) for role in role_classes):
                role_names = ", ".join([r.__name__ for r in role_classes])
                raise HttpError(
                    HTTPStatus.FORBIDDEN,
                    f"Rôles insuffisants. Requis: {role_names}"
                )

            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator


def all_roles_required(*role_classes: Type[BaseRole]):
    """
    Décorateur qui vérifie si l'utilisateur a tous les rôles spécifiés.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(controller, request, *args, **kwargs):
            # Vérifier si l'utilisateur est authentifié
            if not hasattr(request, 'auth') or not request.auth:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "Non authentifié")

            user_id = request.auth.get("user_id")
            if not user_id:
                raise HttpError(HTTPStatus.UNAUTHORIZED, "ID utilisateur non trouvé")

            # Vérifier tous les rôles
            unit_of_work = controller.unit_of_work

            missing_roles = []
            for role in role_classes:
                if not role.has_role(user_id, unit_of_work):
                    missing_roles.append(role.__name__)

            if missing_roles:
                raise HttpError(
                    HTTPStatus.FORBIDDEN,
                    f"Rôles manquants: {', '.join(missing_roles)}"
                )

            return func(controller, request, *args, **kwargs)
        return wrapper
    return decorator
```

## 8. Schémas de données pour l'API

```python
from typing import List, Optional
from ninja import Schema


class PermissionSchema(Schema):
    id: Optional[int] = None
    name: str
    codename: str


class RoleSchema(Schema):
    id: Optional[int] = None
    name: str
    permissions: List[PermissionSchema] = []


class RoleAssignmentSchema(Schema):
    role_name: str
    user_id: int


class PermissionAssignmentSchema(Schema):
    permission_codename: str
    role_name: str
```

## 9. Mise à jour des schémas utilisateur

```python
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ninja import Schema
from pydantic import ConfigDict, EmailStr

from presentation.schemas.base_schema import BaseSchema
from presentation.schemas.permission_schema import PermissionSchema, RoleSchema


class UserBase(Schema):
    email: EmailStr


class UserCreate(Schema):
    email: EmailStr
    password: str


class UserSignUp(Schema):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    id: UUID
    email_verified: bool


class UserOut(UserInDB):
    pass


class ClientOut(UserOut):
    client_type: str


class UserAuthSchema(BaseSchema):
    id: Optional[int] = None
    email: EmailStr
    active: bool = True
    roles: List[RoleSchema] = []
    permissions: List[PermissionSchema] = []
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
```

## 10. Contrôleur API pour la gestion des rôles et permissions

```python
import logging

from ninja_extra import api_controller, http_get, http_post

from core.use_cases.permission_use_case import PermissionUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import jwt_auth
from presentation.decorators.permission_decorators import permissions_required, roles_required
from presentation.exceptions import InternalServerError
from presentation.permissions import AddGroupPermission, ChangeUserPermission, AdminRole
from presentation.schemas.error_schema import ErrorResponseSchema
from presentation.schemas.permission_schema import (
    PermissionAssignmentSchema,
    PermissionSchema,
    RoleAssignmentSchema,
    RoleSchema,
)


@api_controller("/roles", tags=["Roles & Permissions"], auth=jwt_auth)
class RoleController:
    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.permission_use_case = PermissionUseCase(self.unit_of_work)
        self.logger = logging.getLogger(__name__)

    @http_post(
        "/create",
        response={
            201: dict,
            403: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    @permissions_required(AddGroupPermission)
    def create_role(self, request, role_name: str):
        try:
            role = self.permission_use_case.create_role(role_name)
            return {"message": f"Rôle '{role_name}' créé avec succès", "role_id": role.id}
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du rôle: {str(e)}", exc_info=True)
            raise InternalServerError()

    @http_post(
        "/assign_permission",
        response={
            200: dict,
            403: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    @roles_required(AdminRole)
    def assign_permission_to_role(self, request, data: PermissionAssignmentSchema):
        try:
            result = self.permission_use_case.assign_permission_to_role(
                data.role_name, data.permission_codename
            )
            if result:
                return {"message": f"Permission '{data.permission_codename}' ajoutée au rôle '{data.role_name}'"}
            return {"message": "Échec de l'attribution de la permission", "success": False}
        except Exception as e:
            self.logger.error(f"Erreur lors de l'attribution de la permission: {str(e)}", exc_info=True)
            raise InternalServerError()

    @http_post(
        "/assign_to_user",
        response={
            200: dict,
            403: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    @permissions_required(ChangeUserPermission)
    def assign_role_to_user(self, request, data: RoleAssignmentSchema):
        try:
            result = self.permission_use_case.assign_role_to_user(data.user_id, data.role_name)
            if result:
                return {"message": f"Rôle '{data.role_name}' attribué à l'utilisateur ID:{data.user_id}"}
            return {"message": "Échec de l'attribution du rôle", "success": False}
        except Exception as e:
            self.logger.error(f"Erreur lors de l'attribution du rôle: {str(e)}", exc_info=True)
            raise InternalServerError()

    @http_get(
        "/list",
        response={
            200: List[RoleSchema],
            403: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def list_roles(self, request):
        try:
            roles = self.permission_use_case.get_all_roles()
            return roles
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des rôles: {str(e)}", exc_info=True)
            raise InternalServerError()

    @http_get(
        "/permissions",
        response={
            200: List[PermissionSchema],
            403: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def list_permissions(self, request):
        try:
            permissions = self.permission_use_case.get_all_permissions()
            return permissions
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des permissions: {str(e)}", exc_info=True)
            raise InternalServerError()
```

## 11. Commande de gestion Django pour initialiser les rôles et permissions

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.users.models import User


class Command(BaseCommand):
    help = 'Configure les rôles et permissions de base'

    def handle(self, *args, **kwargs):
        self.stdout.write('Configuration des rôles et permissions...')

        # Création des groupes de base
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        editor_group, _ = Group.objects.get_or_create(name='Editor')
        viewer_group, _ = Group.objects.get_or_create(name='Viewer')

        # Récupération des permissions importantes
        user_permissions = Permission.objects.filter(
            content_type__app_label='users',
            content_type__model='user'
        )

        # Attribution des permissions aux groupes
        # Admin peut tout faire
        for perm in Permission.objects.all():
            admin_group.permissions.add(perm)

        # Éditeurs peuvent modifier les données mais pas les utilisateurs
        for perm in Permission.objects.filter(codename__startswith='change_'):
            if not perm.content_type.app_label == 'users':
                editor_group.permissions.add(perm)

        # Viewers peuvent seulement voir
        for perm in Permission.objects.filter(codename__startswith='view_'):
            viewer_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Rôles et permissions configurés avec succès !'))

        # Ajouter un admin par défaut si nécessaire
        if kwargs.get('create_admin'):
            email = kwargs.get('admin_email', 'admin@example.com')
            password = kwargs.get('admin_password', 'adminpassword')

            try:
                admin_user = User.objects.get(email=email)
                admin_user.set_password(password)
                admin_user.save()
                self.stdout.write(f'Mot de passe de l\'admin {email} mis à jour')
            except User.DoesNotExist:
                admin_user = User.objects.create_superuser(email=email, password=password)
                self.stdout.write(f'Admin créé avec email {email} et mot de passe spécifié')

            # Assurez-vous que l'admin est dans le groupe Admin
            admin_user.groups.add(admin_group)
```

## 12. Exemple d'utilisation avec le contrôleur existant

Mise à jour du AuthController pour utiliser les nouvelles permissions:

```python
import logging

from ninja_extra import api_controller, http_get, http_post, route
from pydantic import ValidationError as PydanticValidationError

from core.use_cases.auth_use_case import AuthUseCase
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork
from infrastructure.external_services.jwt_service import JWTService, jwt_auth
from presentation.decorators.permission_decorators import permissions_required, roles_required
from presentation.exceptions import (
    AuthenticationError,
    ConflictError,
    InternalServerError,
    InvalidTokenError,
    ValidationError,
)
from presentation.permissions import AdminRole, ViewUserPermission
from presentation.schemas.auth_schema import Login, TokenSchema
from presentation.schemas.error_schema import ErrorResponseSchema
from presentation.schemas.user_schema import UserAuthSchema, UserSignUp


@api_controller("/auth", tags=["Authentication"])
class AuthController:
    def __init__(self):
        self.unit_of_work = DjangoUnitOfWork()
        self.jwt_service = JWTService()
        self.auth_use_case = AuthUseCase(
            self.unit_of_work,
            self.jwt_service,
        )
        self.logger = logging.getLogger(__name__)

    @route.post(
        "/signup",
        response={
            201: UserAuthSchema,
            422: ErrorResponseSchema,
            409: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def sign_up(self, user_data: UserSignUp):
        try:
            user = self.auth_use_case.register_user(
                user_data.email, user_data.password
            )
            return user
        except PydanticValidationError as e:
            raise ValidationError(e)
        except ConflictError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Erreur lors de l'inscription: {str(e)}", exc_info=True)
            raise InternalServerError()

    @route.post(
        "/login",
        response={
            200: TokenSchema,
            401: ErrorResponseSchema,
            422: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def login(self, data: Login):
        try:
            tokens = self.auth_use_case.login(data.email, data.password)
            return tokens
        except AuthenticationError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Erreur lors de la connexion: {str(e)}", exc_info=True)
            raise InternalServerError()

    @route.post(
        "/refresh",
        response={
            200: TokenSchema,
            401: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
    )
    def refresh_token(self, refresh_token: str):
        try:
            tokens = self.auth_use_case.refresh_token(refresh_token)
            return tokens
        except InvalidTokenError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Erreur lors du rafraîchissement du token: {str(e)}", exc_info=True)
            raise InternalServerError()

    @http_get("/me", response=UserAuthSchema, auth=jwt_auth)
    def get_current_user(self, request):
        try:
            user_id = request.auth.get("user_id")
            user = self.auth_use_case.get_user_by_id(user_id)
            return user
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération de l'utilisateur: {str(e)}", exc_info=True)
            raise InternalServerError()

    @http_post(
        "/logout",
        response={
            200: dict,
            401: ErrorResponseSchema,
            500: ErrorResponseSchema,
        },
        auth=jwt_auth,
    )
    def logout(self, request, refresh_token: str):
        try:
            self.auth_use_case.logout(refresh_token)
            return {"message": "Déconnexion réussie"}
        except InvalidTokenError as e:
            raise e
        except Exception as e:
            self.logger.error(f"Erreur lors de la déconnexion: {str(e)}", exc_info=True)
            raise InternalServerError()

    @http_get(
        "/admin-only",
        response={
            200: dict,
            401: ErrorResponseSchema,
            403: ErrorResponseSchema,
        },
        auth=jwt_auth,
    )
    @roles_required(AdminRole)
    def admin_only(self, request):
        return {"message": "Vous êtes administrateur"}

    @http_get(
        "/users-view",
        response={
            200: dict,
            401: ErrorResponseSchema,
            403: ErrorResponseSchema,
        },
        auth=jwt_auth,
    )
    @permissions_required(ViewUserPermission)
    def view_users_permission(self, request):
        return {"message": "Vous avez la permission de voir les utilisateurs"}
```

## 13. Utilisation et exemples

### 13.1 Comment définir une nouvelle permission ou un nouveau rôle

Pour créer une nouvelle permission ou un nouveau rôle:

1. Ajoutez-les au fichier `presentation/permissions.py`:

   ```python
   class CreateArticlePermission(Permission):
       codename = "articles.add_article"

   class ArticleEditorRole(Role):
       name = "ArticleEditor"
   ```

2. Utilisez les décorateurs dans vos contrôleurs:

   ```python
   @permissions_required(CreateArticlePermission)
   def create_article(self, request, data: ArticleCreateSchema):
       # ...

   @roles_required(ArticleEditorRole)
   def edit_article(self, request, article_id: int, data: ArticleUpdateSchema):
       # ...
   ```

### 13.2 Comment initialiser les rôles et permissions

Exécutez la commande Django suivante:

```bash
python manage.py setup_permissions --create_admin --admin_email=admin@example.com --admin_password=secure_password
```

### 13.3 Comment tester les permissions

```python
from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from apps.users.models import User

from presentation.permissions import AdminRole, CreateArticlePermission
from infrastructure.db.django_unit_of_work import DjangoUnitOfWork


class PermissionTests(TestCase):
    def setUp(self):
        # Créer un utilisateur de test
        self.user = User.objects.create_user(email="test@example.com", password="testpass")

        # Créer le groupe Admin
        self.admin_group = Group.objects.create(name="Admin")

        # Ajouter toutes les permissions au groupe Admin
        for perm in Permission.objects.all():
            self.admin_group.permissions.add(perm)

    def test_admin_role(self):
        # Vérifier que l'utilisateur n'a pas le rôle Admin
        uow = DjangoUnitOfWork()
        self.assertFalse(AdminRole.has_role(self.user.id, uow))

        # Ajouter l'utilisateur au groupe Admin
        self.user.groups.add(self.admin_group)

        # Vérifier que maintenant l'utilisateur a le rôle Admin
        self.assertTrue(AdminRole.has_role(self.user.id, uow))

    def test_permission(self):
        # Vérifier que l'utilisateur n'a pas la permission
        uow = DjangoUnitOfWork()
        self.assertFalse(CreateArticlePermission.has_permission(self.user.id, uow))

        # Ajouter l'utilisateur au groupe Admin (qui a toutes les permissions)
        self.user.groups.add(self.admin_group)

        # Vérifier que maintenant l'utilisateur a la permission
        self.assertTrue(CreateArticlePermission.has_permission(self.user.id, uow))
```

Cette implémentation respecte pleinement votre architecture existante en ajoutant la gestion des rôles et permissions de manière cohérente, facilement extensible et maintenable. Elle utilise des classes pour les permissions et les rôles, ce qui offre une meilleure réutilisabilité et un typage plus fort que les simples chaînes de caractères.
