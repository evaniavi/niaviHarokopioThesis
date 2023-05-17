from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from personal.models import *
from django.forms.widgets import DateTimeInput
from django.contrib.admin import widgets
from captcha.fields import CaptchaField

DEGREE_TYPES = (
    ("Προπτυχιακό", "Προπτυχιακό"),
    ("Μεαπτυχιακό", "Μεαπτυχιακό"),
    ("Σεμινάριο", "Σεμινάριο"),
    ("Διαδικτυακά Μαθήματα" , "Διαδικτυακά Μαθήματα")
)

STUDIES_TYPES = (
    ("Μερικής Φοίτησης", "Μερικής Φοίτησης"),
    ("Πλήρους Φοίτησης", "Πλήρους Φοίτησης"),
)

class DateInput(forms.DateInput):
  input_type = 'date'

class TextInput(forms.DateInput):
  input_type = 'text'

class CreateUserForm(UserCreationForm):
    # email = forms.EmailField()
    # profile_pic = forms.ImageField()
    username= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'username', 
                               'id':'username', 
                               'type':'text', 
                               'placeholder':'Όνομα Χρήστη', 
                                'maxlength': '16', 
                                'minlength': '3', 
				        } ))
    email= forms.EmailField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'email', 
                               'id':'email', 
                               'type':'email', 
                               'placeholder':'Email', 
                                 
				        } ))
    password1 = forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'password1', 
                               'id':'password1', 
                               'type':'password', 
                               'placeholder':'Κωδικός Πρόσβασης',  
				        } ))
    password2 = forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'password2', 
                               'id':'password2', 
                               'type':'password', 
                               'placeholder':'Επαλήθευση Κωδικού',  
				        } ))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

        labels = {
        "username": "Όνομα Χρήστη",
        "email": "Email",
        "password1": "Κωδικός",
        'password2' : 'Επανάληψη Κωδικού',
        }


class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget= forms.FileInput
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'profile_pic', 
                               'id':'profile_pic', 
                               'placeholder':'Εικόνα Προφίλ',  
                               'onchange' : "readURL(this);"
				        } ))
    class Meta():
        model = Profile
        fields = ['profile_pic']
        labels = {
        "profile_pic": "Εικόνα Προφίλ",
        }

