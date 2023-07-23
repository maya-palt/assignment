
import jwt
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Certificate, CertificateFile
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404
from io import BytesIO
from xhtml2pdf import pisa
from django.urls import reverse
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
from datetime import datetime, timedelta
from .utils import generate_jwt_token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Certificate, CertificateFile
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token



def create_certificate(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        certificate = Certificate.objects.create(name=name, description=description)
        certificate.save()
        # Generate the certificate PDF and save it to the CertificateFile model
        pdf_buffer = generate_certificate_pdf(certificate, 'certificate_id')
        pdf_filename = "certificate_{}.pdf".format(certificate.id)
        certificate_file = CertificateFile(certificate=certificate)
        certificate_file.pdf_file.save(pdf_filename, ContentFile(pdf_buffer.getvalue()))
        certificate_file.save()

        # Redirect to the 'check' view
        return redirect(reverse('check', kwargs={'certificate_id': certificate.id}))

    return render(request, 'create_certificate.html')


def render_to_pdf(template_src, context_dict):
    """
    Generate a PDF using an HTML template with CSS styling.
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result_buffer = BytesIO()

    # Create a PDF from the HTML content
    pisa_status = pisa.CreatePDF(html, dest=result_buffer)

    if pisa_status.err:
        raise Exception("Error generating PDF: {}".format(pisa_status.err))

    return result_buffer

def generate_certificate_pdf(certificate, certificate_id):
    # Context data to be passed to the template
    context = {
        'certificate': certificate,
    }

    # Render the template with CSS styling and logo
    pdf_buffer = render_to_pdf('certificate_template.html', context)
    return pdf_buffer

def certificate_pdf(request, certificate_id):
    
    certificate_file = os.path.join(f'certificates/pdfs/certificate_{certificate_id}.pdf')
    if os.path.exists(certificate_file):
        with open(certificate_file, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="certificate_{certificate_id}.pdf"'
            return response

    return HttpResponse("Certificate PDF not found.", status=404)

def view_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)

    return render(request, 'view_certificate.html', {'certificate': certificate})


import jwt
from datetime import datetime, timedelta


def generate_jwt_token(certificate_id):
    # Set the secret key for JWT token
    secret_key = settings.SECRET_KEY

    # Set the expiration time for the token (e.g., 1 day from now)
    expiration_time = datetime.utcnow() + timedelta(days=1)

    # Create the payload for the token
    payload = {
        'certificate_id': certificate_id,
        'exp': expiration_time
    }

    # Generate the JWT token
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return token


from myapp.models import VerificationID

def verify_certificate(request):
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        verification_id = request.POST.get('verification_id')

        if not verification_id:
            return HttpResponse('Verification ID not provided.', status=400)

        try:
            # Check if the verification ID exists in the VerificationID model
            verification_object = get_object_or_404(VerificationID, verification_id=verification_id)

            # If it exists, the certificate is valid for the associated user
            certificate = verification_object.certificate
            return HttpResponse(f'Certificate "{certificate.name}" is valid.')
        except VerificationID.DoesNotExist:
            return HttpResponse('Verification ID not found.', status=404)

    return render(request, 'verify_certificate.html')



from .utils import generate_jwt_token
from django.views.decorators.csrf import csrf_exempt


from rest_framework.decorators import api_view

from django.contrib.auth.models import User

# @api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            # import pdb;pdb.set_trace()
            return HttpResponse({'error': 'Username already exists'}, status=400)

        # Create a new user account
        user = User.objects.create_user(username=username, password=password, email=email)

        # Optionally, you can generate a JWT token for the new user here
        # (similar to what was done in the login view)

        return HttpResponse({'message': 'User account created successfully'}, status=201)

    return render(request, 'register.html')


# certificates/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
# @api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            jwt_token = str(refresh.access_token)  # Convert the access_token to a string
            return JsonResponse({'token': jwt_token})

        return Response('fine')

    return render(request, 'login.html')



def view_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)

    context = {
        'certificate': certificate,
    }

    return render_to_pdf('view_certificate.html', context)