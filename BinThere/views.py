from django.shortcuts import render
from datetime import datetime;
from django.views import View

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