class EducationInfo_form(forms.ModelForm):
    class Meta():
        model = EducationInfo
        fields = ['degree_type','title','university','average','graduation_year','thesis_title','thesis_description','pdf_degree','pdf_thesis']

        labels = {
        "title": "Τίτλος σπουδών",
        "university": "Φορέας",
        "average": "Μέσος Όρος",
        "graduation_year": "Έτος/Αναμενόμενο έτος Αποφοίτησης",
        'thesis_title' : 'Τίτλος Πτυχιακής',
        'thesis_description' : 'Περιγραφή Πτυχιακής',
        'pdf_degree' :'PDF πτυχίου',
        'pdf_thesis' : 'PDF πτυχιακής',
        'degree_type' : 'Τύπος πτυχίου'
        }

        title= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'title', 
                               'id':'title', 
                               'type':'text', 
                               'placeholder':'Τίτλος σπουδών', 
                                'minlength': '3', 
				        } ))

        university= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'university', 
                               'id':'university', 
                               'type':'text', 
                               'placeholder':'Φορέας', 
                               
                                'minlength': '3', 
				        } ))

        average= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'average', 
                               'id':'average', 
                               'type':'text', 
                               'placeholder':'Μέσος Όρος', 
                               
                                'minlength': '3', 
				        } ))

        graduation_year= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'graduation_year', 
                               'id':'graduation_year', 
                               'type':'text', 
                               'placeholder':'Έτος/Αναμενόμενο έτος Αποφοίτησης', 
                               
                                'minlength': '3', 
				        } ))
        thesis_title= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'False', 
                               'name':'thesis_title', 
                               'id':'thesis_title', 
                               'type':'text', 
                               'placeholder':'Τίτλος Πτυχιακής', 
                               
                                'minlength': '3', 
				        } ))
        thesis_description= forms.CharField(widget= forms.Textarea 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'False', 
                               'name':'thesis_description', 
                               'id':'thesis_description', 
                               'type':'text', 
                               'placeholder':'Περιγραφή Πτυχιακής', 
				        } ))
        pdf_degree= forms.FileField(widget= forms.FileInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'False',  
                              'name':'pdf_degree', 
                               'id':'pdf_degree',

				        } ))
        pdf_thesis= forms.FileField(widget= forms.FileInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'False', 
                               'name':'pdf_thesis', 
                               'id':'pdf_thesis', 
                               'type':'file', 
                               'placeholder':'PDF πτυχιακής',  
				        } ))
        degree_type= forms.ChoiceField(choices = DEGREE_TYPES)

        
        widgets = {
            'title' : TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}),
            'university' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}),  
            'average' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}) ,   
            'graduation_year' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}) ,
            # 'thesis_title' : forms.Textarea (attrs={'type': 'text',
            #                                'class': 'form-control', 
            #                                'required':'False',})  ,
            #  'thesis_description' : forms.Textarea (attrs={'class': 'form-control', 
            #                               'required':'False',  
            #                                } )     ,

              'degree_type': forms.Select(choices = DEGREE_TYPES,attrs={ 
                             'class': 'form-control', 
                             'required':'True', 
                             'name':'degree_type', 
                             'id':'degree_type', 
				        } )
        #  forms.ModelChoiceField(widget= forms.TextInput 
        #                    (attrs={ 
        #                      'class': 'form-control', 
        #                       'required':'True', 
        #                        'name':'title', 
        #                        'id':'title', 
        #                        'type':'text', 
        #                        'placeholder':'Τίτλος σπουδών', 
        #                         'minlength': '3', 
				#         } ))                                                                                                              
        }

class BasicInfo_form(forms.ModelForm):
    class Meta():
        model = BasicUserInfo
        fields = ['name','surname','fatherName','motherName','afm','birth_date']
        name= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'name', 
                               'id':'name', 
                               'type':'text', 
                               'placeholder':'Όνομα', 
                                
                                'minlength': '3', 
				        } ))

        surname= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'surname', 
                               'id':'surname', 
                               'type':'text', 
                               'placeholder':'Επίθετο', 
                               
                                'minlength': '3', 
				        } ))

        fatherName= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'fatherName', 
                               'id':'fatherName', 
                               'type':'text', 
                               'placeholder':'Όνομα Πατρός', 
                               
                                'minlength': '3', 
				        } ))

        motherName= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'motherName', 
                               'id':'motherName', 
                               'type':'text', 
                               'placeholder':'Όνομα Μητρός', 
                               
                                'minlength': '3', 
				        } ))

        # birth_date= forms.DateField(widget= DateInput(attrs={ 
        #                      'class': 'form-control', 
        #                       'required':'True', 
        #                        'name':'birth_date', 
        #                        'id':'birth_date', 
        #                        'type':'date', 
        #                        'placeholder':'Ημερομηνία Γέννησης', 
                               
        # }))
        
        labels = {
        "name": "Όνομα",
        "surname": "Επώνυμο",
        "fatherName": "Όνομα Πατρός",
        "motherName": "Όνομα Μητρός",
        'afm' : 'Αριθμός Φορολογικού Μητρώου',
        'birth_date' : 'Ημερομηνία Γέννησης'
        }
        widgets = {
            # 'birth_date': DateInput(attrs={'type': 'date',
            #                                'class': 'form-control', 
            #                                'required':'True',}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder':'π.χ 25/06/1996', 'type': 'date'},format=('%Y-%m-%d')),
            'name' : TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}),
            'surname' : TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}),  
            'fatherName' : TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}) ,   
            'motherName' : TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}) ,
            'afm' : TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',})                                                                                                                     
        }

    def clean_date(self):
      birth_date = self.cleaned_data['date']
      if birth_date > datetime.date.today():
        raise forms.ValidationError("The date cannot be in the future!")
      return birth_date


