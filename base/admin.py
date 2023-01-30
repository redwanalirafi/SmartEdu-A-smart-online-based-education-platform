from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Userdata)

admin.site.register(readattempt)


@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ['id','title','email']

@admin.register(quizattempt)
class quizattemptAdmin(admin.ModelAdmin):
    list_display = ['email','source','starttime']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['email','question','studentans','source']

@admin.register(Subcohort)
class SubcohortAdmin(admin.ModelAdmin):
    list_display = ['cohort_id','parent_id']


@admin.register(Cohortpdfs)
class CohortpdfsAdmin(admin.ModelAdmin):
    list_display = ['cohort_id','title','content_date','content_time','qn_published']

@admin.register(Cohortstudent)
class CohortstudentAdmin(admin.ModelAdmin):
    list_display = ['cohort','email']

@admin.register(facedetails)
class facedetailsAdmin(admin.ModelAdmin):
    list_display = ['id','email','fullname']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','type','cohort','source']

@admin.register(Cq)
class CqAdmin(admin.ModelAdmin):
    list_display = ['question','question_title','correct_answer']

@admin.register(Mcq)
class McqAdmin(admin.ModelAdmin):
    list_display = ['question','question_title','option1','option2','option3','option4','correct_answer']


@admin.register(Evaluate)
class EvaluateAdmin(admin.ModelAdmin):
    list_display = ['email','question','point','source']
    
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['email','point','source']