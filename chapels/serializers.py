from rest_framework import serializers
from .models import Chapel

class ChapelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapel
        fields = '__all__'
