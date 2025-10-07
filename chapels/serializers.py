from rest_framework import serializers
from .models import Chapel, Responsible, ChapelImage, Mass
import json

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

        # Parse JSON com segurança
        def parse_json(field):
            data = request.data.get(field, '[]')
            if isinstance(data, str):
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    return []
            return data

        masses_data = parse_json('masses')
        responsibles_data = parse_json('responsibles')

        def parse_float(value):
            try:
                if isinstance(value, list):
                    value = value[0]
                return float(value)
            except (TypeError, ValueError):
                return None

        validated_data['latitude'] = parse_float(request.data.get('latitude'))
        validated_data['longitude'] = parse_float(request.data.get('longitude'))

        # Cria a capela
        chapel = Chapel.objects.create(**validated_data)

        # Cria missas, responsáveis e imagens
        Mass.objects.bulk_create([Mass(chapel=chapel, **mass) for mass in masses_data])
        Responsible.objects.bulk_create([Responsible(chapel=chapel, **r) for r in responsibles_data])
        for image_file in request.FILES.getlist('images'):
            ChapelImage.objects.create(chapel=chapel, image=image_file)

        return chapel
