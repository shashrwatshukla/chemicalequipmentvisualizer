from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# We removed 're_path' and 'TemplateView' imports because we don't need them anymore.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ❌ DELETED: The block that was here trying to serve 'index.html'
# urlpatterns += [
#    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
# ]