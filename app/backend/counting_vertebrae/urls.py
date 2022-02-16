
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
# from .subscriber import start_listening

urlpatterns = [
    path('admin/', admin.site.urls),
    path('detect/', include('detector.urls'), name="detector"),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    # re_path(r"\S", TemplateView.as_view(template_name="index.html")),
]

# start_listening()