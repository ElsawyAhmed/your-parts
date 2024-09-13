from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def get_sum(request):
    return Response({"Key", "Val"}, status=200)