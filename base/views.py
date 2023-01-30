from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.db.models import Q
from .functions import *
from django.http import FileResponse, Http404
import os
from pathlib import Path
from django.db.models import Prefetch
# Create your views here.
from django.contrib.sites.models import Site
from base.backEnd import FaceRecognition

import time 


facerecognition = FaceRecognition()


def home(requests):
    if requests.method == 'POST':
        print("kaj hoy")

    return render(requests,'login.html')



def addFace(face_id):
    face_id = face_id
    facerecognition.faceDetect(face_id)
    facerecognition.trainFace()
    return redirect('/')



def dashboard(requests):
    
    #print("yoyo " , str(User.username))
    

    initiate_user = {
        'email':requests.user.email,
        'first_name':str(requests.user.first_name),
        'last_name':requests.user.last_name,
        'userrole':'student',
    }
    
    room =  Userdata.objects.filter(email=requests.user.email)
    
    
    print(initiate_user)

    if len(room) == 0:
       
        form = UserdataForm(initiate_user)
        print(form.is_valid())

        faceinsert = facedetails.objects.create(fullname=str(requests.user.first_name)+" "+str(requests.user.last_name),email=str(requests.user.email))
        
        faceid=facedetails.objects.filter(email=str(requests.user.email))[0].id
        #print(faceid)

        addFace(int(faceid))
        form.save()
    
    room2 = Userdata.objects.filter(email=requests.user.email).values()
    
    context = {'userdatas' : requests.user, 'counter': 0,'dbuser':room2}

    if len(Cohort.objects.all())>0:
        
    
        parentid=Cohort.objects.filter(origin=True)[0].id
        print(parentid, "<--------")
        #cohorts = Cohort.objects.all()

        sub = Subcohort.objects.select_related('cohort_id').filter(parent_id=parentid).filter(~Q(cohort_id=parentid)).filter(cohort_id__email=requests.user.email)


        print(sub.values())
        

        #print(sub[0].cohort_id.title)
        #print(sub.values())
        context= {'cohorts': sub, 'userdatas' : requests.user, 'counter': 0,'dbuser':room2}

    studentdata=Cohortstudent.objects.filter(email=requests.user.email)

    cohortlist=[]

    print(studentdata)
    for i in studentdata:
        cohortlist.append(i.cohort_id)

    studentlist = Cohort.objects.filter(id__in=cohortlist)

    context['studentcohorts']=studentlist

    return render(requests,'dashboard.html',context)
   





def create(requests,id):
    context = {}
    form = CohortForm(requests.POST or None)
    data =  Cohort.objects.filter(~Q(id=id)).values()

    cohortidnew = Cohort.objects.filter(id=2)
               
    print(cohortidnew)

    if requests.method == 'POST':
        if requests.POST.get("createbtn"):
            
            #First cohort checking
            if(len(Cohort.objects.all())==0):
                initialvalue={
                'origin':True,
                'title':'Origin',
                'email':requests.user.email,
                }
                
                form = CohortForm(initialvalue)
                if form.is_valid():
                    form.save()
                    print('origin created')
            #End

            initialvalue={
                'origin':False,
                'title':requests.POST.get('title'),
                'email':requests.user.email,
            }
            
            form = CohortForm(initialvalue)

            #form.fields['email'].choices = [(requests.user.email, requests.user.email)]

            if form.is_valid():
                form.save()

                cohortidnew = Cohort.objects.latest('id').id
                
                #Finding origin id
                id2=id
                if id2==0:
                    id2=Cohort.objects.filter(origin=True)[0].id
                    print('origin id:',id)

                initialvalue2={
                    'cohort_id':int(cohortidnew),
                    'parent_id':id2,
                }
                print(initialvalue2)
                form2 = SubcohortForm(initialvalue2)
                
                if form2.is_valid():
                    print("2nd done")
                    form2.save()
                    return redirect('/dashboard')
        else:
            id2=id

            cohortidnew = requests.POST.get('idparent')
            
            initialvalue2={
                    'cohort_id':int(cohortidnew),
                    'parent_id':id2,
            }
            print(initialvalue2)
            form2 = SubcohortForm(initialvalue2)
                
            if form2.is_valid():
                    print("2nd done")
                    form2.save()
                    return redirect('/dashboard')
            

    context['form'] = form
    context['id']= id
    context['cohorts']=data

    return render(requests,'create.html', context)





def delete(requests,id,cohort):
    print(id)
    data =  Cohort.objects.filter(id=id)
    data.delete()
    return redirect('/cohort/'+str(cohort))

def deletefile(requests,id,cohort):
    data =  Cohortpdfs.objects.filter(id=id)
    data.delete()
    return redirect("/cohort/"+str(cohort))




