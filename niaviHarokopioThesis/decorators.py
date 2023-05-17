from django.http import HttpResponse    
from django.shortcuts import redirect
from personal.models import Profile
from django.contrib.auth.decorators import user_passes_test

#decorator for unauthenticated users
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


#decorator to check if user is a postgrad student
def student_required(function=None):
    def is_postgrad(u):
        return Profile.objects.filter(user=u, title='Φοιτητής').exists()
    actual_decorator = user_passes_test(is_postgrad)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator

#decorator to check if user is a professor
def professor_required(function=None):
    def is_professor(u):
        return Profile.objects.filter(user=u, title='Αναπληρωτής Καθηγητής').exists()
    actual_decorator = user_passes_test(is_professor)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator
    
#decorator to check if user is secretarian
def secretary_required(function=None):
    def is_secretary(u):
        return Profile.objects.filter(user=u, title='Ιδρυματικός Λογαριασμός').exists()
    actual_decorator = user_passes_test(is_secretary)
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator