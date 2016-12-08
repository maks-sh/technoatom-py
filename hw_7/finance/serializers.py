from rest_framework import serializers
from .models import Account
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.validators import UniqueValidator


class AccountSerializer(serializers.ModelSerializer):
    # number = serializers.CharField(
    #     max_length=22,
    #     validators=[
    #         UniqueNumberValidator(queryset=Account.objects.all())
    #     ]
    # )

    class Meta:
        model = Account
        fields = ['id_acc', 'total']