# maybe a SettingsUserForm with username email and profile pic fields

class WorkExperienceInfo_form(forms.ModelForm):
    class Meta():
        model = JobInfo
        fields = ['job_title','employer','duties_description','start_date','end_date']

        labels = {
        "job_title": "Τίτλος Εργασίας",
        "employer": "Εργοδότης",
        "duties_description": "Περιγραφή Καθηκόντων",
        "start_date": "Ημερομηνία Έναρξης",
        "end_date" : "Ημερομηνία Λήξης",
        }

        job_title= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'job_title', 
                               'id':'job_title', 
                               'type':'text', 
                               'placeholder':'Τίτλος Εργασίας', 
                                'minlength': '3', 
				        } ))

        employer= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'employer', 
                               'id':'employer', 
                               'type':'text', 
                               'placeholder':'Εργοδότης', 
                                'minlength': '3', 
				        } ))

        duties_description= forms.CharField(widget= forms.Textarea 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'duties_description', 
                               'id':'duties_description', 
                               'type':'text', 
                               'placeholder':'Περιγραφή Καθηκόντων', 
				        } ))
        
        widgets = {
            'job_title' : TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}),
            'employer' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control',}), 
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder':'π.χ 25/06/1996', 'type': 'date'},format=('%Y-%m-%d')),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder':'π.χ 25/06/1996', 'type': 'date'},format=('%Y-%m-%d')),
            'duties_description' : forms.Textarea (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',})  
        }
      # def clean_date(self):
      #   birth_date = self.cleaned_data['date']
      #   if birth_date > datetime.date.today():
      #     raise forms.ValidationError("The date cannot be in the future!")
      #   return birth_date                                                                                                  
        
class Recommendation_form(forms.ModelForm):
    class Meta():
        model = Recommendation
        fields = ['recom_name','recom_surname','recom_email','recom_organism','recom_position']

        labels = {
        "recom_name": "Όνομα",
        "recom_surname": "Επίθετο",
        "recom_email": "E-mail",
        "recom_organism": "Οργανισμός",
        "recom_position": "Θέση",
        }

        recom_name= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'recom_name', 
                               'id':'recom_name', 
                               'type':'text', 
                               'placeholder':'Όνομα', 
                                'minlength': '3', 
				        } ))

        recom_surname= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'recom_surname', 
                               'id':'recom_surname', 
                               'type':'text', 
                               'placeholder':'Επίθετο', 
                                'minlength': '3', 
				        } ))

        recom_email= forms.EmailField(widget= forms.EmailInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'recom_email', 
                               'id':'recom_email', 
				        } ))
        recom_organism= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'recom_surname', 
                               'id':'recom_surname', 
                               'type':'text', 
                               'placeholder':'Οργανισμός', 
                                'minlength': '3', 
				        } ))
        recom_position= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'recom_surname', 
                               'id':'recom_surname', 
                               'type':'text', 
                               'placeholder':'Θέση', 
                                'minlength': '3', 
				        } ))
        
        widgets = {
            'recom_name' : TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}),
            'recom_surname' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control',}), 
            'recom_email': forms.EmailInput(attrs={'class': 'form-control', 
                              'required':'True', 
                               'name':'recom_email', 
                               'id':'recom_email', }),
            'recom_organism' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control',}), 
            'recom_position' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control',}), 
            
        }