def cohort(requests,id):
    data =  Cohort.objects.filter(id=id).values()
    subdata =  sub = Subcohort.objects.select_related('cohort_id').filter(parent_id=id).filter(~Q(cohort_id=id))

    room2 = Userdata.objects.filter(email=requests.user.email).values()
    
    #print(data:d)
    content=CohortpdfsForm()

    if requests.method == 'POST':  
        initialvalue={
            'cohort_id':id,
            'title':requests.POST.get('title'),
        }
        contentform = CohortpdfsForm(initialvalue)


        if contentform.is_valid():  
            if(requests.FILES['file'].name.endswith('pdf')):
                contentform.save()
                fileid=Cohortpdfs.objects.latest('id').id
                handle_uploaded_file(requests.FILES['file'],fileid)  
                print("File uploaded")
        else:
            print("FORM ERROR")
            print(content.errors)
            print(content.non_field_errors)

    contents = Cohortpdfs.objects.filter(cohort_id_id=id).order_by('-id').values()
    
    
    context = {'cohort':data,'subcohort':subdata,'content':content,'dbuser':room2,'files':contents,'cohortid':id,'pageid':id}
    return render(requests,'cohortviewer.html',context)


def test(requests):
    return render(requests,'test.html')

def pdfviewer(requests,id):
    print("yoyo")
    data=Cohortpdfs.objects.filter(id=id).values()
    context = {'pdfdata':data}
    return render(requests,'pdfview.html',context)

def assign(requests,id):
    cohorts=Cohort.objects.filter(~Q(title="Origin")).values()
    students=Userdata.objects.filter(userrole='student')
    myrole=str(Userdata.objects.filter(email=requests.user.email)[0].userrole)
    print(myrole)

    if requests.method == "POST":
        idcohort=(requests.POST.get('idcohort'))
        addstudent=(requests.POST.get('addstudent'))
        initialvalue={
            'cohort':idcohort,
            'email':addstudent,
        }
        contentform = CohortstudentForm(initialvalue)

        if contentform.is_valid():
            if len(Cohortstudent.objects.filter(cohort=idcohort,email=addstudent)) == 0:
                contentform.save()
            return redirect('/cohort/'+str(id))
        else:
            print("form error <-")

    return render(requests,'assign.html',context={'cohorts':cohorts,'students':students,'myrole':myrole,})

def viewstudents(requests,id):
    currentstudents = []
    data=Cohortstudent.objects.filter(cohort=id)

    for i in data:
        currentstudents.append(str(i.email))
    
    print(currentstudents)

    data2=Userdata.objects.filter(email__in=currentstudents)
    title=Cohort.objects.filter(id=id)[0].title


    return render(requests,'viewstudents.html',context={'students':data2,'cohort':title,'idcohort':id,'useremail':requests.user.email})


def removestudent(requests,idcohort,useremail):
    student=Cohortstudent.objects.filter(cohort=idcohort).filter(email=useremail)
    student.delete()
    return redirect('/students/'+str(idcohort))
    return HttpResponse("yo")


def trackface(requests,pdf):
    facerecognition.recognizeFace(requests.user.email,pdf)
    #return redirect('/')
    return HttpResponse("go home")



def setquestion(requests,fileid,cohortid):

    if requests.method=="POST":

        if 'textqnsubmit' in requests.POST:
            
            textqn=requests.POST.get('textques')
            textans=requests.POST.get('textans')
            Question.objects.create(type="cq",cohort=Cohort.objects.get(id=cohortid),source=fileid)
            qnid = Question.objects.latest('id').id
            Cq.objects.create(question=Question.objects.get(id=qnid),question_title=textqn,correct_answer=textans)


        elif 'mcqsubmit' in requests.POST:
            mcqques=requests.POST.get('mcqques')
            mcqop1=requests.POST.get('mcqop1')
            mcqop2=requests.POST.get('mcqop2')
            mcqop3=requests.POST.get('mcqop3')
            mcqop4=requests.POST.get('mcqop4')
            mcqans=requests.POST.get('mcqans')
            
            Question.objects.create(type="mcq",cohort=Cohort.objects.get(id=cohortid),source=fileid)
            qnid = Question.objects.latest('id').id
            Mcq.objects.create(question=Question.objects.get(id=qnid),question_title=mcqques,option1=mcqop1,option2=mcqop2,option3=mcqop3,option4=mcqop4,correct_answer=mcqans)

        elif 'publishqn' in requests.POST:
            pdfddata = Cohortpdfs.objects.get(id=fileid)
            pdfddata.qn_published=True
            pdfddata.save()


    data=Cohortpdfs.objects.filter(id=fileid).values()
    

    cqs = Question.objects.prefetch_related(Prefetch('cq_set',  to_attr='allcqques')).filter(source=fileid).filter(type="cq")
    mcqs =  Question.objects.prefetch_related(Prefetch('mcq_set',  to_attr='allmcqs')).filter(source=fileid).filter(type="mcq")
    
    cq = []
    mcq = []

    for i in cqs:
        #print(i.allcqques[0].question_title)
        cq.append({'qnid':i.allcqques[0].question_id,'qntitle':i.allcqques[0].question_title})
    


    for i in mcqs:
        #print(i.allmcqs[0].question_title)
        mcq.append({'qnid':i.allmcqs[0].question_id,'qntitle':i.allmcqs[0].question_title,'op1':i.allmcqs[0].option1,'op2':i.allmcqs[0].option2,'op3':i.allmcqs[0].option3,'op4':i.allmcqs[0].option4})
         



    context = {'pdfdata':data,'cq':cq,'mcq':mcq}
    return render(requests,'setquestion.html',context)



