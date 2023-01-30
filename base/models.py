from django.db import models
from django.core.validators import MaxLengthValidator
# Create your models here.


class Userdata(models.Model):
    ROLE_CHOICES = (
        ('student','student'),
        ('faculty','faculty'),
        ('admin','admin'),
    )
    email = models.CharField(max_length=100,primary_key=True)
    first_name =  models.CharField(max_length=100)
    last_name =  models.CharField(max_length=100)
    userrole = models.CharField(max_length=20,choices=ROLE_CHOICES,default="student")


    def __str__(self):
        return self.email

class Cohort(models.Model):
    id = models.AutoField(primary_key=True,editable=True)
    origin=models.BooleanField(default=False)
    title = models.CharField(max_length=200,validators=[MaxLengthValidator(100)])
    email = models.ForeignKey(Userdata, on_delete=models.CASCADE,default='0',db_constraint=False)
    

    def __str__(self):
        return self.title

class Subcohort(models.Model):
    cohort_id=models.ForeignKey(Cohort,on_delete=models.CASCADE,default=0,db_constraint=False,related_name='subcohortid')
    parent_id=models.ForeignKey(Cohort,on_delete=models.CASCADE,default=0,db_constraint=False,related_name='subparentid')

class Cohortpdfs(models.Model):
    id = models.AutoField(primary_key=True,editable=True)
    title= models.CharField(max_length=200,validators=[MaxLengthValidator(100)])
    cohort_id=models.ForeignKey(Cohort,on_delete=models.CASCADE,default=0,db_constraint=False)
    content_date = models.DateField( auto_now_add=True, blank=True)
    content_time = models.TimeField( auto_now_add=True, blank=True)
    qn_published = models.BooleanField(default=False)

class Cohortstudent(models.Model):
    email = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    cohort=models.ForeignKey(Cohort,on_delete=models.CASCADE,default=0,db_constraint=False)

class facedetails(models.Model):
    email = models.CharField(max_length=100)
    fullname=models.CharField(max_length=200)

class readattempt(models.Model):
    email = models.CharField(max_length=100)
    pdf = models.IntegerField()
    total = models.IntegerField()
    onscreen =  models.IntegerField()
    sus =  models.IntegerField()


class Question(models.Model):
    type=models.CharField(max_length=20)
    cohort=models.ForeignKey(Cohort,on_delete=models.CASCADE)
    source = models.IntegerField(default=0)

class Mcq(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    question_title=models.CharField(max_length=200, default="-")
    option1=models.CharField(max_length=100)
    option2=models.CharField(max_length=100)
    option3=models.CharField(max_length=100)
    option4=models.CharField(max_length=100)
    correct_answer=models.CharField(max_length=100)


class Cq(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    question_title=models.CharField(max_length=200, default="-")
    correct_answer=models.CharField(max_length=600)

class quizattempt(models.Model):
    email= models.ForeignKey(Userdata, on_delete=models.CASCADE,default='0',db_constraint=False)
    source = models.IntegerField(default=0)
    starttime = models.FloatField(default=0.0)

class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    email= models.ForeignKey(Userdata, on_delete=models.CASCADE,default='0',db_constraint=False)
    studentans = models.CharField(max_length=600)
    source = models.IntegerField(default=0)

class Evaluate(models.Model):
    email= models.ForeignKey(Userdata, on_delete=models.CASCADE,default='0',db_constraint=False)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    source = models.IntegerField(default=0)

class Result(models.Model):
    email= models.ForeignKey(Userdata, on_delete=models.CASCADE,default='0',db_constraint=False)
    point = models.IntegerField(default=0)
    source = models.IntegerField(default=0)

class GeeksModel(models.Model):
 
    # fields of the model
    title = models.CharField(max_length = 200)
    description = models.TextField()
 
    # renames the instances of the model
    # with their title name
    def __str__(self):
        return self.title