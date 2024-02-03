from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm,AddRecordForm,UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from . models import Record
from django.db.models import Q

# Create your views here.


#Home

def home(request):
    
    return render(request,'index.html')


#Register

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)
         
        if form.is_valid():

            form.save()

            return redirect('login')


    context = {'form':form}
    return render(request, 'register.html',context=context)


#Login

def login(request):

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user is not None:
                auth.login(request,user)

                return redirect('dashboard')

    context = {'form2':form}

    return render(request,'login.html',context=context)


#Logout

def user_logout(request):
    auth.logout(request)

    return redirect('login')


#Dashboard

@login_required(login_url='login')
def dashboard(request):
    my_records = Record.objects.all()
    context = {'records':my_records}

    return render(request,'dashboard.html',context=context)


#Add Record
@login_required(login_url='login')
def create_record(request):
    form = AddRecordForm()

    if request.method == "POST":
        form = AddRecordForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('dashboard')
        
    context = {'form3':form}

    return render(request,'create-record.html',context=context)


#Update Record
@login_required(login_url='login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    
    context = {'form4':form}
    return render(request,'update-record.html',context=context)


#Read a singular record
@login_required(login_url='login')
def single_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record':all_records}
    print(context,"DEVEN")
    return render(request,'view-record.html',context=context)

#Delete record
@login_required(login_url='login')
def delete_record(request, pk):
    del_record = Record.objects.get(id=pk)
    del_record.delete()

    return redirect("dashboard")
 

#Search Fuctionality
@login_required(login_url='login')
def search_results(request):
    query = request.GET.get('q')
    print(f"Query: {query}")  # Add this line for debugging

    
    if query:
        results = Record.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(address__icontains=query) |
            Q(state__icontains=query) |
            Q(country__icontains=query) |
            Q(creation_date__icontains=query)
        )
    else:
        results = Record.objects.all()

    context = {'results': results, 'query': query}
    return render(request, 'search-results.html', context)



