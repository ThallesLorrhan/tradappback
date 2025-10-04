# chapels/serializers.py
from rest_framework import serializers
from .models import Chapel, Responsible, ChapelImage, Mass

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
    images = ChapelImageSerializer(many=True)

    class Meta:
        model = Chapel
        fields = '__all__'

    def create(self, validated_data):
        masses_data = validated_data.pop('masses', [])
        responsibles_data = validated_data.pop('responsibles', [])
        images_data = validated_data.pop('images', [])

        chapel = Chapel.objects.create(**validated_data)

        for mass in masses_data:
            Mass.objects.create(chapel=chapel, **mass)

        for responsible in responsibles_data:
            Responsible.objects.create(chapel=chapel, **responsible)

        for image in images_data:
            ChapelImage.objects.create(chapel=chapel, **image)

        return chapel

