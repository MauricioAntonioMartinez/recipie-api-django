from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers

# from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user serializer
    """
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # fields that we want to be able to write and read
        # in the database
        # read_only_fields = ['email']  # this fields doesn't
        # take in condiretation for post patch put request
        extra_kwargs = {
            'password': {
                "write_only": True,
                "min_length": 5
            },
        }
        # this allow us to specify extra arguments or validation
        # that can be accepted in this serializer
        # the validate foo will be in charge to respect this conditions

    def create(self, validated_data):
        """create a new user with encripted password and return it
        """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update a user, setting the password correctly and return it

        Args:
            instance (model Instance): User Object Email this case
            validated_data (fields): Valid fields   

        Raises:
            serializers.ValidationError: [description]

        Returns: User
        """
        # print(f'THE DATA {validated_data}')
        # validated_data.pop('email')  # cannot update his email
        password = validated_data.pop('password', None)
        # the None is the default value if not exists
        # the pop is deleting the field password from the dict
        user = super().update(instance, validated_data)
        # super to the normal update

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthSerializer(serializers.Serializer):
    """Serializer for the user authentication token
    """
    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user
        """
        email = attrs.get('email')
        password = attrs.get('password')
        # this is how you access to the context of the request
        print(self.context.get('request'))
        user = authenticate(request=self.context.get(
            'request'), username=email, password=password)
        # if cannot authenticate return None
        if not user:
            msg = ('Unable to authenticate for provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs
