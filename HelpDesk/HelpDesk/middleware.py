from django.shortcuts import redirect


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        valid = ['login/','register/']
        if request.user.is_authenticated or request.get_full_path().endswith('login/') or request.get_full_path().endswith('register/'):
            response = self.get_response(request)
            return response
        return redirect('login_url')
