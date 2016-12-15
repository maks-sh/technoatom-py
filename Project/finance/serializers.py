from rest_framework import serializers
from .models import *
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.validators import UniqueValidator


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['acc_id', 'total', 'acc_name', 'user_id']
        read_only_fileds = ['acc_id',]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ChargeCategory
        fields = ['cat_id', 'cat_name']
        read_only_fileds = ['cat_id', ]





class ChargeSerializer(serializers.ModelSerializer):

    account = AccountSerializer(source='account')

    class Meta:
        model = Charge
        fields = ['ch_id', 'value', 'date', 'account']
        read_only_fileds = ['ch_id',]
