# serializers.py
from rest_framework import serializers

from .models import Hero, Claims

class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ('name', 'alias')

class ClaimsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Claims
        fields = ('id', 'name', 'age', 'address', 'license_num', 'id_proof', 'claims_amount', 'created_date')
        