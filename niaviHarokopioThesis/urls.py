"""niaviHuaThesis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from niaviHarokopioThesis.views import (
    HomePage,
    informatics_page_view,
    login_page_view,
    signup_page_view,
    profile_page_view ,
    add_education_info_view,
    student_education_dashboard,
    edit_basic_info,
    education_info_details,
    create_new_degree,
    create_new_work_experience,
    job_info_details,
    create_new_reccomendation,
    recommendation_details,
    # create_new_application,
    departments,
    create_application_for_program,
    create_new_language,
    student_dashboard,
    language_details,
    create_application_pdf,
    edit_additional_info,
    activate,
    my_applications,
    view_my_application,
    applfinalization,
    select_applications_for_program,
    contact,
	)


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('captcha/', include('captcha.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', HomePage , name='home'),
    path('informatics', informatics_page_view , name='informatics'),
    path('login',  login_page_view , name='user_login'),
    path('signup', signup_page_view , name='signup'),
    path('profile', profile_page_view , name='profile'),
    # path('application', create_new_application , name='application'),
    path('add_education', add_education_info_view , name='add_education'),
    path('my_dashboard', student_education_dashboard, name='user_dashboard'),
    path('edit_basic_info/<str:pk>', edit_basic_info, name='edit_basic_info'),
    path('education_info_details/<str:pk>', education_info_details, name='education_info_details'),
    path('new_degree/<str:pk>', create_new_degree, name='create_new_degree'),
    path('new_work_experience/<str:pk>', create_new_work_experience, name='create_new_work_experience'),
    path('job_info_details/<str:pk>', job_info_details, name='job_info_details'),
    path('new_reccomendation/<str:pk>', create_new_reccomendation, name='create_new_reccomendation'),
    path('recommendation_details/<str:pk>', recommendation_details, name='recommendation_details'),
    path('departments', departments, name='departments'),
    path('create_application_for_program/<str:pk>', create_application_for_program, name='create_application_for_program'),
    path('new_language/<str:pk>', create_new_language, name='create_new_language'),
    path('language_details/<str:pk>', language_details, name='language_details'),
    path('my_dashboard/<str:pk>', student_dashboard, name='student_dashboard'),
    path('create_application_pdf/<str:pk>', create_application_pdf, name='create_application_pdf'),
    path('edit_additional_info/<str:pk>', edit_additional_info, name='edit_additional_info'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('my_applications', my_applications , name='my_applications'),
    path('view_my_application/<str:pk>', view_my_application, name='view_my_application'),
    path('applfinalization/<str:pk>', applfinalization, name='applfinalization'),
    path('select_applications_for_program/<str:pk>', select_applications_for_program, name='select_applications_for_program'),
    path('contact/', contact, name='contact'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
