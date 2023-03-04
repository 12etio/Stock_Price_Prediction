from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse
from homepage import Stock_price_prediction
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import UserRequest
from .forms import StockRequestForm 
from django.contrib import messages
from datetime import date, datetime
from django.views.decorators.cache import cache_control
# from email import message
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.forms import AuthenticationForm
# from django.views.generic import CreateView
# from .forms import StudentSignUpForm, TeacherSignUpForm

symbols = ['TSLA', 'AAPL', 'AMZN', 'GOOG', 'MSFT', 'NVDA']

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def homepage(request):
    return render(request, "frontpage.html")

def tslaStock(request):
    stock_name = "Tesla"
    obj = Stock_price_prediction.StockPricePredictor('TSLA')
    obj.predict_future_price()
    context = {"stock_data": obj.context, "stock_name": stock_name, "current_data": obj.get_current_data}
    return render(request, 'getStock.html', context)

def aaplStock(request):
    stock_name = "Apple"
    obj = Stock_price_prediction.StockPricePredictor('AAPL')
    obj.predict_future_price()
    context = {"stock_data": obj.context, "stock_name": stock_name, "current_data": obj.get_current_data}
    return render(request, 'getStock.html', context)

def amznStock(request):
    stock_name = "Amazon"
    obj = Stock_price_prediction.StockPricePredictor('AMZN')
    obj.predict_future_price()
    context = {"stock_data": obj.context, "stock_name": stock_name, "current_data": obj.get_current_data}
    return render(request, 'getStock.html', context)

def googStock(request):
    stock_name = "Google"
    obj = Stock_price_prediction.StockPricePredictor('GOOG')
    obj.predict_future_price()
    context = {"stock_data": obj.context, "stock_name": stock_name, "current_data": obj.get_current_data}
    return render(request, 'getStock.html', context)

def msftStock(request):
    stock_name = "Microsoft"
    obj = Stock_price_prediction.StockPricePredictor('MSFT')
    obj.predict_future_price()
    context = {"stock_data": obj.context, "stock_name": stock_name, "current_data": obj.get_current_data}
    return render(request, 'getStock.html', context)

def nvdaStock(request):
    stock_name = "Nvidia"
    obj = Stock_price_prediction.StockPricePredictor('NVDA')
    obj.predict_future_price()
    context = {"stock_data": obj.context, "stock_name": stock_name, "current_data": obj.get_current_data}
    return render(request, 'getStock.html', context)



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect("http://127.0.0.1:8000/register/")
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect("http://127.0.0.1:8000/register/")
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save()
                
                return redirect('http://127.0.0.1:8000/login_user')


        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect("http://127.0.0.1:8000/register/")
            
    else:
        return render(request, 'registration.html')

def stock_request(request):
    if request.method == 'POST':
        symbol = request.POST["symbol"] 
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        num_epochs = request.POST["num_epochs"]
        batch_size = request.POST["batch_size"]
        
        if symbol not in symbols:
            if  datetime.strptime(start_date, r'20%y-%m-%d').date() < date(2018,1,1):
                messages.info(request, 'It is not advisable to go past 2018')
                return redirect("http://127.0.0.1:8000/stock_request/")
            elif  datetime.strptime(end_date, r'20%y-%m-%d').date() < date.today():
                messages.info(request, 'The lastest possible date is todays date')
                return redirect("http://127.0.0.1:8000/stock_request/")
            elif int(num_epochs) > 60:
                messages.info(request, 'Too many epochs may lead to overfitting')
                return redirect("http://127.0.0.1:8000/stock_request/")
            elif int(batch_size) > 16:
                messages.info(request, 'Batch size too large')
                return redirect("http://127.0.0.1:8000/stock_request/")
            else:
                user_request = UserRequest(symbol=symbol, start_date=start_date, end_date=end_date, num_epochs=num_epochs, batch_size=batch_size)
                user_request.user = request.user
                user_request.save()
                stock_name = symbol
                obj = Stock_price_prediction.StockPricePredictor(symbol, start_date, end_date, int(num_epochs), int(batch_size))
                obj._train_model()
                obj.predict_future_price()
                context = {"stock_data": obj.context, "stock_name": stock_name, "current_data": obj.get_current_data}
                return render(request, 'getStock.html', context)
                
        else:
            messages.info(request, 'Stock is already on website')
            return redirect("http://127.0.0.1:8000/stock_request/")
    else: 
        return render(request, 'stock_request.html')
       
        
        
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('http://127.0.0.1:8000/login_user/')



    else:
        return render(request, 'login.html')
    
def logout_user(request):
    auth.logout(request)
    return redirect('http://127.0.0.1:8000/')

# def my_form(request):
#   if request.method == "POST":
#     form = SignUpForm(request.POST)
#     if form.is_valid():
#       form.save()
#       return redirect('http://127.0.0.1:8000/')
#   else:
#       form = SignUpForm()
#   return render(request, 'form_test.html', {'form': form})

# def register(request):
#     return render(request, 'register.html')

# class student_register(CreateView):
#     model = User  
#     form_class = StudentSignUpForm
#     template_name= 'student_register.html'

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('http://127.0.0.1:8000/')

# class teacher_register(CreateView):
#     model = User  
#     form_class = TeacherSignUpForm
#     template_name= 'teacher_register.html'

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('http://127.0.0.1:8000/')

# def login_user(request):
#     if request.method=='POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None :
#                 login(request,user)
#                 return redirect('http://127.0.0.1:8000/')
#             else:
#                 messages.error(request,"Invalid username or password")
#         else:
#             messages.error(request,"Invalid username or password")
#     return render(request, 'login.html',context={'form':AuthenticationForm()})

# def logout_user(request):
#     logout(request)
#     return redirect('http://127.0.0.1:8000/')