from rest_framework import serializers
from .models import Patient, Measure
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    patients = serializers.HyperlinkedRelatedField(queryset=Patient.objects.all(), view_name='patient-detail', many=True)
    measures = serializers.HyperlinkedRelatedField(queryset=Measure.objects.all(), view_name='measure-detail', many=True)

    class Meta:
        model = User
        fields = ( 'username', 'patients','measures','url')


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Patient
        fields = ('firstname','register_date','owner','url')


class MeasureSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Measure
        fields = ('patient','eye_choice','measure_date','owner','url')