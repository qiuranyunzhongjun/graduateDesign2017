from django.contrib import admin
from .models import Patient,Measure,FuncData,StruData


class PatientAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'register_date','getRecentMeasure')
    fieldsets = [
        ('匿名编号',               {'fields': ['firstname']}),
        ('录入时间', {'fields': ['register_date']}),
    ]
    list_filter = ['firstname']
admin.site.register(Patient,PatientAdmin)

class FuncDataInline(admin.TabularInline):
    model = FuncData
    extra = 52
class StruDataInline(admin.TabularInline):
    model = StruData
    extra = 12
class MeasureAdmin(admin.ModelAdmin):
    list_display = ('patient','eye_choice','measure_date')
    inlines = [FuncDataInline,StruDataInline]
    list_filter = ['patient','eye_choice','measure_date']
admin.site.register(Measure,MeasureAdmin)
#admin.site.register(FuncData)
#admin.site.register(StruData)
