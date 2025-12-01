from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username_key = getattr(self, 'username_field', 'username')
        self.fields['email'] = serializers.EmailField(write_only=True, required=False)
        if username_key in self.fields:
            self.fields[username_key].required = False

    def validate(self, attrs):
        # attrs only contains fields validated by DRF; the raw input is in self.initial_data
        data = getattr(self, 'initial_data', {}) or {}
        username_key = getattr(self, 'username_field', 'username')

        # If username missing but email present in payload, map email -> username
        if not attrs.get(username_key) and data.get('email'):
            email = data.get('email')
            try:
                user = User.objects.filter(email__iexact=email).first()
                if user:
                    attrs[username_key] = user.get_username()
            except Exception:
                pass

        # If username provided but looks like an email, try resolving it
        if attrs.get(username_key) and '@' in str(attrs.get(username_key)):
            maybe_email = attrs.get(username_key)
            try:
                user = User.objects.filter(email__iexact=maybe_email).first()
                if user:
                    attrs[username_key] = user.get_username()
            except Exception:
                pass

        try:
            return super().validate(attrs)
        except Exception:
            raise serializers.ValidationError({'detail': 'Credenciais inválidas.'})