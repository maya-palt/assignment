"""
URL configuration for certificate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import  create_certificate,view_certificate, generate_certificate_pdf,certificate_pdf,verify_certificate,register_view,login_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('verify/', verify_certificate, name='verify_certificate'),
    # path('check/<int:certificate_id>/', views.view_certificate, name='view_certificate'),
    path('check/<int:certificate_id>/', view_certificate, name='check'),
    path('create/', create_certificate, name='create'),
    path('certificates/pdfs/<int:certificate_id>.pdf', views.certificate_pdf, name='certificate_pdf'),

    path('certificates/pdfs/<int:certificate_id>.pdf', views.certificate_pdf, name='certificate_pdf'),
    path('certificates/pdfs/<int:certificate_id>.pdf', views.generate_certificate_pdf, name='generate_certificate_pdf'),
    # # path('verify-certificate/', views.verify_certificate, name='verify_certificate'),

    # path('show/', show_verification_form, name='show'),
    path('register/', register_view, name='register'),
    # path('home/', home, name='home'),
    path('login/', login_view, name='login'),
    # path('certificates/pdfs/<int:certificate_id>.pdf', views.generate_certificate_pdf, name='generate_certificate_pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

