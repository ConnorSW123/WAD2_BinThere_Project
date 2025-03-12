from django.shortcuts import render, redirect
from datetime import datetime;
from django.views import View
from .models import Location, Bin
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from BinThere.forms import UserProfileForm, BinForm, UserForm
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from BinThere.models import UserProfile, BinType
from django.utils import timezone
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView, FormView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login
from geopy.distance import geodesic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404


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
        context = super().get_context_data(**kwargs)

        # Query all bins and bin types
        bins = Bin.objects.all()
        bin_types = BinType.objects.all()

        # Serialize the bin data into JSON format to pass it to the template
        bin_data = [
            {
                'id': bin.id,
                'latitude': float(bin.location.latitude),
                'longitude': float(bin.location.longitude),
                'bin_types': [bin_type.name for bin_type in bin.bin_types.all()],
                'location_name': bin.location.name,
                'upvotes': bin.upvotes,
                'downvotes': bin.downvotes
            }
            for bin in bins
        ]

        # Convert bin types to a list of dictionaries for safe JSON passing
        bin_types_data = [{'id': bin_type.id, 'name': bin_type.name} for bin_type in bin_types]

        context['bin_data'] = json.dumps(bin_data)
        context['bin_types'] = json.dumps(bin_types_data)  # Passing bin types as JSON

        return context

class VoteView(View):
    def post(self, request, bin_id, vote_type):
        try:
            bin = Bin.objects.get(id=bin_id)
        except Bin.DoesNotExist:
            return JsonResponse({'error': 'Bin not found'}, status=404)

        # Handle upvotes and downvotes based on vote_type (1 for upvote, -1 for downvote)
        if vote_type == 1:
            bin.upvotes += 1
        elif vote_type == -1:
            bin.downvotes += 1
        else:
            return JsonResponse({'error': 'Invalid vote type'}, status=400)

        bin.save()  # Save the updated bin with the new vote count
        return JsonResponse({'upvotes': bin.upvotes, 'downvotes': bin.downvotes})

class RegisterProfileView(View):
    def get(self, request):
        # Create form instances for user and user profile
        user_form = UserForm()
        profile_form = UserProfileForm()

        # Pass forms to the context for rendering
        context_dict = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'BinThere/profile_registration.html', context_dict)

    def post(self, request):
        # Create form instances with POST data
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # First save the user (which creates the username, email, etc.)
            user = user_form.save(commit=False)

            # Ensure username is set if it's empty (using get_or_create for user)
            if not user.username:
                # Try to get or create a user with the provided username
                user, created = User.objects.get_or_create(
                    username=user.email.split('@')[0],  # Automatically generate username from email
                    defaults={'email': user.email}  # If the username doesn't exist, set email
                )
            
            # Save the user
            user.save()

            # Now save the user profile
            user_profile = profile_form.save(commit=False)
            user_profile.user = user  # Attach the user to the profile
            user_profile.save()

            # Log in the user
            login(request, user)

            # Redirect to the profile page after successful registration
            return redirect(reverse('BinThere:profile', kwargs={'username': user.username}))

        # If the form is not valid, print errors and return to the registration page
        else:
            print(user_form.errors)
            print(profile_form.errors)

        # If forms are invalid, render the page with forms and errors
        context_dict = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'BinThere/profile_registration.html', context_dict)



class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile, created = UserProfile.objects.get_or_create(user=user)
        form = UserProfileForm(instance=user_profile)

        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect('BinThere:home')

        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form}
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
    