class ForeignLanguages_form(forms.ModelForm):
    class Meta():
        model = ForeignLanguages
        fields = ['name','level','score','degree_name','date_of_acquisition'] 
        # ,'application'

        labels = {
        "name": "Όνομα",
        "level": "Επίπεδο",
        "score": "Βαθμός",
        "degree_name": "Όνομα Πτυχίου",
        "date_of_acquisition": "Ημερομηνία Απόκτησης",
        }

        name= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'name', 
                               'id':'name', 
                               'type':'text', 
                               'placeholder':'Όνομα', 
                                'minlength': '3', 
				        } ))

        level= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'level', 
                               'id':'level', 
                               'type':'text', 
                              
                                'minlength': '3', 
				        } ))

        score= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'score', 
                               'id':'score', 
                               'type':'text', 
                              
                                'minlength': '3', 
				        } ))
        degree_name= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'degree_name', 
                               'id':'degree_name', 
                               'type':'text', 
				        } ))
        
        widgets = {
            'name' : TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True','placeholder':'Π.χ. Αγγλικά'}),
            'level' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control','placeholder':'Π.χ. Lower,Advanced'}), 
            'score' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control','placeholder':'Π.χ. 7.5'}),
            'degree_name' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control','placeholder':'Π.χ. KΠγ,Cambridge'}), 
            'date_of_acquisition': forms.DateInput(attrs={'class': 'form-control', 'placeholder':'π.χ 25/06/1996', 'type': 'date'},format=('%Y-%m-%d')),
            # 'application' : forms.HiddenInput(),
            
        }

class AdditionalInfo_form(forms.ModelForm):
    class Meta():
        model = AdditionalInfo
        fields = ['reason_of_selection','other_applications','studies_type','first_choice','second_choice','third_choice']

        reason_of_selection= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'reason_of_selection', 
                               'id':'reason_of_selection', 
                               'type':'text', 
                               
                                'minlength': '3', 
				        } ))

        other_applications= forms.CharField(widget= forms.TextInput 
                           (attrs={ 
                             'class': 'form-control', 
                              'required':'True', 
                               'name':'other_applications', 
                               'id':'other_applications', 
                               'type':'text', 
                              
                               
                                'minlength': '3', 
				        } ))

        degree_type= forms.ChoiceField(choices = STUDIES_TYPES)
        first_choice=forms.ChoiceField(choices = STUDIES_TYPES)
        second_choice=forms.ChoiceField(choices = STUDIES_TYPES,required=False)
        third_choice=forms.ChoiceField(choices = STUDIES_TYPES,required=False)


        widgets = {
            'reason_of_selection' : TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}),
            'other_applications' : forms.TextInput (attrs={'type': 'text',
                                           'class': 'form-control', 
                                           'required':'True',}),  

              'studies_type': forms.Select(choices = STUDIES_TYPES,attrs={ 
                             'class': 'form-control', 
                             'required':'True', 
                             'name':'studies_type', 
                             'id':'studies_type', 
				        } ),

              'first_choice': forms.Select(choices = STUDIES_TYPES,attrs={ 
                             'class': 'form-control', 
                             'required':'True', 
                             'name':'first_choice', 
                             'id':'first_choice', 
				        } ),

              'second_choice': forms.Select(choices = STUDIES_TYPES,attrs={ 
                             'class': 'form-control', 

                             'name':'second_choice', 
                             'id':'second_choice', 
				        } ),

              'third_choice': forms.Select(choices = STUDIES_TYPES,attrs={ 
                             'class': 'form-control', 

                             'name':'third_choice', 
                             'id':'third_choice', 
				        } )
                                                                                                            
        }



#contact form
class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50, widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Όνομα'}),label='Εισάγετε όνομα')
	last_name = forms.CharField(max_length = 50, widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Επίθετο'}),label='Εισάγετε επίθετο')
	email_address = forms.EmailField(max_length = 50, widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@domain.com'}),label='Εισάγετε email')
	message = forms.CharField(max_length = 2000, widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Κείμενο μηνύματος'}),label='Εισάγετε κείμενο μηνύματος')
	captcha = CaptchaField(label='Εισάγετε το κέιμενο της εικόνας')

	class Μeta:

		labels = {
        "first_name": "Όνομα",
        "last_name": "Επίθετο",
        "email_address": "Διεύθυνση Email",
		"message": "Μήνυμα"
        }
      