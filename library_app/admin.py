from django.contrib import admin

from library_app.models import Student, Borrow, Book, FinePayment


# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone', 'admission_no']
    search_fields =  ['name','email','phone', 'admission_no']
    list_per_page = 25

class BooKAdmin(admin.ModelAdmin):
    list_display = ['title','author','year', 'subject', 'isbn']
    search_fields = ['title','author','year', 'subject', 'isbn']
    list_per_page = 25

class BorrowAdmin(admin.ModelAdmin):
    list_display = ['book','student','status', 'expected_return_date', 'return_date','fine']
    search_fields = ['book','student','status', 'expected_return_date', 'return_date']
    list_per_page = 25

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['borrow','merchant_request_id','checkout_request_id', 'code', 'amount','status']
    search_fields = ['borrow','merchant_request_id','checkout_request_id', 'code', 'amount','status']
    list_per_page = 25

admin.site.register(Student,StudentAdmin)
admin.site.register(Book,BooKAdmin)
admin.site.register(Borrow,BorrowAdmin)
admin.site.register(FinePayment,PaymentAdmin)
