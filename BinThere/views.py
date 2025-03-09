from django.shortcuts import render
from datetime import datetime;
from django.views import View
from django.shortcuts import render
from .models import Location
from .models import Bin, Vote
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.


def about(request):
    # prints out whether the method is a GET or a POST 
    print(request.method) 
    # prints out the user name, if no one is logged in it prints `AnonymousUser` 
    print(request.user) 
    visitor_cookie_handler(request)
    visits = request.session.get('visits', 1)

    return render(request, 'BinThere/about.html',{'visits': visits})

class AboutView(View):
    def get(self, request): 
        context_dict = {}

        visitor_cookie_handler(request) 
        context_dict['visits'] = request.session['visits']

        return render(request,
                      'BinThere/about.html', 
                      context_dict)
    
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



def map(request):
    # Query all bins
    bins = Bin.objects.all()
    print(bins)
    
    # Format bin data to include relevant details (location, type, upvotes, downvotes)
    bin_data = [
            {'latitude': float(bin.location.latitude),  # Ensure it is a float for JavaScript
            'longitude': float(bin.location.longitude),  # Ensure it is a float for JavaScript
            'name': bin.bin_type.name,
            'location_name': bin.location.name,
            'upvotes': bin.upvotes,
            'downvotes': bin.downvotes,}
            for bin in bins
        ]
    
    # Serialize the bin data into JSON format to pass it to the template
    bin_data_json = json.dumps(bin_data)
    
    return render(request, 'BinThere/map.html', {'bin_data': bin_data_json})



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
