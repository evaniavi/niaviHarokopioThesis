from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils.timezone import now
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

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

APPLICATION_STATUS = (
    ("Υπό Επεξεργασία", "Υπό Επεξεργασία"),
    ("Οριστικοποιημένη", "Οριστικοποιημένη"),
    ("Αποδεκτή", "Αποδεκτή"),
    ("Απορρίφθηκε", "Απορρίφθηκε"),
)

APPLICATION_PERIOD = (
    ("Ενεργή Περίοδος", "Ενεργή Περίοδος"),
    ("Ανενεργή Πείοδος", "Ανενεργή Πείοδος"),
)

YEAR_CHOICES = [
        (r,r) for r in range(2000, datetime.date.today().year+2)
    ]
def current_year():
    return datetime.date.today().year

# class User(AbstractUser):
#     username = models.CharField(_('username'), max_length = 200, unique = True )
#     email = models.EmailField(_('email address'), unique = True)
#     title = models.CharField(_('title'), max_length = 200, default = 'None' )
#     department = models.CharField(_('department'), max_length = 200, default = 'None' )
   

#for registration form
class Profile(models.Model):
    user = models.OneToOneField(User,
         on_delete=models.CASCADE,
         primary_key=True) 


    #additional registration info
    profile_pic = models.ImageField(upload_to='profile_images',blank=True)

    # new additions for LDAP
    department = models.CharField(max_length=100, null=True, blank=True, verbose_name='Τμήμα',default=None)
    title = models.CharField(max_length=100,  null=True, blank=True, verbose_name='Τίτλος',default='Φοιτητής')

    class Meta:
        db_table="personal_profile" 

    def __str__(self):
        return self.user.username

class Departments(models.Model):
    
    #IMPORTANT-what i will need to change the functionality
    # application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Αίτηση')

    name = models.CharField(max_length=1000, blank=False, verbose_name='Όνομα')

    creation_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Τμήμα'
        verbose_name_plural = 'Τμήματα'

class PostgraduatePrograms(models.Model):
    
    #IMPORTANT-what i will need to change the functionality
    # application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Αίτηση')

    name = models.CharField(max_length=1000, blank=False, verbose_name='Όνομα')

    department = models.ForeignKey(Departments, on_delete=models.CASCADE, verbose_name='Τμήμα')
    creation_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')
    start_date = models.DateField(blank=False,verbose_name="Ημερομηνία Έναρξης") 
    end_date = models.DateField(blank=False,verbose_name="Ημερομηνία Τέλους")

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Πρόγραμμα'
        verbose_name_plural = 'Προγράμματα'

