from .models import *
from django import forms

class CohortForm(forms.ModelForm):

    class Meta:
        model = Cohort

        fields = [
            "origin","title","email",
        ]

        widgets={
            'title' : forms.TextInput(attrs={'class': 'form-control','max_length':20}),
            'email': forms.TextInput(attrs={'type': 'hidden'}),
            'origin': forms.TextInput(attrs={'type': 'hidden'}),
            #'parentCohort': forms.TextInput(attrs={'type': 'hidden'}),
        }

class SubcohortForm(forms.ModelForm):

    class Meta:
        model = Subcohort

        fields = [
            "cohort_id","parent_id",
        ]

 
# creating a form
class GeeksForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = GeeksModel
 
        # specify fields to be used
        fields = [
            "title",
            "description",
        ]

class UserdataForm(forms.ModelForm):

    class Meta:
        model = Userdata
        fields = [
            "email","first_name","last_name", "userrole"
        ]
class CohortpdfsForm(forms.ModelForm):

    class Meta:
        model = Cohortpdfs

        fields = [
            "title","cohort_id",
        ]

        widgets={
            'title' : forms.TextInput(attrs={'class': 'form-control','max_length':20}),
            'content': forms.FileInput(attrs={'class': 'form-control'}),
            'cohort_id': forms.TextInput(attrs={'type': 'hidden'}),
        }

class CohortstudentForm(forms.ModelForm):

    class Meta:
        model = Cohortstudent
        fields = [
            "email","cohort",
        ]