@method_decorator(login_required, name='dispatch')
class BinCreateView(CreateView):
    model = Bin
    form_class = BinForm
    template_name = 'BinThere/add_bin.html'
    success_url = reverse_lazy('BinThere:bin_map')

    def form_valid(self, form):
        # Debugging: Check if the user is logged in
        if not self.request.user.is_authenticated:
            messages.error(self.request, "You need to be logged in to create a bin.")
            return redirect('login')  # Or any other redirect URL for login
        
        print(self.request.user.username)  # Debug: Check the user object
        
        # Check if an existing bin is selected
        existing_bin = form.cleaned_data.get('existing_bin')
        if existing_bin:
            messages.error(self.request, "You selected an existing bin. Please use the update feature instead.")
            return redirect('BinThere:bin_map')

        # Check if location data is provided for new bin creation
        location_name = form.cleaned_data['location_name']
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']

        if not location_name or latitude is None or longitude is None:
            messages.error(self.request, "You must provide location details (name, latitude, longitude) to create a new bin.")
            return redirect('BinThere:add_bin')  # Redirect back to form with error message

        # Create or get location (we should be creating a new location or using an existing one)
        location, created = Location.objects.get_or_create(
            name=location_name,
            defaults={'latitude': latitude, 'longitude': longitude}
        )

        # Create the Bin instance (but don't save it yet)
        bin_instance = form.save(commit=False)

        # Assign the location to the bin
        bin_instance.location = location

        # Assign the selected user (added_by) from the form
        bin_instance.added_by = self.request.user  # Get the selected user - Should work now

        # Set default upvotes and downvotes to 0
        bin_instance.upvotes = 0
        bin_instance.downvotes = 0

        # Save the bin instance
        bin_instance.save()

        # Assign the selected bin types to the bin instance
        bin_types = form.cleaned_data['bin_types']
        bin_instance.bin_types.set(bin_types)  # Many-to-many relationship
        bin_instance.save()  # Save changes after assigning bin types

        messages.success(self.request, "New bin created successfully.")
        return redirect('BinThere:bin_map')  # Redirect to map after successful creation






@method_decorator(login_required, name='dispatch')
class BinUpdateView(UpdateView):
    model = Bin
    form_class = BinForm
    template_name = 'BinThere/add_bin.html'
    success_url = reverse_lazy('BinThere:bin_list')

    def form_valid(self, form):
        existing_bin = form.cleaned_data.get('existing_bin')
        if not existing_bin:
            messages.error(self.request, "No existing bin was selected for an update.")
            return redirect('BinThere:bin_map')

        # Add selected bin types to the existing bin
        existing_bin.bin_types.add(*form.cleaned_data['bin_types'])
        existing_bin.save()

        messages.success(self.request, "Bin updated successfully.")
        return redirect('BinThere:bin_map')


class BinListView(ListView):
    model = Bin
    template_name = 'BinThere/bin_list.html'
    context_object_name = 'bins'
    paginate_by = 10  

    def get_queryset(self):
        queryset = Bin.objects.all()
        search_query = self.request.GET.get('search', None)
        location_query = self.request.GET.get('location', None)
        user_lat = self.request.GET.get('latitude', None)
        user_lon = self.request.GET.get('longitude', None)

        # Filter by bin type
        if search_query:
            queryset = queryset.filter(bin_types__name__icontains=search_query)

        # Filter by location name
        if location_query:
            queryset = queryset.filter(location__name__icontains=location_query)

        # Filter by geolocation (5km radius)
        if user_lat and user_lon:
            try:
                user_location = (float(user_lat), float(user_lon))
                nearby_bins = []

                for bin in queryset:
                    bin_location = (float(bin.location.latitude), float(bin.location.longitude))
                    distance = geodesic(user_location, bin_location).km
                    if distance <= 5:
                        nearby_bins.append(bin)

                queryset = nearby_bins  
            except ValueError:
                pass  

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bin_types'] = BinType.objects.all()
        return context








class AddBinTypeView(FormView):
    template_name = 'BinThere/add_bin_type.html'
    form_class = BinForm
    success_url = '/BinThere/BinMap/'  # Redirect to the map page after successful form submission

    def form_valid(self, form):
        # Save the bin form (either create new or update existing bin)
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Handle invalid form submission
        return self.render_to_response(self.get_context_data(form=form))
    


class DeleteBinView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bin
    context_object_name = 'bin'
    success_url = reverse_lazy('BinThere:bin_list')

    def test_func(self):
        """
        Ensure only bin owners or superusers can delete bins.
        """
        bin_instance = self.get_object()
        return self.request.user == bin_instance.added_by or self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Show a 404 error instead of redirecting for unauthorized access.
        """
        raise Http404("You do not have permission to delete this bin.")

    def delete(self, request, *args, **kwargs):
        """
        Add a success message before redirecting after deletion.
        """
        messages.success(self.request, "Bin deleted successfully!")
        return super().delete(request, *args, **kwargs)

    