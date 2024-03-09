from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from supabase_py import create_client
from django.views.decorators.csrf import csrf_protect

supabase_url="https://zhibxigvnqmanyzxvqql.supabase.co"
supabase_api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpoaWJ4aWd2bnFtYW55enh2cXFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDk5MjY4MDAsImV4cCI6MjAyNTUwMjgwMH0.8nqiWpWSoBNqALzrGL0k8mhL9kLWZyoTav5kRhEZVYs"

supabase = create_client(supabase_url, supabase_api_key)

global isAuth
isAuth = False

def index(request):
    return render(request, "index.html")

def signup(request):
    # this is where we verify email -> automatic
    return render(request, "signup.html")
@csrf_protect
def signin(request):
    print("check 1")
    csrfContext = RequestContext(request)
    if request.POST != {}:
        email = request.POST['email']
        password = request.POST.get('password', False)
        try:
            response = supabase.auth.sign_in(email=email, password=password)
            print(response)
            isAuth = True
            return render(request, 'dashboard.html', {'isAuth' : isAuth})
        except:
            print("failed")
            isAuth = False
            return render(request, "signin.html")
    isAuth = False
    return render(request, "signin.html")


def dashboard(request):
    if request.POST != {}:
        email = request.POST['email']
        password = request.POST['password']
        response = supabase.auth.sign_up(email=email, password=password)
        print(response)
        isAuth = True
        return render(request, 'dashboard.html', {'isAuth' : isAuth})
    isAuth = False
    return render(request, 'dashboard.html', {'isAuth': isAuth})