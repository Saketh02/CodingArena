from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from qeval.models import c_questiondetails
from qeval.models import java_questiondetails
from qeval.models import py_questiondetails
import re
import requests

# Create your views here.
def login(request):
    if request.method=="POST":
        username=request.POST['your-name']
        password=request.POST['your-email']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'index1.html')
        else:
            messages.info(request,'Invalid credintials')
            return redirect('/')    
def index1(request):
    if request.user.is_authenticated:
        return render(request,'index1.html')   
    else:
        return render(request,'error.html')         
def contact(request):
    if request.user.is_authenticated:
        return render(request,'contact.html')   
    else:
        return render(request,'error.html')         
def leader(request):
    if request.user.is_authenticated:
        return render(request,'leader.html')   
    else:
        return render(request,'error.html')             
def c(request):
    if request.user.is_authenticated:
        row=c_questiondetails.objects.all()
        return render(request,'c.html',{'name':row})   
    else:
        return render(request,'error.html')         
def java(request):
    if request.user.is_authenticated:
        row=java_questiondetails.objects.all()
        return render(request,'java.html',{'name':row})   
    else:
        return render(request,'error.html')          
def python(request):
    if request.user.is_authenticated:
        row=py_questiondetails.objects.all()
        return render(request,'python.html',{'name':row})   
    else:
        return render(request,'error.html')              
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)  
        return redirect('/')
