from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path(
        'openapi/',
        TemplateView.as_view(template_name='index.html'),
        name='openapi'
    ),
]
