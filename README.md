# 🍽️ Recipe API - Projeto Django com Django REST Framework

> API REST completa para gerenciamento de receitas culinárias, desenvolvida com Django 5.x e Django REST Framework.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Tecnologias](#-tecnologias)
- [Funcionalidades](#-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [API Endpoints](#-api-endpoints)
- [Modelos](#-modelos)
- [Testes](#-testes)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

---

## 📖 Visão Geral

Este é um projeto Django completo que combina:
- **Frontend**: Templates Django renderizados no servidor
- **Backend**: API RESTful com Django REST Framework
- **Autenticação**: JWT (JSON Web Tokens) via SimpleJWT
- **Testes**: Pytest com cobertura de código

O sistema permite o gerenciamento de receitas culinárias com categorias, autores, e uma interface de administração completa.

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Django | 5.x | Framework web Python full-stack |
| Django REST Framework | 3.15+ | Framework para APIs REST |
| SimpleJWT | latest | Autenticação via JSON Web Tokens |
| Python | 3.10+ | Linguagem de programação |
| pytest | latest | Framework de testes |
| SQLite | - | Banco de dados (desenvolvimento) |
| CORS Headers | latest | Configuração de CORS para API |

---

## ✨ Funcionalidades

### Módulo de Receitas
- ✅ Listagem de receitas com paginação customizada
- ✅ Busca por título e descrição
- ✅ Filtragem por categoria
- ✅ Detail view de receitas
- ✅ API REST com paginação (PageNumberPagination)
- ✅ Serializer com validações customizadas
- ✅ Permissões granulares (Owner para PATCH/DELETE)
- ✅ Campos calculados via annotations (Concat)

### Módulo de Autores/Usuários
- ✅ Registro de usuários com validação
- ✅ Login com formulários Django
- ✅ Dashboard pessoal
- ✅ CRUD de receitas do autor
- ✅ Perfil público de autores
- ✅ Validadores customizados (senha forte, etc)
- ✅ API RESTful somente leitura (ReadOnlyModelViewSet)

### Utilitários
- ✅ Paginação customizada com range dinâmico
- ✅ Validadores de strings e formulários
- ✅ Signals para criação automática de perfis

---

## 📁 Estrutura do Projeto

```
PYTHON_TESTES/
├── project/                 # Configurações do projeto Django
│   ├── settings.py         # Settings principal
│   └── urls.py             # URLs raiz
├── recipes/                # App de receitas
│   ├── models.py           # Modelos Category e Recipe
│   ├── views/
│   │   ├── api.py          # ViewSet API REST
│   │   └── site.py         # Views Django (ListView, DetailView)
│   ├── serializers.py     # Serializers DRF
│   ├── permissions.py      # Permissões customizadas
│   ├── urls.py             # Rotas do app
│   └── admin.py            # Configuração admin
├── authors/                # App de autores/usuários
│   ├── models.py           # Modelos personalizados
│   ├── views/
│   │   ├── api.py          # ViewSet para API
│   │   ├── all.py          # Views diversas
│   │   ├── dashboard_recipe.py
│   │   └── profile.py
│   ├── forms/
│   │   ├── login.py        # Formulário de login
│   │   ├── register_form.py # Formulário de registro
│   │   └── recipe_form.py
│   ├── serializers.py     # Serializers de autores
│   ├── validators.py      # Validadores customizados
│   ├── signals.py         # Signals Django
│   └── urls.py            # Rotas do app
├── utils/                 # Módulo de utilitários
│   ├── pagination.py      # Paginação customizada
│   ├── django_forms.py    # Helpers para formulários
│   ├── strings.py         # Utilitários de string
│   └── environment.py    # Variáveis de ambiente
├── base_templates/        # Templates base
├── static/                # Arquivos estáticos
├── media/                 # Arquivos de mídia (uploads)
├── manage.py              # Script de gerenciamento Django
├── requirements.txt       # Dependências Python
└── pytest.ini             # Configuração do pytest
```

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
cd PYTHON_TESTES
```

### 2. Crie um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute as migrações

```bash
python manage.py migrate
```

### 5. Crie um superusuário (opcional)

```bash
python manage.py createsuperuser
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

A aplicação estará disponível em `http://127.0.0.1:8000/`

---

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=1
SECRET_KEY_JWT=sua-chave-jwt-aqui
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
PER_PAGE=6
```

### Configurações Principais

As configurações estão em [project/settings.py](project/settings.py):

- **DEBUG**: Modo de desenvolvimento
- **ALLOWED_HOSTS**: Hosts permitidos
- **REST_FRAMEWORK**: Configurações da API
- **SIMPLE_JWT**: Configurações de autenticação JWT
- **CORS**: Configuração de Cross-Origin Resource Sharing

---

## 🔌 API Endpoints

### API v1 (Django Views como JSON)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/recipes/api/v1/` | Lista todas as receitas publicadas |
| GET | `/recipes/api/v1/<int:pk>/` | Detalha uma receita específica |

### API v2 (Django REST Framework)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/recipes/api/v2/recipes/` | Lista receitas com paginação |
| POST | `/recipes/api/v2/recipes/` | Cria uma nova receita |
| GET | `/recipes/api/v2/recipes/<int:pk>/` | Detalha uma receita |
| PATCH | `/recipes/api/v2/recipes/<int:pk>/` | Atualiza parcialmente |
| DELETE | `/recipes/api/v2/recipes/<int:pk>/` | Remove uma receita |

#### Parâmetros de Query

```
/recipes/api/v2/recipes/?category_id=1
```

### Autenticação JWT

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/recipes/api/token/` | Obtém token de acesso |
| POST | `/recipes/api/token/refresh/` | Refresh do token |
| POST | `/recipes/api/token/verify/` | Verifica token |

### Autores API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/authors/api/` | Lista autores |
| GET | `/authors/api/me/` | Dados do usuário atual |

### Endpoints do Site

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Home - Lista de receitas |
| GET | `/recipes/search/?q=termo` | Busca de receitas |
| GET | `/recipes/category/<int:category_id>/` | Receitas por categoria |
| GET | `/recipes/<int:pk>/` | Detail de receita |
| GET | `/authors/register/` | Página de registro |
| GET | `/authors/login/` | Página de login |
| GET | `/authors/dashboard/` | Dashboard do usuário |
| GET | `/authors/profile/<int:id>/` | Perfil público do autor |

---

## 📊 Modelos

### Category

```python
class Category(models.Model):
    name = models.CharField(max_length=65)
    slug = models.SlugField(unique=True)
```

### Recipe

```python
class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/')
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### Manager Personalizado

```python
class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')')
            )
        ).order_by('-id').select_related('category', 'author')
```

---

## 🧪 Testes

### Executar Todos os Testes

```bash
pytest
```

### Executar com Cobertura

```bash
pytest --cov=recipes --cov=authors --cov=project
```

### Executar Testes Específicos

```bash
# Testes rápidos
pytest -m fast

# Testes lentos
pytest -m slow

# Testes funcionais (Selenium)
pytest -m functional_test
```

### Configuração

O projeto utiliza [pytest.ini](pytest.ini) com:
- Suporte a testes Django
- Configuração de markers (`slow`, `fast`, `functional_test`)
- Doctest modules ativado

---

## 📦 Serializers

### RecipeSerializer

```python
class RecipeSerializer(serializers.ModelSerializer):
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)
```

**Campos expostos**: `id`, `title`, `description`, `public`, `preparation`, `author`, `category`, `preparation_time`, `preparation_time_unit`, `servings`, `servings_unit`, `preparation_steps`, `cover`

### Validações Customizadas

O serializer utiliza `AuthorRecipeValidator` para:
- Validar que título tem pelo menos 5 caracteres
- Validar que `preparation_time` é número positivo
- Validar que `servings` é número positivo
- Garantir que título ≠ descrição

---

## 🔐 Permissões

### IsOwner

Permissão customizada que permite:
- **Leitura (GET)**: Qualquer usuário autenticado ou anônimo
- **Edição (PATCH)**: Apenas o autor da receita
- **Remoção (DELETE)**: Apenas o autor da receita

```python
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
```

---

## 📈 Paginação

### Custom Pagination

O projeto implementa paginação customizada em [utils/pagination.py](utils/pagination.py):

```python
def make_pagination_range(page_range, qty_pages, current_page):
    # Retorna range dinâmico de páginas
    # com suporte a primeiro/última página fora do range
