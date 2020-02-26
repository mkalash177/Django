from django.shortcuts import redirect
from datetime import timedelta, datetime
import pytz
from django.contrib.auth import logout



class LastActionCheckMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_superuser and request.user.is_authenticated:
            local = pytz.timezone('Europe/Kiev')
            if not request.session.get('last_action'):
                request.session['last_action'] = datetime.now().timestamp()
            else:
                local_time_now = local.localize(datetime.now())
                last_action_time = local.localize(datetime.fromtimestamp(request.session.get('last_action')))
                if (local_time_now - last_action_time) >= timedelta(minutes=5):
                    del request.session['last_action']
                    logout(request)
                else:
                    request.session['last_action'] = datetime.now().timestamp()
        response = self.get_response(request)
        return response



class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if 'api' in request.path:
            return self.get_response(request)
        else:
            if request.user.is_authenticated or request.get_full_path().endswith(
                    'login/') or request.get_full_path().endswith('register/'):
                # response = self.get_response(request)
                return self.get_response(request)
        return redirect('login_url')