def register(request):
    if request.method=='POST':
        name=request.POST['your-name']
        email=request.POST['your-email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=name).exists():
                 messages.success(request,'User exists')  
            elif User.objects.filter(email=email).exists():
                 messages.success(request,'Email taken')
            else:
                user=User.objects.create_user(username=name,password=password1,email=email)
                user.save();
                messages.success(request,'User registration successful')
                             
        else:    
             messages.success(request,'Passwords not matching')
        return redirect('/')    
    else:    
        return render(request,'/')
                
def RUN(request):
    if request.method=="POST" and "btnrun" in request.POST:
        qid=int(request.POST['QuestionID'])
        code=request.POST['mycode']
        inputs=request.POST['input-code']
        
        url="https://tpcg.tutorialspoint.com/tpcg.php"
        data={
	    'lang': 'python3',
	    'device': '',
	    'code': code,
	    'stdinput':inputs,
	    'ext': 'py',
	    'compile': 0,
	    'execute': 'python3 main.py',
	    'mainfile': 'main.py',
	    'uid': '154567',
        }
        r=requests.post(url,data=data)
        content=r.text
        
        stripped = re.sub('<[^<]+?>', '', content)
        #stripped=stripped[425:]
        s='$python3 main.py'
        if s in stripped:
            stripped=stripped[len(s):]
        row1=py_questiondetails.objects.raw('SELECT id,t1,o1 FROM public.qeval_py_questiondetails')[qid-1]
        return render(request,'new.htm',{'name':stripped,'code':code,'question':row1.question,'input':row1.t1,'output':row1.o1,'i_format':row1.input_format,'o_format':row1.output_format}) 
    elif request.method=="POST" and "btneval" in request.POST:
        id=int(request.POST['QuestionID'])
        
        row1=py_questiondetails.objects.raw('SELECT id,t1,o1 FROM public.qeval_py_questiondetails')[id-1]
        inp=[]
        out=[]
        inp.append(row1.t1)
        inp.append(row1.t2)
        inp.append(row1.t3)
        inp.append(row1.t4)
        inp.append(row1.t5)
        inp.append(row1.t6)
        inp.append(row1.t7)
        inp.append(row1.t8)
        inp.append(row1.t9)
        inp.append(row1.t10)
        out.append(row1.o1)
        out.append(row1.o2)
        out.append(row1.o3)
        out.append(row1.o4)
        out.append(row1.o5)
        out.append(row1.o6)
        out.append(row1.o7)
        out.append(row1.o8)
        out.append(row1.o9)
        out.append(row1.o10)
        qid=int(request.POST['QuestionID'])
        code=request.POST['mycode']
        count=0
         
        for i in range(0,10):
            ins=inp[i]
            if '\r\n' in ins:
                ins=re.sub('\r\n','\n',ins)
            else:
                ins=ins+'\n'
            url="https://tpcg.tutorialspoint.com/tpcg.php"
            data={
	        'lang': 'python3',
	        'device': '',
	        'code': code,
	        'stdinput':ins,
	        'ext': 'py',
	        'compile': 0,
	        'execute': 'python3 main.py',
	        'mainfile': 'main.py',
	        'uid': '154567',
            }
            r=requests.post(url,data=data)
            content=r.text
            stripped = re.sub('<[^<]+?>', '', content)
            s='$python3 main.py'
            
            if '\r\n' in out[i]:
                out[i]=re.sub('\r\n','\n',out[i])
            else:
                out[i]=out[i]+'\n'    

            if s in stripped:
                stripped=stripped[len(s):]
            l=list(stripped) 
            k=list(out[i])   
            if stripped==out[i]:
                count+=10
        messages.info(request,"Your submission has got {} points!".format(count))   
        return render(request,'new.htm',{'code':code,'title':row1.title,'question':row1.question,'input':row1.t1,'output':row1.o1,'i_format':row1.input_format,'o_format':row1.output_format})   




def RUNJAVA(request):
    if request.method=="POST":
        qid=int(request.POST['QuestionID'])
        code=request.POST['mycode']
        inputs=request.POST['input-code']
        
        url="https://tpcg.tutorialspoint.com/tpcg.php"
        data={
	    'lang': 'java8',
	    'device': '',
	    'code': code,
	    'stdinput':inputs,
	    'ext': 'java',
	    'compile': 'javac',
	    'execute': 'java -Xmx128M -Xms16M',
	    'mainfile': 'HelloWorld.java',
	    'uid': 1704494,
        }
        r=requests.post(url,data=data)
        content=r.text
        stripped = re.sub('<[^<]+?>', '', content)
        stripped=stripped[425:]
        row1=py_questiondetails.objects.raw('SELECT id,t1,o1 FROM public.qeval_java_questiondetails')[qid-1]
        return render(request,"newinjava.htm",{'name':stripped,'code':code,'question':row1.question,'input':row1.t1,'output':row1.o1,'i_format':row1.input_format,'o_format':row1.output_format})
        
def RUNC(request):
    if request.method=="POST":
        qid=int(request.POST['QuestionID'])
        code=request.POST['mycode']
        inputs=request.POST['input-code']
        url="https://tpcg.tutorialspoint.com/tpcg.php"
        data={
	    'lang': 'c',
	    'device': '',
	    'code': code,
	    'stdinput':inputs,
	    'ext': 'c',
	    'compile': 'gcc -o main *.c',
	    'execute': 'main',
	    'mainfile': 'main.c',
	    'uid': 1704494,
        }
        r=requests.post(url,data=data)
        content=r.text
        stripped = re.sub('<[^<]+?>', '', content)
        stripped=stripped[425:]
        row1=py_questiondetails.objects.raw('SELECT id,t1,o1 FROM public.qeval_c_questiondetails')[qid-1]
        return render(request,"newinc.htm",{'name':stripped,'code':code,'question':row1.question,'input':row1.t1,'output':row1.o1,'i_format':row1.input_format,'o_format':row1.output_format})
         
        

def EVALUATE(request):
    pass
def HelloWorldinpy(request):
    if request.method=="POST":
        qid=int(request.POST['QuestionID'])
        row1=py_questiondetails.objects.raw('SELECT id,question FROM public.qeval_py_questiondetails')[qid-1]
        return render(request,'new.htm',{'qid':qid,'name1':row1.question,'question':row1.question,'input':row1.t1,'output':row1.o1,'i_format':row1.input_format,'o_format':row1.output_format}) 
def HelloWorldinjava(request):
    if request.method=="POST":
        qid=int(request.POST['QuestionID'])
        row1=java_questiondetails.objects.raw('SELECT id,question FROM public.qeval_java_questiondetails where id={qid}')[0]
        return render(request,'newinjava.htm',{'qid':qid,'name1':row1.question,'question':row1.question,'input':row1.t1,'output':row1.o1,'i_format':row1.input_format,'o_format':row1.output_format})  
def HelloWorldinc(request):  
    if request.method=="POST":
        qid=int(request.POST['QuestionID'])
        row1=c_questiondetails.objects.raw(f'SELECT id,question FROM public.qeval_c_questiondetails where id={qid}')[0]
        return render(request,'newinc.htm',{'qid':qid,'name1':row1.question,'question':row1.question,'input':row1.t1,'output':row1.o1,'i_format':row1.input_format,'o_format':row1.output_format}) 
