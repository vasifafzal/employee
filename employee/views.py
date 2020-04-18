import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employee.models import Employee


class OrgEmployee(APIView):
    """
    API's for Creating, Listing and Deleting Employees.
    """

    def post(self, request):
        """
        API for Saving the Employee data.
        :param request:
        :return: dict --> with Sucess or Error message
        """
        name = request.data.get("employee_name")
        employee_id = request.data.get("employee_id")
        date_of_birth = request.data.get("date_of_birth")
        reporting_manager = request.data.get("reporting_manager")
        if name and name.strip() and employee_id and employee_id.strip() and date_of_birth and date_of_birth.strip():
            try:
                date_of_birth = datetime.datetime.strptime(date_of_birth, "%d/%m/%Y")
            except Exception as e:
                print(e)
                return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)
            if Employee.objects.all().exists():
                if reporting_manager:
                    reporting_manager_obj = Employee.objects.filter(employee_id=reporting_manager)
                    if reporting_manager_obj.exists():
                        emp = Employee.objects.create(name=name,
                                                      employee_id=employee_id,
                                                      date_of_birth=date_of_birth,
                                                      reporting_manager=reporting_manager_obj.first())
                        return Response({"employee": emp.employee_id}, status=status.HTTP_201_CREATED)
            else:
                emp = Employee.objects.create(name=name,
                                              employee_id=employee_id,
                                              date_of_birth=date_of_birth)
                return Response({"employee": emp.employee_id}, status=status.HTTP_201_CREATED)
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Api for deleting the Employee.
        :param request:
        :return: str --> Success or Error Message.
        """
        employee_id = request.data.get("employee_id")
        if employee_id:
            try:
                employee_obj = Employee.objects.get(employee_id=employee_id)
                if employee_obj.reporting_manager:
                    Employee.objects.filter(reporting_manager=employee_obj).update(
                        reporting_manager=employee_obj.reporting_manager)
                    employee_obj.delete()
                    return Response("Deleted Successfully", status=status.HTTP_200_OK)
            except Exception as e:
                return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Api for fetching the people under the employee.
        :param request:
        :return:
        """
        employee_id = request.GET.get("employee_id")
        if employee_id:
            try:
                employee_obj = Employee.objects.get(employee_id=employee_id)
                data = Employee.objects.filter(reporting_manager=employee_obj).values("employee_id", "name")
                return Response(list(data), status=status.HTTP_200_OK)
            except Exception as e:
                return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)