```

### API v2 Pagination

```python
class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2
```

---

## 🛡️ Validadores

### RegisterForm

- Username: 4-150 caracteres
- Validação de email único
- Confirmação de senha
- Validador de senha forte (`strong_password`)

### AuthorRecipeValidator

- Título mínimo de 5 caracteres
- Tempo de preparo deve ser número positivo
- Porções devem ser número positivo
- Título não pode ser igual à descrição

---

## 📝 Rotas Principais

### URLs do Projeto

```python
# project/urls.py
urlpatterns = [
    path('', include('recipes.urls')),
    path('authors/', include('authors.urls')),
    path('admin/', admin.site.urls),
]
```

---

## 🎨 Templates

O projeto utiliza templates Django em:
- `base_templates/` - Templates base
- `recipes/templates/` - Templates de receitas
- `authors/templates/` - Templates de autores

---

## 📱 Media Files

Imagens de receitas são armazenadas em:
```
media/recipes/covers/%Y/%m/%d/
```

Configurado via `MEDIA_URL` e `MEDIA_ROOT` em settings.

---

## 🔧 Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Shell Django
python manage.py shell

# Verificar código
python manage.py check

# Servidor com porta específica
python manage.py runserver 8080
```

---

## 🤝 Contribuição

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🙏 Agradecimentos

- [Django](https://www.djangoproject.com/) - Framework web
- [Django REST Framework](https://www.django-rest-framework.org/) - API REST
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/) - Autenticação JWT

---

**Desenvolvido por José Antonio usando Django e Django REST Framework**