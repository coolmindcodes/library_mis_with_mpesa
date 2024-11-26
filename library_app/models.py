from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=14, unique=True)
    email = models.CharField(max_length=50, unique=True)
    admission_no = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
        db_table = 'students'


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year = models.IntegerField()
    subject = models.CharField(max_length=50)
    isbn = models.CharField(max_length=50, unique=True)
    class Meta:
        ordering = ['title']
        db_table = 'books'
    def __str__(self):
        return self.title

STATUS_CHOICES = (
    ('RETURNED', 'Returned'),
    ('BORROWED', 'Borrowed'),
    ('LOST', 'Lost'),
)
class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='borrower')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    expected_return_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def fine_total(self):
        if self.return_date and self.expected_return_date and self.return_date> self.expected_return_date:
            amount = (self.return_date - self.expected_return_date).days * 10
            return amount
        return 0

    class Meta:
        ordering = ['-created_at']
        db_table = 'borrowings'

    def __str__(self):
        return f" {self.book.title} - {self.student.name}"

class FinePayment(models.Model):
    borrow = models.ForeignKey(Borrow, on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=120)
    code = models.CharField(max_length=50, null=True, blank=True)
    amount= models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'payments'
    def __str__(self):
        return f'{self.merchant_request_id} - {self.amount}'

