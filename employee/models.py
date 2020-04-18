from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=250)
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    reporting_manager = models.ForeignKey("self", null=True, blank=True, on_delete=models.DO_NOTHING)
    created_timestamp = models.DateTimeField(auto_now=True)
    updated_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name