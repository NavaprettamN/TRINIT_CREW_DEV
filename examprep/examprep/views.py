from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from supabase_py import create_client
from django.views.decorators.csrf import csrf_protect

supabase_url="https://avkjleinmjywxmspfkck.supabase.co"
supabase_api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF2a2psZWlubWp5d3htc3Bma2NrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDk5NzIxMDEsImV4cCI6MjAyNTU0ODEwMX0.YiCobkolgIfyGGWSf37K_ECI40KtzwkzA4Kgt9GGACU"

supabase = create_client(supabase_url, supabase_api_key)

global isAuth
isAuth = False

def index(request):
    return render(request, "index.html")

def signup(request):
    if request.POST != {}:
        username=[]
        data = supabase.table('user').select('username').execute()
        for i in data['data']:
            username.append(i['username'])
        email = request.POST['email']
        password = request.POST['password']
        if email not in username:
            print(1)
            data, count = supabase.table('user').insert({"username": email, "password": password}).execute()
            email, password='',''
        # this is where we verify email -> automatic
            return render(request, "dashboard.html", {"username": email})
        else: return render(request, "signup.html", {"userexists": 1})
    return render(request, "signup.html", {"userexists": 0})
@csrf_protect
def signin(request):
    # print("check 1")
    csrfContext = RequestContext(request)
    if request.POST != {}:
        username, passwordarr=[],[]
        data = supabase.table('user').select('username, password').execute()
        for i in data["data"]:
            username.append(i["username"])
            passwordarr.append(i["password"])
        email = request.POST['email']
        password = request.POST['password']
        if (email not in username and  password in passwordarr) or (email in username and password not in passwordarr):
            isAuth=False
            return render(request, "signin.html", {"error": "Email or Password Error"})
        if email in username and username.index(email)==passwordarr.index(password):
            isAuth = True
            return render(request, 'dashboard.html', {'isAuth' : isAuth})
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