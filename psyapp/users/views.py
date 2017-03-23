from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from oauth2_provider.models import AccessToken
from braces.views import CsrfExemptMixin
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.settings import oauth2_settings
from rest_framework.views import APIView
import json

from .serializers import UserSerializer
from .models import User

# Create your views here.
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Register new User
    """
    if request.method == 'POST':
        if User.objects.filter(email=request.data['email']):
            return Response(status=302, data={'error': 'user already exists'})
        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid(raise_exception=True):
            userSerializer.save()
        return Response(status=200, data=userSerializer.data)

class TokenView(APIView, CsrfExemptMixin, OAuthLibMixin):
    permission_classes = (permissions.AllowAny,)

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        email = request.POST.get('email')
        try:
            if email is None:
                raise User.DoesNotExist
        except Exception as e:
            return Response(data={'error': e.message}, status=400)
        try:
            user = User.objects.get(email=email)
            if user:
                if not user.check_password(request.POST.get('password')):
                    return Response(status=401, data={'error': 'incorrect password'})
                userToken = AccessToken.objects.filter(user=user)
                if userToken:
                    return Response(data={
                        'access_token': userToken[0].token,
                        'token_type': 'Bearer',
                        "email": userToken[0].user.email,
                        "scope": userToken[0].scope
                    }, status=200)
                else:
                    url, headers, body, status = self.create_token_response(request)
                    data = json.loads(body)
                    tokenObject = AccessToken.objects.get(token=data['access_token'])
                    tokenObject.user = user
                    tokenObject.save()
                    data['email'] = email
                    return Response(data, status=status, headers=headers)
        except Exception as e:
            return Response(status=404, data={'error': e.message})
