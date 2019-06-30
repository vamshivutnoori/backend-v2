from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from .models import Products, Subscribers
from django.contrib.sites.shortcuts import get_current_site
import csv, io
from background_task import background
from django.core.mail import EmailMessage
import os
# Create your views here.
from urllib import request
import datetime
from .forms import UserRegistrationForm


from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
url='https://cve.mitre.org/data/downloads/allitems.csv'

    

@background(schedule=60000)
def hello():
	start = datetime.datetime.now()
	response = request.urlopen(url)
	csv = response.read()
	csv_str = str(csv)
	lines = csv_str.split("\\n")
	dest_url=r'C:\Users\rishith\Desktop\Patch-Remainder-master\backend\mysite\core\new.csv'
	fx = open(dest_url,"w")
	for line in lines:
		fx.write(line + "\n")
	fx.close()
	print("Download complete")
	with open(r'C:\Users\rishith\Desktop\Patch-remainder-master\backend\mysite\core\old.csv', 'r',encoding="utf8", errors='ignore') as t1, open(r'C:\Users\rishith\Desktop\Patch-Remainder-master\backend\mysite\core\new.csv', 'r', encoding="utf8", errors='ignore') as t2:
		fileone = t1.readlines()
		filetwo = t2.readlines()
	print("Reading Complete")
	with open(r'C:\Users\rishith\Desktop\Patch-remainder-master\backend\mysite\core\update.csv', 'w', encoding="utf8", errors='ignore') as outFile:
		for line in filetwo:
			if line not in fileone:
				outFile.write(line)
	print("Update Complete")
	#os.remove(r'C:\Users\rishith\Desktop\Patch-remainder-master\backend\mysite\core\old.csv')
	#os.rename(r'C:\Users\rishith\Desktop\Patch-remainder-master\backend\mysite\core\new.csv', r'C:\Users\rishith\Desktop\Patch-remainder-master\backend\mysite\core\old.csv')
	messages = []
	with open('mysite/core/update.csv','rt')as f:
		data = f.readlines()
	#print(data)
	for user in User.objects.all():
		#recievers.append(user.email)
		id = user.id
		try:
			
			s = Subscribers.objects.get(user_id=user.id)
			
			sb=s.subscriptions
			sb = sb.split(",")
			#print(sb)
			ma = list()
			#print("LOL")
			for row in data:
				#print(row)
				row = row.split(",")
				for sub in sb:
					#row = ",".join(row)
					#print(row[2], sub)
					if sub in row[2]:
						#print(sub)
						ma.append(str(row[0]))
			
			msg = "\n".join(ma)
			#print(len(msg))
			reciever = []
			if len(msg)!=0:
				reciever = [user.email]
			print(reciever)
			try:
				subject = "CVE asdasdaa"
				message = msg
				email = EmailMessage(subject, message, to=reciever)
				email.send()
				success = True
			except Exception as e:
				print("Unable to send email to (%s)\n%s" % ('rishi.gandham2998@gmail.com', e))
			print("Hello World!")
			os.remove(r'C:\Users\rishith\Desktop\Patch-remainder-master\backend\mysite\core\update.csv')
			end = datetime.datetime.now()
			print(end -start)
		except:
			pass
	
#import requests
def home(request):
	#count = User.objects.count()
	#return render(request, 'home.html',
	#	{'count' : count} ),
	return render(request,'home.html')

def signup(request):
	if request.method=='POST':
		form=UserRegistrationForm(request.POST)
		if form.is_valid():
			save_it = form.save(commit=False)
			save_it.is_active = False
			save_it.save()
			
			current_site=get_current_site(request)
			reciever=[save_it.email]
			subject='Thanks for Registering to patch remainder'
			message = render_to_string('acc_active_email.html', {
                'user': save_it,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(save_it.pk)),
                'token':account_activation_token.make_token(save_it),
            })
			email=EmailMessage(subject,message,to=reciever)
			email.send()
			success = True
			return render(request,'confirm.html')
			#user.is_active = False
			#user.save()            

	else:
		form = UserRegistrationForm()
	return render(request,
		'registration/signup.html',
		{'form':form}
		) 



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



