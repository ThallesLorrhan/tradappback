from rest_framework import serializers
from .models import Chapel, Responsible, ChapelImage, Mass
import json

class MassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mass
        fields = ['day_of_week', 'time', 'mass_type', 'notes']

class ResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsible
        fields = ['name', 'role', 'phone', 'email']

class ChapelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapelImage
        fields = ['image', 'caption']

class ChapelSerializer(serializers.ModelSerializer):
    masses = MassSerializer(many=True)
    responsibles = ResponsibleSerializer(many=True)
    images = ChapelImageSerializer(many=True, required=False)

    class Meta:
        model = Chapel
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')

        # Parse JSON enviado via FormData
        masses_data = json.loads(request.data.get('masses', '[]')) if request else []
        responsibles_data = json.loads(request.data.get('responsibles', '[]')) if request else []

        # Pega os arquivos de imagens
        images_files = request.FILES.getlist('images') if request else []

        # Remove campos do validated_data para não dar conflito
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
        for image_file in images_files:
            ChapelImage.objects.create(chapel=chapel, image=image_file)

        return chapel
