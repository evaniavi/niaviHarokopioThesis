import django_filters
from django_filters import CharFilter,DateFilter
from django import forms

from personal.models import *
from django.contrib.postgres.forms.ranges import RangeWidget
from django.forms.widgets import DateInput, TextInput


APPLICATION_STATUS = (
    ("Οριστικοποιημένη", "Οριστικοποιημένη"),
    ("Αποδεκτή", "Αποδεκτή"),
    ("Απορρίφθηκε", "Απορρίφθηκε"),
)

# class ApplicationFilter(django_filters.FilterSet):
#     application__status = django_filters.ChoiceFilter( 

#         choices=APPLICATION_STATUS,label='Κατάσταση Αίτησης',
#         widget=forms.Select(attrs={'class': 'form-control' ,'style' :'width: 50%;'}))
#     application__year = django_filters.CharFilter(lookup_expr='icontains', 
#         label='Έτος Αίτησης',
#         widget=forms.TextInput(attrs={'class': 'form-control','style' :'width: 50%;'}))

#     class Meta:
#         model = BasicUserInfo
#         fields = {
#             'application__status': ['exact'],
#             }

class ApplicationFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter( 

        choices=APPLICATION_STATUS,label='Κατάσταση Αίτησης',
        widget=forms.Select(attrs={'class': 'form-control' ,'style' :'width: 50%;'}))
    year = django_filters.CharFilter(lookup_expr='icontains', 
        label='Έτος Αίτησης',
        widget=forms.TextInput(attrs={'class': 'form-control','style' :'width: 50%;'}))
    educationinfo__university = django_filters.CharFilter(field_name="educationinfo__university",lookup_expr='icontains', 
        label='Πανεπιστήμιο',
        widget=forms.TextInput(attrs={'class': 'form-control','style' :'width: 50%;'}))

    class Meta:
        model = Application
        fields = {
            'status': ['exact'],
            }

# class ApplicationFilter(django_filters.FilterSet):
#     university = django_filters.CharFilter(field_name='education_info__university__name', lookup_expr='icontains')

#     class Meta:
#         model = Application
#         fields = ['status']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.filters['university'].label = 'University'

#     @property
#     def qs(self):
#         qs = super().qs
#         if self.request is not None and self.request.GET:
#             university = self.request.GET.get('university')
#             if university:
#                 qs = qs.filter(application__education_info__university__name__icontains=university)
#         return qs



        # parent = super().qs
       
        # return parent

# class SpeechFilter(django_filters.FilterSet):
#     start_date = DateFilter(field_name="created_on", lookup_expr="gte")
#     end_date = DateFilter(field_name="created_on", lookup_expr="lte")
#     start_req_date = DateFilter(field_name="requested_date", lookup_expr="gte")
#     end_req_date = DateFilter(field_name="requested_date", lookup_expr="lte")
#     labels = {
#             'title': 'Τίτλος',
#             'description': 'Περιγραφή',
#             'status': 'Κατάσταση',
#             'date_range': 'Διάστημα Ημερομηνιών',
#             'requested_date_range': 'Διάστημα Αιτηθέντων Ημερομηνιών',
#         }

#     class Meta:
#         model = SpeechRequisition
#         fields = {
#             'title': ['contains'],
#             'description': ['contains'],
#             'status': ['exact'],
#             }



# class TravelFilter(django_filters.FilterSet):
#     start_date = DateFilter(field_name="created_on", lookup_expr="gte")
#     end_date = DateFilter(field_name="created_on", lookup_expr="lte")
#     start_req_date = DateFilter(field_name="requested_date", lookup_expr="gte")
#     end_req_date = DateFilter(field_name="requested_date", lookup_expr="lte")
#     labels = {
#             'title': 'Τίτλος',
#             'description': 'Περιγραφή',
#             'status': 'Κατάσταση',
#             'date_range': 'Διάστημα Ημερομηνιών',
#             'requested_date_range': 'Διάστημα Αιτηθέντων Ημερομηνιών',
#         }

#     class Meta:
#         model = TravelRequisition
#         fields = {
#             'title': ['contains'],
#             'description': ['contains'],
#             'status': ['exact'],
#             'location':['contains'],
#             }