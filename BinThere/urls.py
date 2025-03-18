from django.urls import path

app_name = 'BinThere'

# Adding Classes structure to Views
from BinThere.views import HomeView, RegisterProfileView, ProfileView, ListProfilesView, BinCreateView, BinUpdateView, BinListView, BinMapView, VoteView,DeleteBinView



urlpatterns = [
    #Updated path that point to the new about class-based views.
    path('', HomeView.as_view(), name='home'),
    path('BinMap/', BinMapView.as_view(), name='bin_map'),
    path('add/', BinCreateView.as_view(), name='add_bin'),
    path('edit/<int:pk>/', BinUpdateView.as_view(), name='edit_bin'),
    path('bin/<int:pk>/delete/', DeleteBinView.as_view(), name='delete_bin'),
    path('BinMap/vote/<int:bin_id>/<int:vote_type>/', VoteView.as_view(), name='vote_bin'),
    path('BinMap/BinList', BinListView.as_view(), name='bin_list'),
    path('accounts/register/', RegisterProfileView.as_view(), name='register'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),

    path('profiles/', ListProfilesView.as_view(), name='list_profiles'),

    

]

