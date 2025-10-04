# serializers.py
from rest_framework import serializers
from .models import Chapel, Responsible, ChapelImage, Mass

class MassSerializer(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    mass_type_display = serializers.CharField(source='get_mass_type_display', read_only=True)

    class Meta:
        model = Mass
        fields = ['id', 'day_of_week', 'day_of_week_display', 'time', 'mass_type', 'mass_type_display', 'notes']

class ResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsible
        fields = ['id', 'name', 'role', 'phone', 'email']

class ChapelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapelImage
        fields = ['id', 'image']

class ChapelSerializer(serializers.ModelSerializer):
    masses = MassSerializer(many=True, read_only=True)
    responsibles = ResponsibleSerializer(many=True, read_only=True)
    images = ChapelImageSerializer(many=True, read_only=True)

    class Meta:
        model = Chapel
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')

        masses_data = request.data.get('masses', '[]')
        responsibles_data = request.data.get('responsibles', '[]')

        # Convertendo de JSON se necessário
        import json
        if isinstance(masses_data, str):
            masses_data = json.loads(masses_data)
        if isinstance(responsibles_data, str):
            responsibles_data = json.loads(responsibles_data)

        # Latitude e longitude
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

        # Remover campos extras
        validated_data.pop('masses', None)
        validated_data.pop('responsibles', None)
        validated_data.pop('images', None)

        chapel = Chapel.objects.create(**validated_data)

        for mass in masses_data:
            Mass.objects.create(chapel=chapel, **mass)

        for responsible in responsibles_data:
            Responsible.objects.create(chapel=chapel, **responsible)

        for image_file in request.FILES.getlist('images'):
            ChapelImage.objects.create(chapel=chapel, image=image_file)

        return chapel
