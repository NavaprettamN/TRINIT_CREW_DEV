from django.http import HttpResponse
from django.shortcuts import render
from supabase_py import create_client

supabase_url="https://zhibxigvnqmanyzxvqql.supabase.co"
supabase_api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpoaWJ4aWd2bnFtYW55enh2cXFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDk5MjY4MDAsImV4cCI6MjAyNTUwMjgwMH0.8nqiWpWSoBNqALzrGL0k8mhL9kLWZyoTav5kRhEZVYs"

supabase = create_client(supabase_url, supabase_api_key)

def index(request):
    print(supabase)
    return render(request, "index.html", {'auth': 1})

def signup(request):
    return render(request, "signup.html")

def signin(request):
    return render(request, "signin.html")