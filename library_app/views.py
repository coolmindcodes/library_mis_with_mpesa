import json
import os
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.expressions import result
from django.db.models.functions import TruncMonth
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from library_app.app_forms import LoginForm
from library_app.models import Book, Student, Borrow, FinePayment

@login_required
# Create your views here.
def testing(request):
    # book1 = Book.objects.create(title="Introduction to Statistics", author="Tom Juma", year=1999, subject="Maths", isbn="123456")
    # book1.save()
    #
    # book2 = Book.objects.create(title="Introduction to Computers", author="Charles John", year=2009, subject="Maths", isbn="123457")
    # book2.save()
    #
    # student1 = Student.objects.create(name="Hellen Jane", phone="0723740215", email="hellen@gmail.com", admission_no="K001")
    # student2 = Student.objects.create(name="Krishna Jolie", phone="0723740216", email="jollie@gmail.com", admission_no="K002")
    # student1.save()
    # student2.save()

    # book = get_object_or_404(Book, pk=1)
    # student = get_object_or_404(Student, pk=1)
    # expected_return_date = date.today() +  timedelta(days=7)
    #
    # borrow = Borrow.objects.create(book=book, student=student, status='BORROWED', expected_return_date=expected_return_date)
    # borrow.save()

    # returned_borrow = get_object_or_404(Borrow, pk=1)
    # returned_borrow.return_date = date.today()
    # returned_borrow.status = 'RETURNED'
    #
    # if date.today() > returned_borrow.expected_return_date:
    #    days = abs(date.today() - returned_borrow.expected_return_date).days
    #    fine = days * 50
    #    returned_borrow.fine = fine
    # returned_borrow.save()
    borrowings = Borrow.objects.filter(status='BORROWED')
    print(borrowings)
    return render(request, 'index.html')

@login_required
def index(request):
    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})

@login_required
def issue(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    students = Student.objects.all()
    if request.method == 'GET':
        return render(request, 'borrow.html', {'book': book, 'students': students})
    elif request.method == 'POST':
        student_id = request.POST['student']
        student = Student.objects.get(pk=int(student_id))
        expected_return_date = date.today() + timedelta(days=7)
        borrow = Borrow.objects.create(book=book, student=student, status='BORROWED',
                                       expected_return_date=expected_return_date)
        borrow.save()
        return redirect('home')
    return render(request, 'borrow.html', {'book': book, 'students': students})

@login_required
def borrowed_books(request):
    borrowed_items = Borrow.objects.filter(status='BORROWED')
    return render(request, 'borrowed_books.html', {'borrowed_items': borrowed_items})

@login_required
def return_item(request, borrowed_id):
    returned_borrow = get_object_or_404(Borrow, pk=borrowed_id)
    returned_borrow.return_date = date.today()
    returned_borrow.status = 'RETURNED'
    if date.today() > returned_borrow.expected_return_date:
        days = abs(date.today() - returned_borrow.expected_return_date).days
        fine = days * 10
        returned_borrow.fine = fine
    returned_borrow.save()
    messages.success(request,
                     f'{returned_borrow.book.title} by {returned_borrow.book.author} was returned successfully')
    return redirect('borrowed_books')

@login_required
def dashboard(request):
    return render(request, 'stats.html')

@login_required
def pie_chart_data(request):
    books = Borrow.objects.filter(created_at__year=2024)
    returned = books.filter(status='RETURNED').count()
    borrowed = books.filter(status='BORROWED').count()
    lost = books.filter(status='LOST').count()

    return JsonResponse({
        "title": f"Books Stats",
        "data": {
            "labels": ["Returned", "Borrowed", "Lost"],
            "datasets": [{
                "label": "Count",
                "backgroundColor": ["#55efc4", "#ff7675"],
                "borderColor": ["#55efc4", "#ff7675"],
                "data": [
                    200, 155, 35
                ],
            }]
        },
    })

@login_required
def area_chart_data(request):
    books = Borrow.objects.filter(created_at__year=2024)
    grouped_stats = (books.annotate(month=TruncMonth('created_at')).values('month')
                     .annotate(num_borrows=Count('id'))
                     .order_by('month'))
    counts = []
    for item in grouped_stats:
        item['month'] = item['month'].strftime('%B')
        print(item['month'], " ", item['num_borrows'])
        counts.append(item['num_borrows'])

    return JsonResponse({
        "title": f"Monthly Books Stats",
        "data": {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "datasets": [{
                "label": "Borrowings",
                "lineTension": 0.3,
                "backgroundColor": "rgba(78, 115, 223, 0.05)",
                "borderColor": "rgba(78, 115, 223, 1)",
                "pointRadius": 3,
                "pointBackgroundColor": "rgba(78, 115, 223, 1)",
                "pointBorderColor": "rgba(78, 115, 223, 1)",
                "pointHoverRadius": 3,
                "pointHoverBackgroundColor": "rgba(78, 115, 223, 1)",
                "pointHoverBorderColor": "rgba(78, 115, 223, 1)",
                "pointHitRadius": 10,
                "pointBorderWidth": 2,
                "data": counts,
            }]
        }
    })

@login_required
def bar_chart_data(request):
    books = Borrow.objects.filter(created_at__year=2024)
    grouped_stats = (books.annotate(month=TruncMonth('created_at')).values('month')
                     .annotate(num_borrows=Count('id'))
                     .order_by('month'))
    counts = []
    for item in grouped_stats:
        item['month'] = item['month'].strftime('%B')
        counts.append(item['num_borrows'])

    return JsonResponse({
        "title": "Monthly Books Statistics",
        "data": {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "datasets": [
                {
                    "label": "Items Borrowed",
                    "backgroundColor": "#4e73df",
                    "hoverBackgroundColor": "#2e59d9",
                    "borderColor": "#4e73df",
                    "data": counts,
                }]
        }
    })

@login_required
def pay_fine(request, id):
    item = Borrow.objects.get(pk=id)
    total = item.fine_total
    phone = item.student.phone
    cl = MpesaClient()
    phone_number = '0723740215' #phone
    amount = 1 #total
    account_reference = item.student.admission_no
    transaction_desc = 'Book-Fine'
    callback_url = 'https://mature-octopus-causal.ngrok-free.app/callback'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    print(response.response_code,response.checkout_request_id)
    if response.response_code == "0":
       payment = FinePayment.objects.create(borrow=item,merchant_request_id=response.merchant_request_id, checkout_request_id= response.checkout_request_id,amount=amount)
       payment.save()
       messages.success(request, f'M-PESA payment initiated successfully for account {account_reference}')
    return redirect('returns')
@login_required
def returns(request):
    borrowed_items = Borrow.objects.filter(status__icontains='Returned')
    return render(request, 'returns.html', {'borrowed_items': borrowed_items})


# ngrok http --url=mature-octopus-causal.ngrok-free.app 8000
@csrf_exempt
def callback(request):
    resp = json.loads(request.body)
    data = resp['Body']['stkCallback']
    merchant_request_id = data['MerchantRequestID']
    checkout_request_id = data['CheckoutRequestID']
    result_code = data['ResultCode']
    if result_code == "0":
        payment = FinePayment.objects.get(merchant_request_id=merchant_request_id, checkout_request_id=checkout_request_id)
        if payment:
            payment.status = "COMPLETED"
            payment.save()
    return HttpResponse("OK")



def login_user(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user) # sessions # cookies
                return redirect('dashboard')
        messages.error(request, "Invalid username or password")
        return render(request, "login.html", {"form": form})

@login_required
def signout_user(request):
    logout(request)
    return redirect('login')