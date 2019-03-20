"""MedResults URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from Mrecords.views import AddUser
from Mrecords.views import ClinicOps
from Mrecords.views import ClinicUpdate
from Mrecords.views import ClinicDelete
from Mrecords.views import SpecialistOps
from Mrecords.views import SpecialistUpdate
from Mrecords.views import SpecialistDelete
from Mrecords.views import ExaminationOps
from Mrecords.views import ExaminationUpdate
from Mrecords.views import ExaminationDelete
from Mrecords.views import FileOps
from Mrecords.views import FileUpdate
from Mrecords.views import FileDelete
from Mrecords.views import BokehOps

from django.conf import settings

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('rejestracja/', AddUser.as_view(), name='register'),
    path('admin/', admin.site.urls),
    path('clinic/', ClinicOps.as_view(), name='c_ops'),
    path('clinic/<int:clinic_id>', ClinicUpdate.as_view(), name='c_upd'),
    path('clinic_delete/<int:clinic_id>', ClinicDelete.as_view(), name='c_del'),
    path('specialist', SpecialistOps.as_view(), name='s_ops'),
    path('specialist/<int:specialist_id>', SpecialistUpdate.as_view(), name='s_upd'),
    path('specialist_delete/<int:specialist_id>', SpecialistDelete.as_view(), name='s_del'),
    path('examination', ExaminationOps.as_view(), name='e_ops'),
    path('examination/<int:examination_id>', ExaminationUpdate.as_view(), name='e_upd'),
    path('examination_delete/<int:examination_id>', ExaminationDelete.as_view(), name='e_del'),
    path('file', FileOps.as_view(), name='f_ops'),
    path('file/<int:file_id>', FileUpdate.as_view(), name='f_upd'),
    path('file_delete/<int:file_id>', FileDelete.as_view(), name='f_del'),
    path('wykres/', BokehOps.as_view(), name='b_ops'),]

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
