from django.contrib import admin
from .models import *
from django.db.models.expressions import Subquery, OuterRef
from django.core.mail import send_mail
from import_export.admin import ExportActionMixin, ImportExportMixin, ImportExportModelAdmin,ImportExportActionModelAdmin
from django.contrib.admin import AdminSite

# Register your models here.
# admin.site.register(Profile)
# admin.site.register(BasicUserInfo)
# admin.site.register(EducationInfo)
# admin.site.register(Departments)
# admin.site.register(PostgraduatePrograms)
# admin.site.register(ProgramDirections)
# admin.site.register(Application)
# admin.site.register(JobInfo)
# admin.site.register(Recommendation)
# admin.site.register(AdditionalInfo)
# admin.site.register(ForeignLanguages)

class EducationInline(admin.TabularInline):
    model = EducationInfo
    exclude = ['user']

class ApplicationInline(ExportActionMixin,admin.TabularInline):
    model = Application

class BasicUserInfoInline(admin.StackedInline):
    model = BasicUserInfo
    exclude = ['user']

class JobInfoInline(admin.TabularInline):
    model = JobInfo
    exclude = ['user']

class RecommendationInline(admin.TabularInline):
    model = Recommendation
    exclude = ['user']

class AdditionalInfoInline(admin.StackedInline):
    model = AdditionalInfo
    exclude = ['user']

class ForeignLanguagesInline(admin.TabularInline):
    model = ForeignLanguages
    exclude = ['user']

class AssignedProffessorsInline(admin.TabularInline):
    model = AssignedProffessors
    exclude = ['user']

def set_status_accepted(modeladmin, request,queryset):  
    for i in queryset:
        user = User.objects.filter(id=i.user_id).first()
        send_mail('HUA-Αποτέλεσμα Αίτησης σε Μεταπτυχιακό', 'Αγαπητέ/ή '+ user.last_name +',\nΜε χαρά σας ανακοινώνουμε οτι έχετε επιλεγεί για το πρόγραμμα \t'+ i.program.name,None,[user.email], fail_silently=True)
        #before user.email maybe config.email for each departementsecretary
    queryset.update(status = 'Αποδεκτή')

#Action Description
set_status_accepted.short_description = "Αποδοχή επιλεγμένων Αιτήσεων"

#reject application
def set_status_denied(modeladmin, request,queryset):
    for i in queryset:
        user = User.objects.filter(id=i.user_id).first()
        send_mail('HUA-Αποτέλεσμα Αίτησης σε Μεταπτυχιακό', 'Αγαπητέ/ή '+ user.last_name +',\nΛυπούμαστε που σας ενημερώνουμε οτι δυστυχώς απορριφθήκατε από το πρόγραμμα \t'+ i.program.name,None,[user.email], fail_silently=True)
        #before user.email maybe config.email for each departementsecretary
    queryset.update(status = 'Απορρίφθηκε')

set_status_denied.short_description = "Απόριψη επιλεγμένων Αιτήσεων"

#recommendation letters
def ask_recommendations(modeladmin, request,queryset):
    for i in queryset:
        basicInfo = i.basicuserinfo_set.first()
        for j in i.recommendation_set.all() :
            send_mail('HUA-Έκκληση για Συστατική επιστολή', 'Αγαπητέ/ή ' +',\nΣτειλτε μας συστατική επιστολή για τον/ην ' + basicInfo.surname + ' '+ basicInfo.name +' που έκανε αίτηση στο πρόγραμμα '+ i.program.name,None,[j.recom_email], fail_silently=True)
 
    

ask_recommendations.short_description = "Ζητήστε Συστατικές επιστολές"

class ApplicationAdmin(ExportActionMixin,admin.ModelAdmin):

    
    inlines = [BasicUserInfoInline,
        EducationInline,JobInfoInline,RecommendationInline,ForeignLanguagesInline,AdditionalInfoInline
    ]
    list_display = ('id',
        'status',
        'user',
        'program',
        'year',
    )
    readonly_fields = ('id',
        'status',
        'user',
        'program',
        'year','creation_date')
    list_filter = ('year','program')
    search_fields = ('program','year')
    # list_display_links = (
    #     'id',
    #     'user',
    #     'program',
    # )
    def get_queryset(self, request):
        dep = 0
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='secretary_dit').exists():
            dep=1
            program = PostgraduatePrograms.objects.filter(department_id=dep)
        elif request.user.groups.filter(name='secretary_geo').exists():
            dep=3
            program = PostgraduatePrograms.objects.filter(department_id=dep)
        else:
            program = PostgraduatePrograms.objects.all()
        return qs.filter(program_id__in=program,status="Οριστικοποιημένη").prefetch_related('recommendation_set') #.exclude(status="Υπό Επεξεργασία")
    
    # list_editable = ('status',)
    # def change_view(self, request, object_id, extra_context=None):       
    #     self.exclude = ('user',
    #     'program','creation_date' )
    #     return super(ApplicationAdmin, self).change_view(request, object_id, extra_context)
    actions = [set_status_accepted, set_status_denied,ask_recommendations]

class ApprovedApplication(Application):
    class Meta:
        proxy=True
        verbose_name = 'Εγκεκριμένη Αίτηση Χρήστη'
        verbose_name_plural = 'Εγκεκριμένες Αιτήσεις Χρήστών'
    
