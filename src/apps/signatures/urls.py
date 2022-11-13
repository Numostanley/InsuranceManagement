from .docusign import *
from django.urls import path


app_name = 'signature'

urlpatterns = [
    path('docusign_signature/', docusign_signature, name='docusign_signature'),
    path('signed_completed/', sign_completed, name='sign_completed'),
    path('get_envelope_status/<str:envelope_id>', get_envelope_status, name='get_envelope_status'),
]