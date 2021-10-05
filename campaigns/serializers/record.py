from rest_framework import serializers
from campaigns.models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', ]
