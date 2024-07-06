from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware that ensures a user is authenticated to access any page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that do not require authentication
        exempt_urls = [
            reverse('login'),
            reverse('signup'),
            '/admin/' ,  # Adicione quaisquer outras URLs que não exigem autenticação
        ]

        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect('login')

        response = self.get_response(request)
        return response
