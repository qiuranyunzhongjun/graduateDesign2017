from django.test import TestCase
from django.utils import timezone
from .models import Patient, Measure


class PatientMethodTests(TestCase):
    def test_getRecentMeasure_with_empty(self):
        time = timezone.now()
        empty_measure_patient = Patient(firstname=1, register_date=time)
        self.assertEqual(empty_measure_patient.getRecentMeasure(),'还未录入测试数据')

