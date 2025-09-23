# chapels/serializers.py
from rest_framework import serializers
from .models import Chapel, Responsible, ChapelImage, Mass

class MassSerializer(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    mass_type_display = serializers.CharField(source='get_mass_type_display', read_only=True)

    class Meta:
        model = Mass
        fields = ['id', 'day_of_week', 'time', 'mass_type', 'notes', 'day_of_week_display', 'mass_type_display']

class ResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsible
        fields = ['id', 'name', 'role', 'phone', 'email']

class ChapelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapelImage
        fields = ['id', 'image', 'caption']

class ChapelSerializer(serializers.ModelSerializer):
    masses = MassSerializer(many=True, read_only=True)
    responsibles = ResponsibleSerializer(many=True, read_only=True)
    images = ChapelImageSerializer(many=True, read_only=True)

    class Meta:
        model = Chapel
        fields = '__all__'
