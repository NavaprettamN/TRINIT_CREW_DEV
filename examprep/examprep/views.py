from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from supabase_py import create_client
from django.views.decorators.csrf import csrf_protect
from io import BytesIO

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
            return render(request, "analytics.html", {"username": email})
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
            return render(request, 'analytics.html', {'isAuth' : isAuth, 'username': email})
    isAuth = False
    return render(request, "signin.html")


def dashboard(request):
    if request.POST != {}:
        email = request.POST['email']
        password = request.POST['password']
        response = supabase.auth.sign_up(email=email, password=password)
        print(response)
        isAuth = True
        return render(request, 'analytics.html', {'isAuth' : isAuth})
    isAuth = False
    return render(request, 'analytics.html', {'isAuth': isAuth})

def upload(request):
    
    return render(request, "upload.html")

def analytics(request):

    return render(request, "analytics.html")

def logout(request):
    return render(request, 'index.html')

def manual(request):
    return render(request,  "manual.html")

def taketest(request):
    resp = supabase.table("manual").select("*").execute()
    ques, a, b, c, d, correct=[],[],[],[],[],[]
    for i in resp['data']:
        ques.append(i['question'])
        a.append(i['a'])
        b.append(i['b'])
        c.append(i['c'])
        d.append(i['d'])
        correct.append(i['correct'])
    return render(request, "taketest.html", {"ques": ques, "a": a, "b": b, "c": c, "d": d, "correct": correct}) 

def uploadmanual(request):
    if request.POST != {}:
        question = request.POST["question"]
        option1 = request.POST["option1"]
        option2 = request.POST["option2"]
        option3 = request.POST["option3"]
        option4 = request.POST["option4"]
        correct = request.POST["correctOption"]
        resp = supabase.table("manual").insert({"question": question, "a": option1, "b": option2, "c": option3, "d": option4, "correct": correct, "testid": 1}).execute()
        print(resp)
        return render(request, "manual.html") 

def uploaddata(request):
    if request.method == 'POST' and request.FILES:
        try:
            question_paper = request.FILES['questionPaper']
            answer_key = request.FILES['answerKey']
            exam_duration = request.POST['examDuration']
            schedule_exam = request.POST['scheduleExam']

            storage = supabase.storage

            question_paper_buffer = BytesIO(question_paper.read())
            question_paper_buffer.seek(0)  # Reset pointer for upload

            answer_key_buffer = BytesIO(answer_key.read())
            answer_key_buffer.seek(0)  # Reset pointer for upload

            # Construct file names with timestamps (optional)
            # timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            # question_paper_name = f'{timestamp}_question_paper.{question_paper.name.split(".")[-1]}'
            # answer_key_name = f'{timestamp}_answer_key.{answer_key.name.split(".")[-1]}'

            # Upload files to Supabase storage (replace with your bucket name)
            question_upload_response = supabase.storage.from_('ques').upload('question_paper.pdf', question_paper_buffer, question_paper.content_type).execute()

            answer_upload_response = supabase.storage.from_('ans').upload('answer_key.pdf', answer_key_buffer, answer_key.content_type).execute()

            # Handle upload errors
            if question_upload_response.error or answer_upload_response.error:
                error_message = question_upload_response.error or answer_upload_response.error
                return render(request, "upload.html", {'error': error_message})

            # Extract uploaded file URLs (optional)
            # question_paper_url = question_upload_response.data['publicUrl']
            # answer_key_url = answer_upload_response.data['publicUrl']

            # Save metadata to database (consider using a Django model)
            # exam_data = ExamData.objects.create(
            #     question_paper=question_paper_url,
            #     answer_key=answer_key_url,
            #     exam_duration=exam_duration,
            #     schedule_exam=schedule_exam
            # )

            # Success message or redirect (optional)
            return render(request, "upload.html", {'success': 'Files uploaded successfully!'})

        except Exception as e:
            return render(request, "upload.html", {'error': f'An error occurred: {str(e)}'})

    return render(request, "upload.html")