class ProgramDirections(models.Model):


    name = models.CharField(max_length=1000, blank=False, verbose_name='Όνομα Κατεύθυνσης')

    program = models.ForeignKey(PostgraduatePrograms, on_delete=models.CASCADE, verbose_name='Πρόγραμμα')
    creation_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Κατεύθυνση'
        verbose_name_plural = 'Κατευθύνσεις'

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης')
    # department = models.ForeignKey(Departments, on_delete=models.CASCADE, verbose_name='Τμήμα')
    program = models.ForeignKey(PostgraduatePrograms, on_delete=models.CASCADE, verbose_name='Πρόγραμμα')
    status = models.CharField(
        max_length = 50,
        choices = APPLICATION_STATUS,
        default = 'Υπό Επεξεργασία',
        verbose_name='Κατάσταση Αίτησης'
        )
    creation_date = models.DateTimeField(default=timezone.now,blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')
    year = models.IntegerField(choices=YEAR_CHOICES, default=current_year, verbose_name='Έτος Αίτησης',blank=True, null=True) 
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Αίτηση Χρήστη'
        verbose_name_plural = 'Αιτήσεις Χρήστών'


class BasicUserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Αίτηση')
    name = models.CharField(max_length=25, blank=False, null=True, verbose_name='Όνομα')
    surname = models.CharField(max_length=25, blank=False, null=True, verbose_name='Επώνυμο')
    fatherName = models.CharField(max_length=25, blank=False, null=True, verbose_name='Όνομα πατέρα')
    motherName = models.CharField(max_length=25, blank=False, null=True, verbose_name='Όνομα μητέρας')
    afm = models.CharField(max_length=25, blank=False, null=True, verbose_name='ΑΦΜ')
    creation_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')
    birth_date = models.DateField(blank=False,verbose_name="Ημερομηνία Γέννησης") 
    national_id = models.CharField(max_length=50, blank=False, null=True, verbose_name='Αριθμός Ταυτότητας')
    address = models.CharField(max_length=50, blank=False, null=True, verbose_name='Διεύθυνση')
    #IMPORTANT-what i will need to change the functionality
    # application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Αίτηση')
    # national_id = models.CharField(max_length=50, blank=False, null=True, verbose_name='Αριθμός Ταυτότητας')
    # amka =  models.CharField(max_length=50, blank=False, null=True, verbose_name='ΑΜΚΑ')
    # address = models.CharField(max_length=50, blank=False, null=True, verbose_name='Διεύθυνση')
    # number_of_address = models.CharField(max_length=50, blank=False, null=True, verbose_name='Αριθμός')
    ## region = models.CharField(max_length=50, blank=False, null=True, verbose_name='Περιοχή')
    # city = models.CharField(max_length=50, blank=False, null=True, verbose_name='Πόλη')
    # postal_code = models.CharField(max_length=50, blank=False, null=True, verbose_name='Τχυδρομικός Κώδικας')
    

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Βασική Πληροφορία Χρήστη'
        verbose_name_plural = 'Βασικές Πληροφορίες Χρηστών'

def user_directory_path(instance, filename):
    return 'user_{0}/{1}_{2}'.format(instance.user.profile.user.username, instance.title, filename)

class EducationInfo(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Αίτηση')

    title = models.CharField(max_length=100, blank=False, verbose_name='Τίτλος Σπουδών')
    university = models.CharField(max_length=100, blank=False, verbose_name='Φορέας')
    average = models.CharField(max_length=15, blank=True, verbose_name='Μέσος Όρος')
    graduation_year=models.CharField(max_length=15, blank=True, verbose_name='Έτος/Αναμενόμενο έτος Αποφοίτησης')
    thesis_title = models.TextField( blank=True, verbose_name='Τίτλος Πτυχιακής')
    thesis_description = models.TextField( blank=True, verbose_name='Περιγραφή Πτυχιακής')
    pdf_degree = models.FileField(upload_to=user_directory_path, verbose_name='PDF πτυχίου',blank=True,null=True)
    pdf_thesis = models.FileField(upload_to=user_directory_path, verbose_name='PDF πτυχιακής',blank=True,null=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')
    degree_type = models.CharField(
        max_length = 50,
        choices = DEGREE_TYPES,
        default = 'Προπτυχιακό',
        verbose_name='Τύπος Πτυχίου'
        )

    def __str__(self):
        return self.user.username
        # return self.title

    class Meta:
        verbose_name = 'Πτυχίο Χρήστη'
        verbose_name_plural = 'Πτυχία Χρήστη'



class JobInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης')

    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Αίτηση')

    job_title = models.CharField(max_length=100, blank=False, verbose_name='Τίτλος Εργασίας')
    employer = models.CharField(max_length=100,blank=False, verbose_name='Εργοδότης')
    duties_description = models.TextField(blank=False, verbose_name='Περιγραφή Καθηκόντων')
    creation_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')
    start_date = models.DateField(blank=False,verbose_name="Ημερομηνία Έναρξης") 
    end_date = models.DateField(blank=True,verbose_name="Ημερομηνία Τέλους",null=True)


    def __str__(self):
        # return self.job_title
        return self.user.username

    class Meta:
        verbose_name = 'Προϋπηρεσία Χρήστη'
        verbose_name_plural = 'Προϋπηρεσία Χρήστη'


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης')

    #IMPORTANT-what i will need to change the functionality
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Αίτηση')

    recom_name = models.CharField(max_length=100, blank=False, verbose_name='Όνομα')
    recom_surname = models.CharField(max_length=100,blank=False, verbose_name='Επώνυμο')
    recom_email = models.EmailField(max_length=254, blank=False, verbose_name='E-mail')
    recom_phone = models.CharField(max_length=100,blank=False, verbose_name='Τηλέφωνο')
    recom_organism = models.CharField(max_length=100,blank=True, verbose_name='Οργανισμός',null=True)
    recom_position = models.CharField(max_length=100,blank=True, verbose_name='Θέση',null=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')

    def __str__(self):

        return self.user.username

    class Meta:
        verbose_name = 'Συστατική Επιστολή'
        verbose_name_plural = 'Συστατικές Επιστολές'

class AdditionalInfo(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Αίτηση')

    first_choice = models.CharField(max_length=300,blank=False, verbose_name='Πρώτη Επιλογή Κατεύθυνσης')
    second_choice = models.CharField(max_length=300,blank=True, verbose_name='Δεύτερη Επιλογή Κατεύθυνσης',null=True)
    third_choice = models.CharField(max_length=300,blank=True, verbose_name='Τρίτη Επιλογή Κατεύθυνσης',null=True)
    reason_of_selection = models.TextField(blank=False, verbose_name='Λόγος Επιλογής Μεταπτυχιακού')
    other_applications = models.TextField(blank=False, verbose_name='Άλλες Αιτήσεις σε Μεταπτυχιακά')
    studies_type = models.CharField(
        max_length = 50,
        choices = STUDIES_TYPES,
        default = 'Πλήρους Φοίτησης',
        verbose_name='Τύπος Φοίτησης'
        )
    creation_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')

    def __str__(self):
        # return self.id
        return self.user.username

    class Meta:
        verbose_name = 'Επιπρόσθετες Πληροφορίες'
        verbose_name_plural = 'Επιπρόσθετες Πληροφορίες'




class ForeignLanguages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης')
    #IMPORTANT-what i will need to change the functionality
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Αίτηση')

    name = models.CharField(max_length=100, blank=False, verbose_name='Γλώσσα')
    level = models.CharField(max_length=100,blank=False, verbose_name='Επίπεδο')
    score = models.CharField(max_length=20,blank=False, verbose_name='Βαθμός',null=True)
    degree_name = models.CharField(max_length=100,blank=False, verbose_name='Όνομα Πτυχίου',null=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')
    date_of_acquisition = models.DateField(blank=True,verbose_name="Ημερομηνία Απόκτησης",null=True) 

    def __str__(self):
        # return self.name
        return self.user.username

    class Meta:
        verbose_name = 'Ξένη Γλώσσα'
        verbose_name_plural = 'Ξένες Γλώσσες'


#intermediate datatable to know which proffessor is assign to which program
class AssignedProffessors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης')

    program = models.ForeignKey(PostgraduatePrograms, on_delete=models.CASCADE, verbose_name='Πρόγραμμα')
    creation_date = models.DateTimeField(default=timezone.now, blank=True, verbose_name='Ημερομηνία Δημιουργίας')
    last_updated_date = models.DateTimeField(auto_now=True, blank=True, verbose_name='Ημερομηνία Ενημέρωσης')

    def __str__(self):
        # return self.name
        return self.user.username

    class Meta:
        verbose_name = 'Υπεύθυνος Καθηγητής'
        verbose_name_plural = 'Υπέυθυνοι Καθηγητές'

