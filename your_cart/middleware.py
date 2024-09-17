from django.utils.deprecation import MiddlewareMixin

class GuestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            if not request.session.session_key:
                request.session.create()