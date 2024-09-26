# views.py
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse

def activation_redirect(request, uidb64, token):
    try:
        frontend_url = f"http://localhost:5173/activate/{uidb64}/{token}/"
        return redirect(frontend_url)
    except Exception as e:
        return HttpResponse("Activation link is invalid.", status=400)
    
