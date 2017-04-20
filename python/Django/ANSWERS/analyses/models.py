from django.db import models


class Patient(models.Model):
    firstname = models.IntegerField('匿名化ID',primary_key=True)
    register_date = models.DateField('录入时间')
    owner = models.ForeignKey('auth.User', related_name='patients', on_delete=models.CASCADE)

    def getRecentMeasure(self):
        measures = self.measure_set.all()
        if len(measures) == 0:
            return '还未录入测试数据'
        last_measure = max(measures)
        return str(last_measure.measure_date)
    getRecentMeasure.short_description = '最近测量日期'
    def __str__(self):
        return 'patient '+str(self.firstname)

    class Meta:
        ordering = ('firstname',)


class Measure(models.Model):
    patient = models.ForeignKey(Patient)
    eye_choice = models.CharField('左眼or右眼',max_length = 1,choices = (('L','left eye'),('R','right eye')), default ='R')
    measure_date = models.DateField('测试日期')
    owner = models.ForeignKey('auth.User', related_name='measures', on_delete=models.CASCADE)

    def __cmp__(self,other):
        if self.measure_date<other.measure_date:
            return -1
        elif self.measure_date>other.measure_date:
            return 1
        else :
            return 0
    def __str__(self):
        return str(self.patient)+'\' '+self.eye_choice+' @ '+str(self.measure_date)


class FuncData(models.Model):
    measure = models.ForeignKey(Measure)
    point_no = models.PositiveSmallIntegerField('所测量的位置编号')
    measure_func_data = models.FloatField('功能数据')

    def __str__(self):
        return str(self.measure)+' F# '+str(self.point_no)


class StruData(models.Model):
    measure = models.ForeignKey(Measure)
    area_no = models.PositiveSmallIntegerField('所测量的区域编号')
    avg_data = models.FloatField('结构数据')

    def __str__(self):
        return str(self.measure)+' S# '+str(self.area_no)
