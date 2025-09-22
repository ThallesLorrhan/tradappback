from django.db import models

class Chapel(models.Model):
    MISS_TYPES = [
        ('Rezada', 'Rezada'),
        ('Cantada', 'Cantada'),
    ]

    DAYS_OF_WEEK = [
        ('Segunda', 'Segunda'),
        ('Terça', 'Terça'),
        ('Quarta', 'Quarta'),
        ('Quinta', 'Quinta'),
        ('Sexta', 'Sexta'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    priest = models.CharField(max_length=255)
    miss_type = models.CharField(max_length=10, choices=MISS_TYPES)
    schedule = models.TimeField()
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    photo = models.ImageField(upload_to='chapel_photos/', blank=True, null=True)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)

    def __str__(self):
        return self.name
