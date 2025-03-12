from django.urls import path
from BinThere import views

app_name = 'BinThere'

#CHAPTER 14/15 ADDITIONS - Adding Classes structure to Views
from BinThere.views import HomeView, RegisterProfileView, ProfileView, ListProfilesView, BinCreateView, BinUpdateView, BinListView, BinMapView, Vote



urlpatterns = [
    #Updated path that point to the new about class-based views.
    path('', HomeView.as_view(), name='home'),
    path('BinMap/', BinMapView.as_view(), name='bin_map'),
    path('add/', BinCreateView.as_view(), name='add_bin'),
    path('edit/<int:pk>/', BinUpdateView.as_view(), name='edit_bin'),

    path('vote/<int:bin_id>/<int:vote_type>/', Vote.as_view(), name='vote'),  # vote_type: 1 for upvote, -1 for downvote
    path('BinMap/BinList', BinListView.as_view(), name='bin_list'),
    path('accounts/register/', RegisterProfileView.as_view(), name='register'),
    path('profile/<username>/', ProfileView.as_view(), name='profile'),
    path('profiles/', ListProfilesView.as_view(), name='list_profiles'),

    

]