def deleteqn(requests,id):
    x = Question.objects.get(id=id)
    x.delete()
    return HttpResponseRedirect(requests.META.get('HTTP_REFERER', '/'))


def monitorstudent(requests,fileid,cohortid):
    data = readattempt.objects.all().values()
    context = {'data':data}
    return render(requests,'monitorstudent.html',context)


def showchart(requests,id):
    data = readattempt.objects.filter(id=id)
    total = data[0].total
    good = data[0].onscreen
    bad=total-good
    context = {'data':data.values(),'good':int(good),'bad':int(bad)}

    print(good,bad)
    return render(requests,'showchart.html',context)



def examhall(requests,fileid):

       
    if requests.method != 'POST':
        if quizattempt.objects.filter(email=requests.user.email).filter(source=fileid).count()>0:
            return HttpResponse("<div style='box-shadow:2px 2px 5px grey;'><br><br><h1 style='margin-left:35%;'>You have already submitted this quiz!</h1><br><br><a href='../dashboard' style='margin-left:45%; text-decoration: none; font-size:25px '>Go Home</a><br><br></div>")
        else:
            user=Userdata.objects.get(email=requests.user.email)
            quizattempt.objects.create(email=user,source=fileid,starttime=time.time())
    

    context = {}
    questions = Question.objects.filter(source=fileid)

    cq = Cq.objects.filter(question__source=fileid)
    mcq = Mcq.objects.filter(question__source=fileid)
    context['cq']=cq.values()
    context['mcq']=mcq.values()

    QUIZTIME=30

    if requests.method=="POST":
        starttime = quizattempt.objects.filter(email=requests.user.email)[0].starttime

        if (time.time()-starttime)>QUIZTIME:
            Result.objects.create(email=Userdata.objects.get(email=requests.user.email),point=0,source=fileid)
            return HttpResponse("<div style='box-shadow:2px 2px 5px grey;'><br><br><h1 style='margin-left:35%;'>Sorry the time is over. Your response is not recorded!</h1><br><br><h1 style='margin-left:35%;'>Congrats! You got 0 Marks! :) </h1><br><br><a href='../dashboard' style='margin-left:45%; text-decoration: none; font-size:25px '>Go Home</a><br><br></div>")

        for i in questions:
            ans = requests.POST.get(str(i.id))

            Answer.objects.create(question=Question.objects.get(id=i.id),email=Userdata.objects.get(email=requests.user.email),studentans=ans,source=fileid)

        #Here we start evaluating the exam paper:

        queryset=Answer.objects.filter(email=requests.user.email).filter(source=fileid)

        for j in queryset:
            point=0
            correct_answer=""
            questionId=j.question_id
            student_ans=j.studentans
            
            
            
            question=Question.objects.get(id=questionId)
            type=question.type

            if type=="mcq":
                correct_answer=Mcq.objects.get(question_id=questionId).correct_answer
            else:
                correct_answer=Cq.objects.get(question_id=questionId).correct_answer

            if str(correct_answer).lower()==str(student_ans).lower():
                point=1

            Evaluate.objects.create(question=Question.objects.get(id=questionId),email=Userdata.objects.get(email=requests.user.email),point=point,source=fileid)


        #Evaluation ends
        #Calculating total point

            
        queryset = Evaluate.objects.filter(email=requests.user.email).filter(source=fileid)
        count=0
        for i in queryset:
            count=count+int(i.point)

        
        Result.objects.create(email=Userdata.objects.get(email=requests.user.email),point=count,source=fileid)


        return HttpResponse("<div style='box-shadow:2px 2px 5px grey;'><br><br><h1 style='margin-left:40%;'>You got <strong style='color:red;'> "+ str(count) + "</strong> Marks!</h1><br><br><a href='../dashboard' style='margin-left:45%; text-decoration: none; font-size:25px '>Go Home</a><br><br></div>")


        return redirect('/dashboard/')


    return render(requests,'examhall.html',context)




def results(requests,fileid,cohortid):

    context= {}
    
    data = Result.objects.filter(source=fileid)
    
    results= []

    for i in data:
        
        x = {}
        y=Userdata.objects.filter(email=i.email)[0]

        name= y.first_name + y.last_name

        x['name']=name
        x['point']=i.point

        results.append(x)

    context['result']=results

    return render(requests,'results.html',context)