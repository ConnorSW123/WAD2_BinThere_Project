from django.urls import path
from BinThere import views

app_name = 'BinThere'

#CHAPTER 14/15 ADDITIONS - Adding Classes structure to Views
from BinThere.views import AboutView


urlpatterns = [
    #Updated path that point to the new about class-based views.
    path('', AboutView.as_view(), name='about'),
    ]