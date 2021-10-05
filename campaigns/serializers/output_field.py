from rest_framework import serializers
from campaigns.models import OutputField


class OutputFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = OutputField
        fields = ('name', 'widget', 'answers', 'type', 'validation', 'default_answer')
