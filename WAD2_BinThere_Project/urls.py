"""WAD2_BinThere_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include
from django.urls import reverse
from BinThere import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from registration.backends.simple.views import RegistrationView
from BinThere.views import HomeView


class MyRegistrationView(RegistrationView): 
    def get_success_url(self, user):
        return reverse('BinThere:register_profile') # pragma: no cover



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('BinThere/', include('BinThere.urls')),
    # The above maps any URLs starting with BinThere/ to be handled by BinThere.
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    
    # New line below -- don't forget the slash after register!
    path('accounts/register/', MyRegistrationView.as_view(), name='registration_register'),

    # Include media urls connector to ensure all media urls are properly formatted.
    path('accounts/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)