class ApprovedApplicationAdmin(admin.ModelAdmin):
    
    inlines = [BasicUserInfoInline,
        EducationInline,JobInfoInline,RecommendationInline,ForeignLanguagesInline,AdditionalInfoInline
    ]
    list_display = ('id',
        'status',
        'user',
        'program',
        'year',
    )
    # list_display_links = (
    #     'id',
    #     'user',
    #     'program',
    #     'year'
    # )
    readonly_fields = ('id',
        'status',
        'user',
        'program',
        'year','creation_date')
    list_filter = ('user', 'year')
    search_fields = ('user__username','year')

    def get_queryset(self, request):
        dep = 0
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='secretary_dit').exists():
            dep=1
            program = PostgraduatePrograms.objects.filter(department_id=dep)
        elif request.user.groups.filter(name='secretary_geo').exists():
            dep=3
            program = PostgraduatePrograms.objects.filter(department_id=dep)
        else:
            program = PostgraduatePrograms.objects.all()
        return qs.filter(program_id__in=program,status="Αποδεκτή")



class RejectedApplication(Application):
    class Meta:
        proxy=True
        verbose_name = 'Απορριφθείσα Αίτηση Χρήστη'
        verbose_name_plural = 'Απορριφθείσες Αιτήσεις Χρήστών'
    
class RejectedApplicationAdmin(admin.ModelAdmin):
    
    inlines = [BasicUserInfoInline,
        EducationInline,JobInfoInline,RecommendationInline,ForeignLanguagesInline,AdditionalInfoInline
    ]
    list_display = ('id',
        'status',
        'user',
        'program',
        'year',
    )
    readonly_fields = ('id',
        'status',
        'user',
        'program',
        'year','creation_date')
    # list_display_links = (
    #     'id',
    #     'user',
    #     'program',
    # )
    list_filter = ('user', 'year')
    search_fields = ('user__username','year')
    def get_queryset(self, request):
        dep = 0
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='secretary_dit').exists():
            dep=1
            program = PostgraduatePrograms.objects.filter(department_id=dep)
        elif request.user.groups.filter(name='secretary_geo').exists():
            dep=3
            program = PostgraduatePrograms.objects.filter(department_id=dep)
        else:
            program = PostgraduatePrograms.objects.all()
        return qs.filter(program_id__in=program,status="Απορρίφθηκε")
    
    
class DirectionsAdmin(admin.ModelAdmin):
    
    list_display = (
        'name',
        'program',

    )
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
                if db_field.name == "program":
                    dep = 0
                    if request.user.groups.filter(name='secretary_dit').exists():
                        dep=1
                    elif request.user.groups.filter(name='secretary_geo').exists():
                        dep=3
                    kwargs["queryset"] = PostgraduatePrograms.objects.filter(department_id=dep)
                    return super(DirectionsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
                if db_field.name == "name":
                    kwargs["queryset"] = ProgramDirections.objects
                    return super(DirectionsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    
class PostgradProgramsAdmin(admin.ModelAdmin):
    
    list_display = (
        'name',
        'department',

    )
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
                if db_field.name == "department":
                    dep = 0
                    if request.user.groups.filter(name='secretary_dit').exists():
                        dep=1
                    elif request.user.groups.filter(name='secretary_geo').exists():
                        dep=3
                    kwargs["queryset"] = Departments.objects.filter(id=dep)
                    return super(PostgradProgramsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
                if db_field.name == "name":
                    kwargs["queryset"] = PostgraduatePrograms.objects
                    return super(PostgradProgramsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    def get_queryset(self, request):
        dep = 0
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='secretary_dit').exists():
            dep=1
            program = PostgraduatePrograms.objects.filter(department_id=dep)
            
        elif request.user.groups.filter(name='secretary_geo').exists():
            dep=3
            program = PostgraduatePrograms.objects.filter(department_id=dep)
        else:
            program = PostgraduatePrograms.objects.all()
        return qs.filter(id__in=program).select_related('department')

class AssignedProfessorsAdmin(admin.ModelAdmin):
    
    list_display = (
        'user',
        'program',

    )
    # inlines = [AssignedProffessorsInline]


    # list_filter = ('year','program')
    # search_fields = ('program','year')
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
                if db_field.name == "program":
                    dep = 0
                    if request.user.groups.filter(name='secretary_dit').exists():
                        dep=1
                    elif request.user.groups.filter(name='secretary_geo').exists():
                        dep=3
                    kwargs["queryset"] = PostgraduatePrograms.objects.filter(department_id=dep)
                    return super(AssignedProfessorsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
                if db_field.name == "user":
                    kwargs["queryset"] = User.objects.select_related('profile').filter(profile__title__contains='Καθηγητής')
                    return super(AssignedProfessorsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
                
    def get_queryset(self, request):
        dep = 0
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='secretary_dit').exists():
            dep=1
            program = PostgraduatePrograms.objects.filter(department_id=dep)
            
        elif request.user.groups.filter(name='secretary_geo').exists():
            dep=3
            program = PostgraduatePrograms.objects.filter(department_id=dep)
        else:
            program = PostgraduatePrograms.objects.all()
        return qs.filter(program_id__in=program).select_related('program') #.exclude(status="Υπό Επεξεργασία")
    
   


admin.site.register(AssignedProffessors,AssignedProfessorsAdmin)
admin.site.register(Application,ApplicationAdmin)
admin.site.register(ApprovedApplication,ApprovedApplicationAdmin)
admin.site.register(RejectedApplication,RejectedApplicationAdmin)
admin.site.register(ProgramDirections,DirectionsAdmin)
admin.site.register(PostgraduatePrograms,PostgradProgramsAdmin)



