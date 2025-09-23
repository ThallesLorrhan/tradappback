from django.contrib import admin
from .models import Chapel, Responsible, Mass, ChapelImage

# Admin de Chapel
@admin.register(Chapel)
class ChapelAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "state", "get_responsibles", "get_masses")
    search_fields = ("name", "city", "state")

    def get_responsibles(self, obj):
        return ", ".join([r.name for r in obj.responsibles.all()])
    get_responsibles.short_description = "Responsáveis"

    def get_masses(self, obj):
        return ", ".join([f"{m.get_day_of_week_display()} {m.time} ({m.get_mass_type_display()})" for m in obj.masses.all()])
    get_masses.short_description = "Missas"

# Admin de Responsible
@admin.register(Responsible)
class ResponsibleAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "phone", "chapel")
    search_fields = ("name", "role", "chapel__name")

# Admin de Mass
@admin.register(Mass)
class MassAdmin(admin.ModelAdmin):
    list_display = ("chapel", "get_day_of_week", "time", "get_mass_type")
    list_filter = ("day_of_week", "mass_type")
    search_fields = ("chapel__name",)

    def get_day_of_week(self, obj):
        return obj.get_day_of_week_display()
    get_day_of_week.short_description = "Dia"

    def get_mass_type(self, obj):
        return obj.get_mass_type_display()
    get_mass_type.short_description = "Tipo"

# Admin de ChapelImage
@admin.register(ChapelImage)
class ChapelImageAdmin(admin.ModelAdmin):
    list_display = ("chapel", "image", "caption")
