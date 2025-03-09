from django.urls import path
from BinThere import views

app_name = 'BinThere'

#CHAPTER 14/15 ADDITIONS - Adding Classes structure to Views
from BinThere.views import AboutView


urlpatterns = [
    #Updated path that point to the new about class-based views.
    path('', AboutView.as_view(), name='about'),
    path('map/', views.map, name='map'),
    path('vote/<int:bin_id>/<int:vote_type>/', views.vote, name='vote'),  # vote_type: 1 for upvote, -1 for downvote


]
