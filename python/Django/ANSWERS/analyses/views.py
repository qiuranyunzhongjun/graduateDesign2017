from django.shortcuts import get_object_or_404,render
from .serializers import PatientSerializer, MeasureSerializer,UserSerializer
from .models import Patient, Measure
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets


def index(request):
    patients = Patient.objects.order_by('firstname')
    context = {'patients':patients}
    return render(request, 'analyses/index.html',context)


def answers(request, patient_id):
    patient = get_object_or_404(Patient, pk = patient_id)
    return render(request, 'analyses/answers.html', {'patient':patient})


class PatientViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MeasureViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer