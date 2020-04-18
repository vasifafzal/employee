from django.urls import path, include
from employee.views import OrgEmployee
urlpatterns = [
    path('employee/', OrgEmployee.as_view()),
]
