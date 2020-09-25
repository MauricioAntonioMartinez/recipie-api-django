from rest_framework import authentication, exceptions, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import AuthSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the db
    """
    serializer_class = UserSerializer


class CreateAuthView(ObtainAuthToken):
    """Create a new token for user
    """
    serializer_class = AuthSerializer
    rendered_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Mange the authenticated user
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrive and return authenticated user
        """
        return self.request.user
