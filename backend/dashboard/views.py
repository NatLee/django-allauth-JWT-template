from django.shortcuts import render
from rest_framework.views import APIView

class DashboardView(APIView):
    permission_classes = []

    def get(self, request):
        return render(request, 'index.html')
