# serializers.py
from rest_framework import serializers
from .models import Chapel, Responsible, ChapelImage, Mass
import json

class ChapelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapel
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')

        # Pegando massas e responsáveis do request
        masses_data = request.data.get('masses', '[]')
        responsibles_data = request.data.get('responsibles', '[]')

        # Se forem strings JSON, converte para lista
        if isinstance(masses_data, str):
            masses_data = json.loads(masses_data)
        if isinstance(responsibles_data, str):
            responsibles_data = json.loads(responsibles_data)

        # Latitude e longitude (tratando arrays)
        lat = request.data.get('latitude')
        lon = request.data.get('longitude')

        try:
            if isinstance(lat, list):
                lat = lat[0]
            validated_data['latitude'] = float(lat) if lat else None
        except (TypeError, ValueError):
            validated_data['latitude'] = None

        try:
            if isinstance(lon, list):
                lon = lon[0]
            validated_data['longitude'] = float(lon) if lon else None
        except (TypeError, ValueError):
            validated_data['longitude'] = None

        # Remove campos extras que não existem na model
        validated_data.pop('masses', None)
        validated_data.pop('responsibles', None)
        validated_data.pop('images', None)

        # Cria a capela
        chapel = Chapel.objects.create(**validated_data)

        # Cria massas
        for mass in masses_data:
            Mass.objects.create(chapel=chapel, **mass)

        # Cria responsáveis
        for responsible in responsibles_data:
            Responsible.objects.create(chapel=chapel, **responsible)

        # Cria imagens
        for image_file in request.FILES.getlist('images'):
            ChapelImage.objects.create(chapel=chapel, image=image_file)

        return chapel
