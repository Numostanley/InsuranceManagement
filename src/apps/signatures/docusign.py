import base64
import json
import logging as logger
import os

from datetime import date

import requests

from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from docusign_esign import RecipientViewRequest, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients, ApiClient, EnvelopesApi, Text, DateSigned
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.settings.base import BASE_DIR, client_user_id, account_id
from . import tokens



def create_jwt_grant():
    token = tokens.docusign_token()
    logger.info('TOKEN', token)
    return token

@api_view(['GET'])
def docusign_signature(request):
    try:
        token = create_jwt_grant()
        post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': token}
        base_url = 'https://account-d.docusign.com/oauth/token'
        r = requests.post(base_url, data=post_data)
        token = r.json()
        data = json.loads(request.body)
        signer_email = data['email']
        signer_name = data['full_name']
        signer_type = data['type']
        
        # document that are to be signed
        with open(os.path.join(BASE_DIR, 'docusign_file/', 'scan.pdf'), 'rb') as file: # Your docusignfile path
            content_bytes = file.read()
        base64_file_content = base64.b64encode(content_bytes).decode('ascii')
        
        if signer_type == 'embedded':
            domain = get_current_site(request)
            url = signature_by_embedded(token, base64_file_content, signer_name, signer_email, domain)
            prefix, envelope_string = url.split('v1/')
            envelope_id, suffix = envelope_string.split('?')
       
        return Response({
            'docsign_url': url,
            'envelope_id': envelope_id,
            'message': 'Docusign',
            'error': ''
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            'docsign_url': '',
            'envelope_id': '',
            'message': 'Internal server error',
            'error': 'In docusign_signature: '+str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def signature_by_embedded(token, base64_file_content, signer_name, signer_email, domain):
    try:
        # Create the document model
        document = Document( # create the DocuSign document object
            document_base64 = base64_file_content,
            name = 'scan', # this is just a sample name. name can be something else
            file_extension = 'pdf', # other document types arre accepted
            document_id = '1'
        )
        
        sign_here = SignHere(
            document_id = '1',
            page_number = '1',
            recepient_id = '1',
            tab_label = 'SignHereTab',
            y_position = '513',
            x_position = '80'
        )
        
        today = date.today()
        current_date = today.strftime("%d/%m/%Y")
        sign_date = DateSigned(
            document_id = '1',
            page_number = '1',
            recipient_id = '1',
            tab_label = 'Date',
            font = 'helvetica',
            bold = "true",
            value = current_date,
            tab_id = "date",
            font_size = "size16",
            y_position = "55",
            x_position = "650"
        )
        
        text_name = Text(
            document_id = '1',
            page_number = '1',
            recipient_id = '1',
            tab_label = 'Name',
            font = 'helvetica',
            bold = "true",
            value = signer_name,
            tab_id = "name",
            font_size = "size16",
            y_position = "280",
            x_position = "54"
        )
        
        text_email = Text(
            document_id = '1',
            page_number = '1',
            recipient_id = '1',
            tab_label = 'Email',
            font = 'helvetica',
            bold = "true",
            value = signer_email,
            tab_id = "email",
            font_size = "size16",
            y_position = "304",
            x_position = "82"
        )
        
        signer_tab = Tabs(sign_here_tabs=[sign_here], text_tabs=[text_name, text_email, sign_date])
        signer = Signer(
            email = signer_email, name = signer_name, recipient_id = '1', routing_order = '1', 
            client_user_id = client_user_id, tabs = signer_tab
        )
        
        # Next, create the top level envelope definition and populate it.
        envelope_definition = EnvelopeDefinition(
            email_subject = "Please sign this document",
            documents = [document],
            # The Recipients object wants arrays for each recipient type
            recipients = Recipients(signers=[signer]),
            status = "sent" # requests that the envelope be created and sent.
        )
        
        #STEP-2 create/send eenvelope
        api_client = ApiClient()
        api_client.host = "https://demo.docusign.net/restapi"
        api_client.set_default_header('Authorization', 'Bearer ' + token['access_token'])
        
        envelope_api = EnvelopesApi(api_client)
        results = envelope_api.create_envelope(account_id=account_id, envelope_definition=envelope_definition)
        envelope_id = results.envelope_id
        envelope_status = results.status
        #Create the Recipients View request object
        recipient_view_request = RecipientViewRequest(
            authentication_method = 'email',
            client_user_id = client_user_id,
            recipient_id = '1',
            return_url = f'http://{domain}/signatures/signed_completed/', # Your redirected URL
            user_name = signer_name,
            email = signer_email
        )
        
        # Obtain the recipient view url for the signing ceremony
        # Exceptions will be caught by the calling function
        results = envelope_api.create_recipient_view(account_id, envelope_id, recipient_view_request = recipient_view_request)
        return results.url
    
    except Exception as e:
        return JsonResponse({
            'docsign_url': '',
            'message' : 'Internal server error',
            'error': 'In signature by embedded: '+str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def sign_completed( request):
    return HttpResponse('Signing completed successfully')

@api_view(['GET'])
def get_envelope_status(request, envelope_id):
    token = create_jwt_grant()
    post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 
                 'assertion': token}
    base_url = 'https://account-d.docusign.com/oauth/token'
    r = requests.post(base_url, data=post_data)
    token = r.json()
    base_url = f'https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes/{envelope_id}'
    r = requests.get(base_url, headers={'Authorization': 'Bearer ' + token['access_token']})
    response = r.json()
    logger.info('response: %s', response)
    
    return Response({
        'response': response,
        'error': ''
    }, status=status.HTTP_200_OK)
    