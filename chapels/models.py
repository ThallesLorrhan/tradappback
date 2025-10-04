from django.db import models


class Chapel(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, default="Brasil")

    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    latitude = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=15, null=True, blank=True)


    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Responsible(models.Model):
    chapel = models.ForeignKey(Chapel, on_delete=models.CASCADE, related_name="responsibles")
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, blank=True, null=True)  # Ex: Pároco, Sacristão
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"


class ChapelImage(models.Model):
    chapel = models.ForeignKey(Chapel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="chapels/")
    caption = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Imagem da {self.chapel.name}"


class Mass(models.Model):
    MASS_TYPE_CHOICES = [
        ('rezada', 'Rezada'),
        ('cantada', 'Cantada'),
        ('solene', 'Solene'),
    ]

    chapel = models.ForeignKey(Chapel, on_delete=models.CASCADE, related_name="masses")
    day_of_week = models.IntegerField(choices=[
        (0, "Segunda"),
        (1, "Terça"),
        (2, "Quarta"),
        (3, "Quinta"),
        (4, "Sexta"),
        (5, "Sábado"),
        (6, "Domingo"),
    ])
    time = models.TimeField()
    mass_type = models.CharField(max_length=10, choices=MASS_TYPE_CHOICES)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.chapel.name} - {self.get_day_of_week_display()} {self.time} ({self.get_mass_type_display()})"
