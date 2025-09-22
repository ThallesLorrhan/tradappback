from rest_framework import viewsets
from .models import Chapel
from .serializers import ChapelSerializer

class ChapelViewSet(viewsets.ModelViewSet):
    queryset = Chapel.objects.all()
    serializer_class = ChapelSerializer
