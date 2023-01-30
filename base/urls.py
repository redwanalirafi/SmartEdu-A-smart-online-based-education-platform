from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
     path('', views.home,name="home"),
     path('dashboard/',views.dashboard,name="dashboard"),
     path('create/<int:id>',views.create,name="create"),
     path('cohort/<int:id>',views.cohort,name="cohort"),
     path('pdfviewer/<int:id>',views.pdfviewer,name="pdfviewer"),
     path('assign/<int:id>',views.assign,name="assign"),
     path('students/<int:id>',views.viewstudents,name="viewstudents"),
     path('trackface/<int:pdf>',views.trackface,name="trackface"),
     path('setquestion/<int:fileid>/<int:cohortid>',views.setquestion,name="setquestion"),
     path('monitorstudent/<int:fileid>/<int:cohortid>',views.monitorstudent,name="monitorstudent"),
     path('showchart/<int:id>',views.showchart,name="showchart"),
     path('examhall/<int:fileid>',views.examhall,name="examhall"),
     path('results/<int:fileid>/<int:cohortid>',views.results,name="results"),
     path('test/',views.test,name="test"),


     # Deletes

     path('delete/<int:id>/<int:cohort>',views.delete,name="delete"),
     path('deletefile/<int:id>/<int:cohort>',views.deletefile,name="deletefile"),
     path('removestudent/<int:idcohort>/<str:useremail>',views.removestudent,name="removestudent"),
     path('deleteqn/<int:id>',views.deleteqn,name="deleteqn"),
]
