from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
from datetime import date
from django.db.models import Q
from django.contrib import messages
from django.db.models import Count
from datetime import datetime

import json


# Create your views here.

def index(request):
    return render(request,'index.html')

def admin_signup(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if the password and confirm password match
        if password != confirm_password:
            error = "Passwords do not match"
        else:
            try:
                # Create the user if passwords match
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully!')
                return redirect('admin_login')  # Redirect to the login page after sign-up
            except Exception as e:
                error = f"Error: {str(e)}"  # Provide a clear error message

    return render(request, 'admin_signup.html', {'error': error})

# def admin_login(request):
#     error = ""
#     if request.method == 'POST':
#         u = request.POST['uname']
#         p = request.POST['pwd']
#         user = authenticate(username=u, password=p)
#         try:
#             if user.is_staff:
#                 login(request, user)
#                 error = "no"
#             else:
#                 error = "yes"
#         except:
#             error = "yes"
#     return render(request,'admin_login.html', locals())
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pwd']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User exists and credentials are correct
            
            # Set the user as staff if they are not already
            if not user.is_staff:
                user.is_staff = True
                user.save()  # Save the changes to the user
            
            login(request, user)  # Log the user in
            messages.success(request, "Logged in successfully!")
            print("Redirecting to admin_home...")
            return redirect('admin_home')  # Redirect to admin home
            
        else:
            # Invalid credentials
            messages.error(request, "Invalid Credentials, Please Try Again")
            return redirect('admin_login')
    
    return render(request, 'admin_login.html')




def admin_home(request):
  
    if not request.user.is_staff:
        return redirect('admin_login')

   
    en = Enquiry.objects.all().count()
    eq = Equipment.objects.all().count()
    p = Plan.objects.all().count()

   
    members = Member.objects.all()
    m = members.count()

    
    statisticData = dict()

    
    for member in members:
       
        date_str = member.joindate.strftime('%m/%d/%Y')
       
        statisticData[date_str] = statisticData.get(date_str, 0) + 1
        chartData = {
            datetime.strptime(k, '%m/%d/%Y').strftime('%Y-%m-%d'): v
            for k, v in sorted(statisticData.items(), key=lambda x: datetime.strptime(x[0], '%m/%d/%Y'))
        }
        
    context = {
        'en': en,
        'eq': eq,
        'p': p,
        'm': m,
        "s": json.dumps(chartData)
    }

    print(context)
    return render(request, 'admin_home.html', context)
def contact(request):
    error = ""
    if request.method == 'POST':
        n = request.POST['name']
        e = request.POST['emailid']
        c = request.POST['contact']
        s = request.POST['subject']
        m = request.POST['message']
        try:
            Contact.objects.create(name=n, emailid=e, contact=c, subject=s, message=m, msgdate=date.today(),
                                   isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request,'contact.html', locals())

def addEnquiry(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    error = ""
    if request.method == "POST":
        n = request.POST['name']
        m = request.POST['mobile']
        e = request.POST['email']
        a = request.POST['age']
        g = request.POST['gender']
        try:
            Enquiry.objects.create(name=n, mobile=m, email=e, age=a, gender=g)
            error = "no"
        except:
            error = "yes"
    return render(request,'addEnquiry.html', locals())

def viewEnquiry(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    enquiry = Enquiry.objects.all()
    return render(request,'viewEnquiry.html', locals())

def edit_Enquiry(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect(admin_login)
    user = request.user
    enquiry = Enquiry.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        m1 = request.POST['mobile']
        e1 = request.POST['email']
        a1 = request.POST['age']
        g1 = request.POST['gender']

        enquiry.name = n1
        enquiry.mobile = m1
        enquiry.email = e1
        enquiry.age = a1
        enquiry.gender = g1
        try:
            enquiry.save()
            error = "no"
        except:
            error = "yes"
    return render(request,'edit_Enquiry.html', locals())

def delete_Enquiry(request,pid):
    enquiry = Enquiry.objects.get(id=pid)
    enquiry.delete()
    return redirect('viewEnquiry')

def addPlan(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    error = ""
    if request.method == "POST":
        p = request.POST['name']
        a = request.POST['amount']
        d = request.POST['duration']
        try:
            Plan.objects.create(name=p, amount=a, duration=d)
            error = "no"
        except:
            error = "yes"
    return render(request,'addPlan.html', locals())

def viewPlan(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    plan = Plan.objects.all()
    return render(request,'viewPlan.html', locals())

def edit_Plan(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect(admin_login)
    user = request.user
    plan = Plan.objects.get(id=pid)
    if request.method == "POST":
        p1 = request.POST['name']
        a1 = request.POST['amount']
        d1 = request.POST['duration']

        plan.name = p1
        plan.amount = a1
        plan.duration = d1
        try:
            plan.save()
            error = "no"
        except:
            error = "yes"
    return render(request,'edit_Plan.html', locals())

def delete_Plan(request,pid):
    plan = Plan.objects.get(id=pid)
    plan.delete()
    return redirect('viewPlan')

def addEquipment(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    error = ""
    if request.method == "POST":
        n = request.POST['name']
        p = request.POST['price']
        u = request.POST['unit']
        pd = request.POST['purchasedate']
        d = request.POST['description']

        try:
            Equipment.objects.create(name=n, price=p, unit=u, purchasedate=pd, description=d)
            error = "no"
        except:
            error = "yes"
    return render(request,'addEquipment.html', locals())

def viewEquipment(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    equipment = Equipment.objects.all()
    return render(request,'viewEquipment.html', locals())

def edit_Equipment(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect(admin_login)
    user = request.user
    equipment = Equipment.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        p1 = request.POST['price']
        u1 = request.POST['unit']
        d1 = request.POST['description']

        equipment.name = n1
        equipment.price = p1
        equipment.unit = u1
        equipment.description = d1
        try:
            equipment.save()
            error = "no"
        except:
            error = "yes"
    return render(request,'edit_Equipment.html', locals())

def delete_Equipment(request,pid):
    equipment = Equipment.objects.get(id=pid)
    equipment.delete()
    return redirect('viewEquipment')

def addMember(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    error = ""
    plan1 = Plan.objects.all()
    if request.method == "POST":
        n = request.POST['name']
        c = request.POST['contact']
        e = request.POST['email']
        g = request.POST['gender']
        p = request.POST['plan']
        j = request.POST['joindate']
        i = request.POST['initamount']
        plan = Plan.objects.get(name=p)
        try:
            Member.objects.create(name=n, contact=c, email=e, gender=g, plan=plan, joindate=j, initamount=i)
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'plan':plan1}
    return render(request,'addMember.html', d)

def viewMember(request):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    member = Member.objects.all()
    return render(request,'viewMember.html', locals())

def edit_Member(request,pid):
    if not request.user.is_authenticated:
        return redirect(admin_login)
    error = ""
    user = request.user
    member = Member.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        c1 = request.POST['contact']
        e1 = request.POST['email']
        g1 = request.POST['gender']
        i1 = request.POST['initamount']

        member.name = n1
        member.contact = c1
        member.email = e1
        member.gender = g1
        member.initamount = i1
        try:
            member.save()
            error = "no"
        except:
            error = "yes"
    return render(request,'edit_Member.html', locals())

def delete_Member(request,pid):
    member = Member.objects.get(id=pid)
    member.delete()
    return redirect('viewMember')

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html', locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact = Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html', locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())

def delete_contact(request,pid):
    contact = Contact.objects.get(id=pid)
    contact.delete()
    return redirect('read_queries')

def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request,'changePassword.html', locals())


def logout_view(request):
    logout(request)
    return redirect('admin_signup.html') 

