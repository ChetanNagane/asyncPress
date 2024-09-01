import uuid

from django.db import models

class Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'pending'),
        ('Completed', 'completed'),
        ('Failed', 'failed'),
    ]
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=50)
    error_details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    serial_number = models.IntegerField()
    product_name = models.CharField(max_length=255)
    input_image_urls = models.TextField()
    output_image_urls = models.TextField(blank=True, null=True)
