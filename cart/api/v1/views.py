from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(['POST'])
def get_sum(request):
    numbers = request.data.get('numbers', [])
    summation = 0
    for number in numbers:
        summation = number + summation

    return Response({"result": summation})
