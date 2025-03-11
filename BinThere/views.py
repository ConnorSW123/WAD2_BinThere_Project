from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime;
from django.views import View
from .models import Location, Bin, Vote
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from BinThere.forms import UserProfileForm, BinForm
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from BinThere.models import UserProfile
from django.utils import timezone
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView




# Create your views here.

class HomeView(View):
    def get(self, request): 
        context_dict = {}

        visitor_cookie_handler(request) 
        context_dict['visits'] = request.session['visits']

        return render(request,'BinThere/home.html', context_dict)
     
    
# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')


     # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = str(datetime.now())

    # Update/set the visits cookie
    request.session['visits'] = visits




class BinMapView(TemplateView):
    template_name = 'BinThere/map.html'

    def get_context_data(self, **kwargs):
        # Get the context data from the parent class
        context = super().get_context_data(**kwargs)
        
        # Query all bins
        bins = Bin.objects.all()
        
        # Format bin data to include relevant details (location, type, upvotes, downvotes)
        bin_data = [
            {'latitude': float(bin.location.latitude),  # Ensure it is a float for JavaScript
             'longitude': float(bin.location.longitude),  # Ensure it is a float for JavaScript
             'name': bin.bin_type.name,
             'location_name': bin.location.name,
             'upvotes': bin.upvotes,
             'downvotes': bin.downvotes}
            for bin in bins
        ]
        
        # Serialize the bin data into JSON format to pass it to the template
        bin_data_json = json.dumps(bin_data)
        
        # Add the bin data to the context
        context['bin_data'] = bin_data_json
        
        return context




@csrf_exempt
@login_required
def vote(request, bin_id, vote_type):
    bin_instance = get_object_or_404(Bin, id=bin_id)
    user = request.user

    # Ensure that the vote_type is valid
    if vote_type not in [1, -1]:
        return JsonResponse({'error': 'Invalid vote type'}, status=400)

    # Check if the user has already voted on this bin
    existing_vote = Vote.objects.filter(bin=bin_instance, user=user).first()

    if existing_vote:
        # If the user has voted, update the vote
        if existing_vote.vote == vote_type:
            # If the user tries to vote the same way again, remove the vote
            existing_vote.delete()
            if vote_type == 1:
                bin_instance.upvotes -= 1
            else:
                bin_instance.downvotes -= 1
        else:
            # Update the vote to the new type
            existing_vote.vote = vote_type
            existing_vote.save()

            if vote_type == 1:
                bin_instance.upvotes += 1
                bin_instance.downvotes -= 1
            else:
                bin_instance.downvotes += 1
                bin_instance.upvotes -= 1
    else:
        # If the user has not voted yet, create a new vote
        Vote.objects.create(bin=bin_instance, user=user, vote=vote_type)

        if vote_type == 1:
            bin_instance.upvotes += 1
        else:
            bin_instance.downvotes += 1

    bin_instance.save()

    # Return the updated vote counts
    return JsonResponse({'upvotes': bin_instance.upvotes, 'downvotes': bin_instance.downvotes})




class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserProfileForm()
        context_dict = {'form': form}
        return render(request, 'BinThere/profile_registration.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user  # Associate with the logged-in user
            user_profile.save()

            return redirect(reverse('BinThere:home'))  # Redirect to the home page

        else:
            print(form.errors)  # Print form validation errors to the console for debugging

        context_dict = {'form': form}
        return render(request, 'BinThere/profile_registration.html', context_dict)


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserProfile.objects.get_or_create(user=user)[0] 
        form = UserProfileForm(instance=user_profile)
        
        return (user, user_profile, form) 

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('BinThere:home'))

        context_dict = {'user_profile': user_profile,
                        'selected_user': user, 
                        'form': form}

        return render(request, 'BinThere/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('BinThere:home'))

        # Populate form with new data
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid(): 
            form.save(commit=True)
            return redirect(reverse('BinThere:profile', kwargs={'username': user.username}))  # Redirect to updated profile
        else:
            print(form.errors)  # Debugging output

        context_dict = {'user_profile': user_profile,
                        'selected_user': user, 
                        'form': form}

        return render(request, 'BinThere/profile.html', context_dict)




class ListProfilesView(View): 
    @method_decorator(login_required) 
    def get(self, request):
        profiles = UserProfile.objects.all()

        return render(request,
        'BinThere/list_profiles.html',
        {'user_profile_list': profiles})
    

@method_decorator(login_required, name='dispatch')  # Ensures the user is logged in before accessing the view
class AddBinView(CreateView):
    model = Bin
    form_class = BinForm
    template_name = 'BinThere/addbin.html'

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        # Get the logged-in user
        user = self.request.user
        bin_instance = form.save(commit=False)
        bin_instance.added_by = user  # Set the user who added the bin

        # Check if a new location is being created
        location = form.cleaned_data['location']
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        location_name = form.cleaned_data['location_name']

        if not location:  # If no location is selected, create a new location
            if latitude and longitude and location_name:
                # Create a new Location
                location = Location.objects.create(
                    name=location_name,
                    latitude=latitude,
                    longitude=longitude
                )
            else:
                # If the location is not provided correctly, we can't create the bin
                form.add_error('location', 'You must either select an existing location or provide a name, latitude, and longitude to create a new location.')
                return self.form_invalid(form)

        bin_instance.location = location  # Associate the bin with the location
        bin_instance.save()  # Save the bin instance
        return redirect(reverse_lazy('BinThere:bin_map'))  # Redirect to the bin map after adding the bin

    def form_invalid(self, form):
        # You can log the form errors here if needed
        print(form.errors)
        return self.render_to_response({'form': form})



class BinListView(ListView):
    model = Bin
    template_name = 'BinThere/bin_list.html'
    context_object_name = 'bins'  # The context variable that will be passed to the template
    paginate_by = 10  # Optional: Paginate the bins (if you want to display them in pages)
    
    def get_queryset(self):
        # Ensure consistent ordering for pagination
        return Bin.objects.all().order_by('created_at') 
