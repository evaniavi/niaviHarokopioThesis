from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import  messages
from django import forms
from personal.forms import *
from personal.models import *
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime,date
import io
import os
from django.http import FileResponse
from platform import python_version
from pyreportjasper import PyReportJasper
from django.http import HttpResponse
from pyreportjasper.config import Config
from pyreportjasper.report import Report
from decimal import Decimal
from django.db.models import Q
from decouple import config
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from personal.tokens import account_activation_token
from django.template import RequestContext
from .decorators import unauthenticated_user,student_required,professor_required
from .filters import ApplicationFilter
from django.http import Http404


update_basic_info = False


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is already used or is invalid!")

    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.', extra_tags='safe')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def HomePage(request):
        print(request.headers)
        return render(request, "home.html", {})



def informatics_page_view(request):
        print(request.headers)
        return render(request, "informatics.html", {})

@unauthenticated_user
def login_page_view(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                if user.groups.filter(name__contains='secretary').exists():
                    return redirect(reverse('admin:index'))
                else:
                    return render(request, "home.html")
                
            else:
                messages.error(request, 'Username OR Password is Incorrect!Please try again')
        return render(request, "registration/login.html", {})

#end token authentication
def signup_page_view(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        profile = ProfileForm(request.POST,request.FILES)
        if user_form.is_valid() and profile.is_valid():
            user = user_form.save(commit=False)
            user.is_active=False
            user.department = None
            user.title = 'Φοιτητής'
            user.save()
            activateEmail(request, user, user_form.cleaned_data.get('email'))
            p = profile.save(commit=False)
            p.user = user
            if 'profile_pic' in request.FILES:
                p.profile_pic = request.FILES['profile_pic']
            p.save()
            return render(request, "home.html")
        else:
            print(user_form.errors,profile.errors)
    else:
        user_form = CreateUserForm()
        profile = ProfileForm()
    context={'form':user_form, 'profile_form':profile}
    return render(request, "signup.html", context)



def create_application_pdf(request,pk):
    student = request.user.id
    # REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')
    REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')
    # input_file = os.path.join(REPORTS_DIR, 'aplication.jrxml')
    # output_file = os.path.join(REPORTS_DIR, 'compile_to_file')
  
    configuration = Config()
    configuration.input = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports', 'aplication.jrxml')
    configuration.output = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports', 'compile_to_file')
    configuration.params = {'IMAGE_DIR': os.path.join(os.path.abspath(os.getcwd()), 'static/images/'),'APPLICATION_ID' : Decimal(pk), 'USER_ID' :student}
    configuration.dbType = config('dbType')
    configuration.dbHost = config('dbHost')
    configuration.dbName = config('dbName')
    configuration.dbPasswd = config('dbPasswd')
    configuration.dbPort = config('dbPort')
    configuration.dbUser = config('dbUser')
    configuration.dbDriver = config('dbDriver')


    instance = Report(configuration, configuration.input)
    instance.fill()
    instance.export_pdf()
    with open(os.path.join(REPORTS_DIR, 'compile_to_file.pdf'), 'rb') as f:
           file_data = f.read()
    response = HttpResponse(file_data,content_type='aplication/pdf')
    response['Content-Disposition'] = 'attachment; filename="application.pdf"'

    return response




@login_required
@student_required
def profile_page_view(request):

    prof = request.user.profile
    form = CreateUserForm(instance=request.user)
    profile = ProfileForm(instance=prof)
    if request.method == 'POST':
        profile = ProfileForm(request.POST,instance=prof)
        form = ProfileForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid()and profile.is_valid():
            user = form.save()
            p = profile.save(commit=False)
            p.user = user
            if 'profile_pic' in request.FILES:
                p.profile_pic = request.FILES['profile_pic']
            p.save()
            return render(request, "home.html")

    context={'form':form, 'profile_form':profile}
    return render(request, "profile.html", context)



def add_education_info_view(request):
    form = EducationInfo_form()
    if request.method == 'POST':
        form = EducationInfo_form(request.POST,request.FILES)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.user = request.user
            edu.save()
            return redirect('student_dashboard')
    else:
            form = EducationInfo_form()
    context={'form':form}
    return render(request, "add_education.html", context)


@login_required
def student_education_dashboard(request):
    update_basic_info = False
    student = request.user  
    try:
        basic_info = BasicUserInfo.objects.get(user_id=student)      
    except BasicUserInfo.DoesNotExist:
        basic_info = None
    basic_info_form = BasicInfo_form(instance=basic_info)
    if basic_info is not None :
        name_ = getattr(basic_info, 'name')
        surname_ = getattr(basic_info, 'surname')
        fatherName_ = getattr(basic_info, 'fatherName')
        motherName_ = getattr(basic_info, 'motherName')
        afm_ = getattr(basic_info, 'afm')
        birth_date_ = getattr(basic_info, 'birth_date')
    else:
        name_ = ""
        surname_ =""
        fatherName_ = ""
        motherName_ = ""
        afm_ = ""
        birth_date_ = ""
    basic_info = BasicUserInfo.objects.filter(user_id=student)
    student_educations = EducationInfo.objects.filter(user_id=student).order_by('-id')
    work_experience = JobInfo.objects.filter(user_id=student).order_by('-id')
    recommendations = Recommendation.objects.filter(user_id=student).order_by('-id')
    languages = ForeignLanguages.objects.filter(user_id=student).order_by('-id')

    context = {
        'student_educations':student_educations,
        'user_basic_info':basic_info_form,
        'work_experience':work_experience,
        'recommendations' :recommendations,
        'languages' :languages,
        'name': name_ ,
        'surname':surname_ , 
        'fatherName':fatherName_ ,
        'motherName':motherName_ ,
        'afm':afm_ ,
        'birth_date':birth_date_     
    }

    return render(request, "education_dashboard.html", context)

@login_required
def student_dashboard(request,pk):
    #pk = application id
    edit = False
    update_basic_info = False
    student = request.user
    application = Application.objects.get(id=pk)
    progr = PostgraduatePrograms.objects.get(id=application.program_id)
    directions = ProgramDirections.objects.filter(program_id=progr.id).order_by('-id')
    try:
        basic_info = BasicUserInfo.objects.get(user_id=student,application_id = application.id)      
    except BasicUserInfo.DoesNotExist:
        basic_info = None
    basic_info_form = BasicInfo_form(instance=basic_info)
    if basic_info is not None :
        name_ = getattr(basic_info, 'name')
        surname_ = getattr(basic_info, 'surname')
        fatherName_ = getattr(basic_info, 'fatherName')
        motherName_ = getattr(basic_info, 'motherName')
        afm_ = getattr(basic_info, 'afm')
        birth_date_ = getattr(basic_info, 'birth_date')
    else:
        name_ = ""
        surname_ =""
        fatherName_ = ""
        motherName_ = ""
        afm_ = ""
        birth_date_ = ""

    try:
        add_info = AdditionalInfo.objects.get(application_id=pk)      
    except AdditionalInfo.DoesNotExist:
        add_info = None
    add_info_form = AdditionalInfo_form(instance=add_info)
    if add_info is not None :
        reason_of_selection_ = getattr(add_info, 'reason_of_selection')
        other_applications_ = getattr(add_info, 'other_applications')
        studies_type_ = getattr(add_info, 'studies_type')
        first_choice_ = getattr(add_info, 'first_choice')
        second_choice_ = getattr(add_info, 'second_choice')
        third_choice_ = getattr(add_info, 'third_choice')
    else:
        reason_of_selection_ = ""
        other_applications_ =""
        studies_type_ = ""
        first_choice_ = ""
        second_choice_ = ""
        third_choice_= ""
    
    application = Application.objects.get(user_id=student,program_id=progr.id)
    print('application id ---->',application.id)
    basic_info = BasicUserInfo.objects.filter(user_id=student)
    student_educations = EducationInfo.objects.filter(user_id=student,application_id=application).order_by('-id')
    work_experience = JobInfo.objects.filter(user_id=student,application_id=application).order_by('-id')
    recommendations = Recommendation.objects.filter(user_id=student,application_id=application).order_by('-id')
    languages = ForeignLanguages.objects.filter(user_id=student,application_id=application).order_by('-id')
    if progr.start_date <= date.today() <= progr.end_date and application.status == 'Υπό Επεξεργασία':
        print('applications are open with id ---->',application.id)
        edit = True
    context = {
        'student_educations':student_educations,
        'user_basic_info':basic_info_form,
        'work_experience':work_experience,
        'recommendations' :recommendations,
        'languages' :languages,
        'name': name_ ,
        'surname':surname_ , 
        'fatherName':fatherName_ ,
        'motherName':motherName_ ,
        'afm':afm_ ,
        'birth_date':birth_date_,
        'edit' :edit,
        'application_id' :application.id,
        'reason_of_selection' :reason_of_selection_ ,
        'other_applications' : other_applications_ ,
        'studies_type' : studies_type_ ,
        'directions' : directions,
        'first_choice' : first_choice_,
        'second_choice' :second_choice_,
        'third_choice':third_choice_
    }

    return render(request, "education_dashboard.html", context)

@login_required
def edit_basic_info(request,pk):
    student = request.user.id
    try:
        print('hello')
        print(student)
        user_basic_info = BasicUserInfo.objects.get(application_id=pk)
    except BasicUserInfo.DoesNotExist:
        user_basic_info = None
        print('in except')
    form = BasicInfo_form(instance=user_basic_info)

    if request.method == 'POST':
        form = BasicInfo_form(request.POST,instance=user_basic_info)
        if form.is_valid():
            bform = form.save(commit=False)
            bform.user = request.user
            bform.application_id = pk 
            bform.save()
            return redirect('student_dashboard',pk=pk)
    else:
        form = BasicInfo_form(instance=user_basic_info)
    context = {'form':form}

    return render(request, "basic_info_details.html", context)


@login_required
def edit_additional_info(request,pk):
    student = request.user.id
    application = Application.objects.get(id=pk)
    progr = PostgraduatePrograms.objects.get(id=application.program_id)
    directions = ProgramDirections.objects.filter(program_id=progr.id).order_by('-id')
    order=1
    available_directions=[]
    for dir in directions:
        setattr(dir, 'order', order)
        order += 1
        available_directions.append({
        'name':dir.name,
        'id': dir.id,
    })
    try:
        user_additional_info = AdditionalInfo.objects.get(application_id=pk)
    except AdditionalInfo.DoesNotExist:
        user_additional_info = None
        print('in except')
    form = AdditionalInfo_form(instance=user_additional_info)
    form.fields['first_choice'].choices = [(dir.name, dir.name) for dir in directions]
    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect('student_dashboard',pk=pk)
        else:
            form = AdditionalInfo_form(request.POST,instance=user_additional_info)
            directions_chosen = request.POST.get('myTable')
            if form.is_valid():
                bform = form.save(commit=False)
                bform.application_id = pk 
                bform.user = request.user
                bform.save()
                return redirect('student_dashboard',pk=pk)
    else:
        form = AdditionalInfo_form(instance=user_additional_info)
        choices = [("", "")]
        for dir in directions:
            choices.append((dir.name, dir.name))
       
        form.fields['first_choice'] = forms.ChoiceField(choices=choices,
                                     widget=forms.Select(attrs={'class': 'form-control', 
                             'required':'True', 
                             'name':'first_choice',
                             'label':'Πρώτη Επιλογή',  
                             'id':'first_choice', }))
        form.fields['second_choice'] = forms.ChoiceField(choices=choices,required=False,
                                     widget=forms.Select(attrs={'class': 'form-control', 

                             'name':'first_choice', 
                             'label':'Δεύτερη Επιλογή',  
                             'id':'first_choice', }))
        form.fields['third_choice'] = forms.ChoiceField(choices=choices,required=False,
                                     widget=forms.Select(attrs={'class': 'form-control', 
   
                             'name':'first_choice', 
                             'label':'Τρίτη Επιλογή',  
                             'id':'first_choice', }))
        form.initial['first_choice'] = choices[0]
        form.initial['second_choice'] = choices[0]
        form.initial['third_choice'] = choices[0]
    context = {'form':form,'application_id' : pk,'directions' : directions}

    return render(request, "additional_info_details.html", context)

@login_required
def education_info_details(request,pk):
    student = request.user.id
    education_info_details = EducationInfo.objects.get(id=pk)

    form = EducationInfo_form(instance=education_info_details)

    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect('student_dashboard',pk=education_info_details.application_id)
        elif "delete" in request.POST:
            education_info_details.delete()
            return redirect('student_dashboard',pk=education_info_details.application_id)
        else:
            form = EducationInfo_form(request.POST,request.FILES,instance=education_info_details)
            if form.is_valid():
                bform = form.save(commit=False)
                bform.user = request.user
                bform.save()
                return redirect('student_dashboard',pk=education_info_details.application_id)
    else:
        form = EducationInfo_form(instance=education_info_details)
    context = {'form':form,
    'application_id' : education_info_details.application_id}

    return render(request, "education_info_details.html", context)


@login_required
def create_new_degree(request,pk):
    #pk = application id
    edit = True
    form = EducationInfo_form()
    #to get data back from the form
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('student_dashboard',pk=pk)
        else:
            form = EducationInfo_form(request.POST)
            if form.is_valid():
                education_form = form.save(commit=False)
                education_form.user = request.user
                education_form.application_id = pk  # This is needed for the new implementation
                education_form.save()
                return redirect('student_dashboard',pk=pk)
    
    context = {
        'form': form,
        'edit' : edit,
        'application_id' : pk
    }
    return render(request, 'add_education.html', context)


@login_required
def create_new_work_experience(request,pk):

    form = WorkExperienceInfo_form()
    #to get data back from the form
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('student_dashboard',pk=pk)
        else:
            form = WorkExperienceInfo_form(request.POST)
            if form.is_valid():
                education_form = form.save(commit=False)
                education_form.user = request.user
                education_form.application_id = pk  # This is needed for the new implementation
                education_form.save()
                return redirect('student_dashboard',pk=pk)

    context = {
        'form': form,
        'application_id' : pk
    }
    return render(request, 'add_work_experience.html', context)

@login_required
def job_info_details(request,pk):
    student = request.user.id
    job_info_details = JobInfo.objects.get(id=pk)

    form = WorkExperienceInfo_form(instance=job_info_details)

    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect('student_dashboard',pk=job_info_details.application_id)
        elif "delete" in request.POST:
            job_info_details.delete()
            return redirect('student_dashboard',pk=job_info_details.application_id)
        else:
            form = WorkExperienceInfo_form(request.POST,request.FILES,instance=job_info_details)
            if form.is_valid():
                bform = form.save(commit=False)
                bform.user = request.user
                bform.save()
                return redirect('student_dashboard',pk=job_info_details.application_id)
    else:
        form = WorkExperienceInfo_form(instance=job_info_details)
    context = {'form':form,
    'application_id' : job_info_details.application_id}

    return render(request, "education_info_details.html", context)

@login_required
def create_new_reccomendation(request,pk):
    form = Recommendation_form()
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('student_dashboard',pk=pk)
        else:
            form = Recommendation_form(request.POST)
            if form.is_valid():
                education_form = form.save(commit=False)
                education_form.user = request.user
                education_form.application_id = pk 
                education_form.save()
                return redirect('student_dashboard',pk=pk)

    context = {
        'form': form,
        'application_id' : pk
    }
    return render(request, 'add_reccomendation.html', context)

@login_required
def recommendation_details(request,pk):
    student = request.user.id
    recommendation_details = Recommendation.objects.get(id=pk)

    form = Recommendation_form(instance=recommendation_details)

    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect('student_dashboard',pk=recommendation_details.application_id)
        elif "delete" in request.POST:
            recommendation_details.delete()
            return redirect('student_dashboard',pk=recommendation_details.application_id)
        else:
            form = Recommendation_form(request.POST,request.FILES,instance=recommendation_details)
            if form.is_valid():
                bform = form.save(commit=False)
                bform.user = request.user
                bform.save()
                return redirect('student_dashboard',pk=recommendation_details.application_id)
    else:
        form = Recommendation_form(instance=recommendation_details)
    context = {'form':form,
    'application_id' : recommendation_details.application_id}

    return render(request, "recommendation_details.html", context)

# @login_required
# def create_new_application(request):  # dont need anymore?
#     update_basic_info = False
#     student = request.user  
#     try:
#         basic_info = BasicUserInfo.objects.get(user_id=student)      
#     except BasicUserInfo.DoesNotExist:
#         basic_info = None
#     basic_info_form = BasicInfo_form(instance=basic_info)
#     if basic_info is not None :
#         name_ = getattr(basic_info, 'name')
#         surname_ = getattr(basic_info, 'surname')
#         fatherName_ = getattr(basic_info, 'fatherName')
#         motherName_ = getattr(basic_info, 'motherName')
#         afm_ = getattr(basic_info, 'afm')
#         birth_date_ = getattr(basic_info, 'birth_date')
#     else:
#         name_ = ""
#         surname_ =""
#         fatherName_ = ""
#         motherName_ = ""
#         afm_ = ""
#         birth_date_ = ""

#     basic_info = BasicUserInfo.objects.filter(user_id=student)
#     student_educations = EducationInfo.objects.filter(user_id=student).order_by('-id')
#     work_experience = JobInfo.objects.filter(user_id=student).order_by('-id')
#     recommendations = Recommendation.objects.filter(user_id=student).order_by('-id')
#     context = {
#         'student_educations':student_educations,
#         'user_basic_info':basic_info_form,
#         'work_experience':work_experience,
#         'recommendations' :recommendations,
#         'name': name_ ,
#         'surname':surname_ , 
#         'fatherName':fatherName_ ,
#         'motherName':motherName_ ,
#         'afm':afm_ ,
#         'birth_date':birth_date_    , 

#     }

#     return render(request, "application.html", context)

@login_required
def departments(request): 

    user = request.user
    if user.groups.filter(name__contains='students').exists() :

        programs = PostgraduatePrograms.objects.select_related('department')
        for progr in programs:
            if progr.start_date <= date.today() <= progr.end_date :
                edit = True
                print('can create  ---->',edit)
                progr.create = edit
    elif user.groups.filter(name__contains='professors').exists() :
        # programs = AssignedProffessors.objects.filter(user_id=user.id).select_related('program') #kinda works its missing the department name
        programs = PostgraduatePrograms.objects.select_related('department').filter(assignedproffessors__user_id=user.id)
    context = {
        'programs':programs

    }
    return render(request, "departments.html", context)


@login_required
@csrf_exempt
def create_application_for_program(request,pk):
    isSubmitted = False
    edit = False
    student = request.user
    programs = PostgraduatePrograms.objects.select_related('department')
    progr = PostgraduatePrograms.objects.get(id=pk)
    dep = Departments.objects.get(id=progr.department_id)
    directions = ProgramDirections.objects.filter(program_id=progr.id).order_by('-id')
    order=1
    for dir in directions:
        setattr(dir, 'order', order)
        order += 1

    if (progr.start_date > date.today()) or  (date.today() > progr.end_date) :
        raise Http404
        
    try :
        application = Application.objects.get(user_id=student,program_id=progr.id,year=date.today().year)
    except Application.DoesNotExist:
        app = Application(user = request.user,program =progr)
        app.save()
    # student_education_dashboard(request.GET)
    application = Application.objects.get(user_id=student,program_id=progr.id)
    try:
        basic_info = BasicUserInfo.objects.get(application_id=application.id)      
    except BasicUserInfo.DoesNotExist:
        basic_info = None
    basic_info_form = BasicInfo_form(instance=basic_info)
    if basic_info is not None :
        name_ = getattr(basic_info, 'name')
        surname_ = getattr(basic_info, 'surname')
        fatherName_ = getattr(basic_info, 'fatherName')
        motherName_ = getattr(basic_info, 'motherName')
        afm_ = getattr(basic_info, 'afm')
        birth_date_ = getattr(basic_info, 'birth_date')
    else:
        name_ = ""
        surname_ =""
        fatherName_ = ""
        motherName_ = ""
        afm_ = ""
        birth_date_ = ""

    try:
        add_info = AdditionalInfo.objects.get(application_id=application.id)      
    except AdditionalInfo.DoesNotExist:
        add_info = None
    add_info_form = AdditionalInfo_form(instance=add_info)
    if add_info is not None :
        reason_of_selection_ = getattr(add_info, 'reason_of_selection')
        other_applications_ = getattr(add_info, 'other_applications')
        studies_type_ = getattr(add_info, 'studies_type')
        studies_type_ = getattr(add_info, 'studies_type')
        first_choice_ = getattr(add_info, 'first_choice')
        second_choice_ = getattr(add_info, 'second_choice')
        third_choice_ = getattr(add_info, 'third_choice')
    else:
        reason_of_selection_ = ""
        other_applications_ =""
        studies_type_ = ""
        first_choice_ = ""
        second_choice_ = ""
        third_choice_= ""
    if request.method == "POST":
        obj = Application.objects.get(id=application.id)
        obj.status = "Οριστικοποιημένη"
        obj.save()
    # print('application id ---->',application.id)
    application = Application.objects.get(id=application.id)
    basic_info = BasicUserInfo.objects.filter(user_id=student)
    student_educations = EducationInfo.objects.filter(user_id=student,application_id=application).order_by('-id')
    work_experience = JobInfo.objects.filter(user_id=student,application_id=application).order_by('-id')
    recommendations = Recommendation.objects.filter(user_id=student,application_id=application).order_by('-id')
    languages = ForeignLanguages.objects.filter(user_id=student,application_id=application).order_by('-id')
    add_info = AdditionalInfo.objects.filter(application_id=application.id)
    if progr.start_date <= date.today() <= progr.end_date and application.status == 'Υπό Επεξεργασία':
        print('applications are open with id ---->',application.id)
        edit = True
    if application.status != 'Υπό Επεξεργασία':
        isSubmitted = True
    context = {
        'student_educations':student_educations,
        'user_basic_info':basic_info_form,
        'work_experience':work_experience,
        'recommendations' :recommendations,
        'languages' :languages,
        'name': name_ ,
        'surname':surname_ , 
        'fatherName':fatherName_ ,
        'motherName':motherName_ ,
        'afm':afm_ ,
        'birth_date':birth_date_,
        'edit' :edit,
        'application_id' :application.id,
        'reason_of_selection' :reason_of_selection_ ,
        'other_applications' : other_applications_ ,
        'studies_type' : studies_type_ ,
        'directions' : directions,
        'isSubmitted' : isSubmitted,
        'first_choice' : first_choice_,
        'second_choice' :second_choice_,
        'third_choice':third_choice_
    }


    return render(request, "education_dashboard.html", context)

@login_required
@student_required
def create_new_language(request,pk):

    form = ForeignLanguages_form()
    #to get data back from the form
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect('student_dashboard',pk=pk)
        else:
            form = ForeignLanguages_form(request.POST)
            if form.is_valid():
                language_form = form.save(commit=False)
                language_form.user = request.user
                language_form.application_id = pk # This is needed for the new implementation connecting everything to an appication
                language_form.save()
                return redirect('student_dashboard',pk=pk)

    context = {
        'form': form,
        'application_id' : pk
    }
    return render(request, 'add_language.html', context)

@login_required
def language_details(request,pk):
    student = request.user.id
    lang_details = ForeignLanguages.objects.get(id=pk)

    form = ForeignLanguages_form(instance=lang_details)

    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect('student_dashboard',pk=lang_details.application_id)
        elif "delete" in request.POST:
            lang_details.delete()
            return redirect('student_dashboard',pk=lang_details.application_id)
        else:
            form = ForeignLanguages_form(request.POST,instance=lang_details)
            if form.is_valid():
                bform = form.save(commit=False)
                bform.user = request.user
                bform.save()
                return redirect('student_dashboard',pk=lang_details.application_id)
    else:
        form = ForeignLanguages_form(instance=lang_details)
    context = {'form':form,
              'application_id' : lang_details.application_id}

    return render(request, "language_details.html", context)

@login_required
def my_applications(request):
    update_basic_info = False
    student = request.user  
    applications = Application.objects.select_related('program').filter(Q(program__isnull=True) | Q(user_id=student))
    context = {
        'applications':applications, 
   
    }

    return render(request, "my_applications.html", context)

@login_required
@csrf_protect
def view_my_application(request,pk):
    isSubmitted = False
    edit = False
    student = request.user
    application = Application.objects.get(id=pk,user=student.id)
    progr = PostgraduatePrograms.objects.get(id=application.program_id)
    dep = Departments.objects.get(id=progr.department_id)
    directions = ProgramDirections.objects.filter(program_id=progr.id).order_by('-id')
    order=1
    for dir in directions:
        setattr(dir, 'order', order)
        order += 1

    print('program id ---->',progr.id)
    print('department id ---->',dep.id)
    try:
        basic_info = BasicUserInfo.objects.get(application_id=application.id)      
    except BasicUserInfo.DoesNotExist:
        basic_info = None
    basic_info_form = BasicInfo_form(instance=basic_info)
    if basic_info is not None :
        name_ = getattr(basic_info, 'name')
        surname_ = getattr(basic_info, 'surname')
        fatherName_ = getattr(basic_info, 'fatherName')
        motherName_ = getattr(basic_info, 'motherName')
        afm_ = getattr(basic_info, 'afm')
        birth_date_ = getattr(basic_info, 'birth_date')
    else:
        name_ = ""
        surname_ =""
        fatherName_ = ""
        motherName_ = ""
        afm_ = ""
        birth_date_ = ""

    try:
        add_info = AdditionalInfo.objects.get(application_id=application.id)      
    except AdditionalInfo.DoesNotExist:
        add_info = None
    add_info_form = AdditionalInfo_form(instance=add_info)
    if add_info is not None :
        reason_of_selection_ = getattr(add_info, 'reason_of_selection')
        other_applications_ = getattr(add_info, 'other_applications')
        studies_type_ = getattr(add_info, 'studies_type')
        first_choice_ = getattr(add_info, 'first_choice')
        second_choice_ = getattr(add_info, 'second_choice')
        third_choice_ = getattr(add_info, 'third_choice')
    else:
        reason_of_selection_ = ""
        other_applications_ =""
        studies_type_ = ""
        first_choice_ = ""
        second_choice_ = ""
        third_choice_= ""
    if request.method == "POST":
        obj = Application.objects.get(id=application.id)
        obj.status = "Οριστικοποιημένη"
        obj.save()
    print('application id ---->',application.id)
    application = Application.objects.get(id=application.id)
    basic_info = BasicUserInfo.objects.filter(application_id=application)
    student_educations = EducationInfo.objects.filter(application_id=application).order_by('-id')
    work_experience = JobInfo.objects.filter(application_id=application).order_by('-id')
    recommendations = Recommendation.objects.filter(application_id=application).order_by('-id')
    languages = ForeignLanguages.objects.filter(application_id=application).order_by('-id')
    add_info = AdditionalInfo.objects.filter(application_id=application.id)
    if progr.start_date <= date.today() <= progr.end_date and application.status == 'Υπό Επεξεργασία': # need to add the year for each application
        print('applications are open with id ---->',application.id)
        edit = True
    if application.status != 'Υπό Επεξεργασία':
        isSubmitted = True
    context = {
        'student_educations':student_educations,
        'user_basic_info':basic_info_form,
        'work_experience':work_experience,
        'recommendations' :recommendations,
        'languages' :languages,
        'name': name_ ,
        'surname':surname_ , 
        'fatherName':fatherName_ ,
        'motherName':motherName_ ,
        'afm':afm_ ,
        'birth_date':birth_date_,
        'edit' :edit,
        'application_id' :application.id,
        'reason_of_selection' :reason_of_selection_ ,
        'other_applications' : other_applications_ ,
        'studies_type' : studies_type_ ,
        'directions' : directions,
        'isSubmitted' : isSubmitted,
        'first_choice' : first_choice_,
        'second_choice' :second_choice_,
        'third_choice':third_choice_
    }


    return render(request, "education_dashboard.html", context)

def applfinalization(request,pk):
    if request.method == "POST":
        obj = Application.objects.get(id=pk)
        obj.status = "Οριστικοποιημένη"
        obj.save()
    view_my_application(request,pk)

@login_required
@professor_required
def select_applications_for_program(request,pk):
    # applications = Application.objects.get(program_id=pk)
    
    # applications = BasicUserInfo.objects.select_related('application').filter(application__program_id=pk).exclude(application__status="Υπό Επεξεργασία")
    # does not work applications = Application.objects.prefetch_related('educationinfo_set', 'basicuserinfo_set').filter(Q(status="Υπό Επεξεργασία") & Q(program_id=pk))
    applications = Application.objects.filter(program_id=pk).prefetch_related('basicuserinfo_set')
    applicationsFilter = ApplicationFilter(request.GET, queryset=applications)
    applications = applicationsFilter.qs
    context = {
        'applications':applications,
        'applicationsFilter':applicationsFilter,
    }

    return render(request, "professor_applications.html", context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Μήνυμα απο τη φόρμα επικοινωνίας Μεταπτυχιακών" 
            message = render_to_string("template_contact_form.html", {
            'first_name': form.cleaned_data['first_name'], 
            'last_name': form.cleaned_data['last_name'], 
            'email': form.cleaned_data['email_address'], 
            'message':form.cleaned_data['message'],
            })
    
            email = EmailMessage(subject, message, to=[settings.EMAIL_HOST_USER])
            if email.send():
                messages.success(request, f'Το e-mail στάλθηκε επιτυχώς.', extra_tags='safe')
            else:
                messages.error(request, f'Απέτυχε η αποστολή του e-mail.', extra_tags='safe')


    form = ContactForm()

    return render(request, "contact.html", {'form':form})