def send_account_activation_email(request, user):
    text_content = 'Account Activation Email'
    subject = 'Email Activation'
    template_name = "emails/account/activation.html"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = [user.email]
    kwargs = {
        "uidb64": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        "token": default_token_generator.make_token(user)
    }
    activation_url = reverse("app:activate_user_account", kwargs=kwargs)

    activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)

    context = {
        'user': user,
        'activate_url': activate_url
    }
    html_content = render_to_string(template_name, context)
    email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
    email.attach_alternative(html_content, "text/html")
    email.send()




def activate_user_account(request, uidb64=None, token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('hr:user_profile')
    else:
        return HttpResponse("Activation link has expired")


@login_required
def direct_sub(request):
	return render(request,"manual.html")
@login_required	
def add_prod(request):
	subscriptions= request.POST["productz"]
	s = Subscribers.objects.get(user_id=request.user.id)
	sb=s.subscriptions
	sb+=","
	sb+=subscriptions
	sub, created = Subscribers.objects.get_or_create(user_id=request.user.id)
	sub.subscriptions = sb  # change field
	sub.save()


	'''prod_info=Subscribers(subscriptions=prod_add)
	prod_info.user = request.user
	prod_info.save()'''
	return render(request,"manual.html")

@login_required
def products(request):
	if request.method == "POST":
		subscriptions = request.POST.getlist("product[]", "")
		s = Subscribers.objects.get(user_id=request.user.id)
		sb=s.subscriptions
		sb+=","
		for sub in subscriptions:
			w=sb.find(sub)
			print(w)
			if w==-1:
				sb+=sub
				sb+=","
		
		sb = sb[:-1]
		sub, created = Subscribers.objects.get_or_create(user_id=request.user.id)
		sub.subscriptions = sb  # change field
		sub.save() # this will update only
   # person just refers to the existing one
		
	
	query_results = Products.objects.all()
	context= {'products': query_results}

	return render(request,'products.html', context)
@login_required
def subscriptions(request):
	if request.method == "POST":
		subscriptions = request.POST.getlist("subscriptions[]", "")
		print(subscriptions)
		s =Subscribers.objects.get(user_id=request.user.id)
		print(s)
		subs = s.subscriptions
		for sub in subscriptions:
			subs = s.subscriptions
			print(subs, sub)
			print(subs.find(sub))
			if(subs.find(sub)+len(sub)==len(subs)):
				subs = subs.replace(","+sub,"")
			else:
				subs = subs.replace(sub+",","")
			print(subs, sub)
			s.subscriptions = subs
		s.save()
		
	#		s+=sub
	#		s+=","
	#	s = s[:-1]
	sub= Subscribers.objects.get(user_id=request.user.id)
	a=sub.subscriptions.split(",")
	context={'subscriptions': a}
	return render(request,'subscrip.html',context)
	
	#	sub.subscriptions = s  # change field
	#	sub.save() # this will update only
   # person just refers to the existing one
		
		
	#query_results = Products.objects.all()
	#context= {'products': query_results}

	return render(request,'subscrip.html')
@login_required
def secret_page(request):
	return render(request,'secret_page.html')


def cvesearch(request):
	return render(request,'cve.html')

def output(request):
	#data=requests.get("https://reqres.in/api/users")
	#data=data.text
	#data="mama"
	#return HttpResponse(data)
	s = Subscribers.objects.get(user_id=request.user.id)
	sb=s.subscriptions
	sb = sb.split(",")
	print(sb)
	l=list()
	ma = list()
	with open('mysite/core/update.csv','rt')as f:
		data = csv.reader(f)
		for row in data:
			for sub in sb:
				#row = ",".join(row)
				print(row[2], sub)
				if sub in row[2]:
					print(sub)
					ma.append(str(row[0]))
					l.append(str(row))
	
	msg = "\n".join(ma)
	recievers = []
	for user in User.objects.all():
		recievers.append(user.email)
	try:
		subject = "CVE details"
		message = msg
		email = EmailMessage(subject, message, to=recievers)
		email.send()
		success = True
	except Exception as e:
		print("Unable to send email to (%s)\n%s" % ('rishi.gandham2998@gmail.com', e))
	return HttpResponse((l))

