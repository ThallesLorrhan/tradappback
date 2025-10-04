# views.py
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Chapel
from .serializers import ChapelSerializer

class ChapelViewSet(viewsets.ModelViewSet):
    queryset = Chapel.objects.all()
    serializer_class = ChapelSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
