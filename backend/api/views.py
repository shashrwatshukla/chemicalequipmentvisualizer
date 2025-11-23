from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Count, Max, Min, Avg, StdDev, Variance
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .models import Dataset, Equipment, EmailVerification
from .serializers import DatasetSerializer, DatasetListSerializer, UserSerializer
from .utils import process_csv_file, save_equipment_data, generate_pdf_report_with_charts
import re
import json
import requests # MODIFIED: Added for Google Access Token verification


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not password or not email:
        return Response({'error': 'Username, email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return Response({'error': 'Username must be 3-20 characters (letters, numbers, underscore only)'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(password) < 8:
        return Response({'error': 'Password must be at least 8 characters'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.search(r'[A-Z]', password):
        return Response({'error': 'Password must contain at least one uppercase letter'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.search(r'[0-9]', password):
        return Response({'error': 'Password must contain at least one number'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return Response({'error': 'Password must contain at least one special character'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        verification_code = get_random_string(length=6, allowed_chars='0123456789')
        EmailVerification.objects.create(user=user, code=verification_code)
        
        try:
            subject = 'Verify Your Email - Chemical Equipment Visualizer'
            message = f'''Hello {username},\n\nYour verification code is: {verification_code}\n\nThis code expires in {settings.EMAIL_VERIFICATION_TIMEOUT_MINUTES} minutes.\n\nBest regards,\nChemical Equipment Visualizer Team'''
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            email_sent = True
        except Exception as e:
            email_sent = False
        
        return Response({
            'message': 'Registration successful! Please check your email for verification code.',
            'verification_required': True,
            'email_sent': email_sent
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f'Registration failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    username = request.data.get('username')
    code = request.data.get('code')
    
    if not username or not code:
        return Response({'error': 'Username and verification code required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username)
        verification = EmailVerification.objects.filter(user=user, code=code, is_verified=False).first()
        
        if not verification:
            return Response({'error': 'Invalid or expired verification code'}, status=status.HTTP_400_BAD_REQUEST)
        
        timeout = timedelta(minutes=settings.EMAIL_VERIFICATION_TIMEOUT_MINUTES)
        if timezone.now() > verification.created_at + timeout:
            return Response({'error': 'Verification code expired. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = True
        user.save()
        verification.is_verified = True
        verification.save()
        
        print(f"✅ User {username} verified successfully")
        return Response({'message': 'Email verified successfully! You can now login.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"❌ Verification error: {str(e)}")
        return Response({'error': f'Verification failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    token = request.data.get('token')
    
    if not token:
        return Response({'error': 'Google token required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # MODIFIED: Use Google UserInfo API to verify Access Token
        google_response = requests.get(f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}')
        
        if google_response.status_code != 200:
            return Response({'error': 'Invalid Google Token'}, status=status.HTTP_400_BAD_REQUEST)
            
        user_data = google_response.json()
        email = user_data.get('email')
        name = user_data.get('name', '')
        
        if not email:
            return Response({'error': 'Email not provided by Google'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=name.split()[0] if name else '',
                last_name=' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
                is_active=True
            )
            EmailVerification.objects.create(user=user, code='GOOGLE_AUTH', is_verified=True)
            print(f"✅ New user created via Google: {username}")
        
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        serializer = UserSerializer(user)
        
        return Response({'message': 'Google authentication successful', 'user': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"❌ Google auth error: {str(e)}")
        return Response({'error': f'Authentication failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        reset_code = get_random_string(length=6, allowed_chars='0123456789')
        EmailVerification.objects.filter(user=user).delete()
        EmailVerification.objects.create(user=user, code=reset_code, is_verified=False)
        
        try:
            subject = 'Password Reset Code - Chemical Equipment Visualizer'
            message = f'''Hello {user.username},\n\nYour password reset code is: {reset_code}\n\nThis code expires in {settings.EMAIL_VERIFICATION_TIMEOUT_MINUTES} minutes.\n\nIf you didn't request this, please ignore this email.\n\nBest regards,\nChemical Equipment Visualizer Team'''
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            email_sent = True
            print(f"✅ Password reset email sent to {email} with code: {reset_code}")
        except Exception as e:
            print(f"❌ Email sending failed: {str(e)}")
            email_sent = False
        
        return Response({
            'message': 'Password reset code sent to your email',
            'email_sent': email_sent,
            'dev_code': reset_code if not email_sent else None
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'If this email exists, a reset code has been sent'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"❌ Password reset error: {str(e)}")
        return Response({'error': f'Password reset failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    email = request.data.get('email')
    code = request.data.get('code')
    new_password = request.data.get('new_password')
    
    if not email or not code or not new_password:
        return Response({'error': 'Email, code, and new password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_password) < 8:
        return Response({'error': 'Password must be at least 8 characters'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.search(r'[A-Z]', new_password):
        return Response({'error': 'Password must contain at least one uppercase letter'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.search(r'[0-9]', new_password):
        return Response({'error': 'Password must contain at least one number'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
        return Response({'error': 'Password must contain at least one special character'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        verification = EmailVerification.objects.filter(user=user, code=code, is_verified=False).first()
        
        if not verification:
            return Response({'error': 'Invalid or expired reset code'}, status=status.HTTP_400_BAD_REQUEST)
        
        timeout = timedelta(minutes=settings.EMAIL_VERIFICATION_TIMEOUT_MINUTES)
        if timezone.now() > verification.created_at + timeout:
            return Response({'error': 'Reset code expired. Please request a new one.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        verification.is_verified = True
        verification.save()
        
        print(f"✅ Password reset successful for {user.username}")
        return Response({'message': 'Password reset successful! You can now login with your new password.'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email or reset code'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"❌ Password reset error: {str(e)}")
        return Response({'error': f'Password reset failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not current_password or not new_password:
        return Response({'error': 'Current and new password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    if not user.check_password(current_password):
        return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_password) < 8:
        return Response({'error': 'Password must be at least 8 characters'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.search(r'[A-Z]', new_password):
        return Response({'error': 'Password must contain at least one uppercase letter'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.search(r'[0-9]', new_password):
        return Response({'error': 'Password must contain at least one number'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
        return Response({'error': 'Password must contain at least one special character'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user.set_password(new_password)
        user.save()
        print(f"✅ Password changed for {user.username}")
        return Response({'message': 'Password changed successfully!'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"❌ Password change error: {str(e)}")
        return Response({'error': f'Password change failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    password = request.data.get('password')
    
    if not password:
        return Response({'error': 'Password is required to delete account'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    if not user.check_password(password):
        return Response({'error': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        username = user.username
        logout(request)
        user.delete()
        print(f"✅ Account deleted: {username}")
        return Response({'message': 'Account deleted successfully', 'redirect': True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"❌ Account deletion error: {str(e)}")
        return Response({'error': f'Account deletion failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username_or_email = request.data.get('username')
    password = request.data.get('password')
    
    if not username_or_email or not password:
        return Response({'error': 'Please provide username/email and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_to_check = None
    try:
        user_to_check = User.objects.get(username=username_or_email)
    except User.DoesNotExist:
        try:
            user_to_check = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user_to_check.is_active:
        return Response({'error': 'Please verify your email before logging in'}, status=status.HTTP_403_FORBIDDEN)
    
    user = authenticate(request, username=user_to_check.username, password=password)
    
    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        print(f"✅ User {user.username} logged in successfully")
        return Response({'message': 'Login successful', 'user': serializer.data, 'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_dataset(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    csv_file = request.FILES['file']
    
    if not csv_file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
    
    success, result = process_csv_file(csv_file)
    
    if not success:
        return Response({'error': result}, status=status.HTTP_400_BAD_REQUEST)
    
    numeric_cols = result['column_summary']['numeric_columns']
    
    dataset = Dataset.objects.create(
        name=csv_file.name,
        uploaded_by=request.user,
        file_path=csv_file,
        total_equipment=result['total_equipment'],
        avg_flowrate=0,
        avg_pressure=0,
        avg_temperature=0
    )
    
    save_equipment_data(dataset, result['equipment_list'], result['column_summary'])
    
    user_datasets = Dataset.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    if user_datasets.count() > 5:
        datasets_to_delete = user_datasets[5:]
        for ds in datasets_to_delete:
            ds.delete()
    
    dataset.refresh_from_db()
    
    serializer = DatasetSerializer(dataset)
    
    column_mapping = {
        'param1': numeric_cols[0] if len(numeric_cols) > 0 else 'Parameter 1',
        'param2': numeric_cols[1] if len(numeric_cols) > 1 else 'Parameter 2',
        'param3': numeric_cols[2] if len(numeric_cols) > 2 else 'Parameter 3',
    }
    
    response_data = {
        'message': 'Dataset uploaded successfully',
        'dataset': serializer.data,
        'column_summary': result['column_summary'],
        'column_mapping': column_mapping,
        'averages': result['averages'],
        'ranges': result['ranges']
    }
    
    return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_datasets(request):
    datasets = Dataset.objects.filter(uploaded_by=request.user)[:5]
    serializer = DatasetListSerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_detail(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, uploaded_by=request.user)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DatasetSerializer(dataset)
    type_dist = dataset.equipment.values('equipment_type').annotate(count=Count('id'))
    type_distribution = {item['equipment_type']: item['count'] for item in type_dist}
    
    response_data = serializer.data
    response_data['type_distribution'] = type_distribution
    
    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_summary(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, uploaded_by=request.user)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    
    type_dist = dataset.equipment.values('equipment_type').annotate(count=Count('id'))
    type_distribution = {item['equipment_type']: item['count'] for item in type_dist}
    
    equipment_stats = dataset.equipment.aggregate(
        max_flowrate=Max('flowrate'),
        min_flowrate=Min('flowrate'),
        std_flowrate=StdDev('flowrate'),
        var_flowrate=Variance('flowrate'),
        max_pressure=Max('pressure'),
        min_pressure=Min('pressure'),
        std_pressure=StdDev('pressure'),
        var_pressure=Variance('pressure'),
        max_temperature=Max('temperature'),
        min_temperature=Min('temperature'),
        std_temperature=StdDev('temperature'),
        var_temperature=Variance('temperature'),
    )
    
    total = dataset.total_equipment
    type_percentages = {eq_type: round((count / total) * 100, 2) for eq_type, count in type_distribution.items()}
    
    cv_flowrate = (equipment_stats['std_flowrate'] / dataset.avg_flowrate * 100) if dataset.avg_flowrate else 0
    cv_pressure = (equipment_stats['std_pressure'] / dataset.avg_pressure * 100) if dataset.avg_pressure else 0
    cv_temperature = (equipment_stats['std_temperature'] / dataset.avg_temperature * 100) if dataset.avg_temperature else 0
    
    summary = {
        'id': dataset.id,
        'name': dataset.name,
        'uploaded_at': dataset.uploaded_at,
        'total_equipment': dataset.total_equipment,
        'averages': {
            'flowrate': dataset.avg_flowrate,
            'pressure': dataset.avg_pressure,
            'temperature': dataset.avg_temperature,
        },
        'ranges': {
            'flowrate': {
                'min': equipment_stats['min_flowrate'],
                'max': equipment_stats['max_flowrate'],
                'std': round(equipment_stats['std_flowrate'] or 0, 2),
                'var': round(equipment_stats['var_flowrate'] or 0, 2),
                'cv': round(cv_flowrate, 2),
            },
            'pressure': {
                'min': equipment_stats['min_pressure'],
                'max': equipment_stats['max_pressure'],
                'std': round(equipment_stats['std_pressure'] or 0, 2),
                'var': round(equipment_stats['var_pressure'] or 0, 2),
                'cv': round(cv_pressure, 2),
            },
            'temperature': {
                'min': equipment_stats['min_temperature'],
                'max': equipment_stats['max_temperature'],
                'std': round(equipment_stats['std_temperature'] or 0, 2),
                'var': round(equipment_stats['var_temperature'] or 0, 2),
                'cv': round(cv_temperature, 2),
            },
        },
        'type_distribution': type_distribution,
        'type_percentages': type_percentages,
    }
    
    return Response(summary)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_report(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, uploaded_by=request.user)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    
    pdf_buffer = generate_pdf_report_with_charts(dataset)
    
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{dataset.name}_complete_report.pdf"'
    
    return response


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, uploaded_by=request.user)
        dataset.delete()
        return Response({'message': 'Dataset deleted successfully'}, status=status.HTTP_200_OK)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)