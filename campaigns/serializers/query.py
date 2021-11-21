from rest_framework import serializers
from campaigns.models import Query
from campaigns.serializers.output_field import OutputFieldSerializer
from fajne_dane.core.exceptions import NotSupported


class QueryCreateSerializer(serializers.ModelSerializer):
    output_field = OutputFieldSerializer()

    class Meta:
        model = Query
        fields = ('id', 'order', 'name', 'data', 'output_field')
        read_only_fields = ['id']

    def create(self, validated_data):
        output_field_serializer = OutputFieldSerializer(data=validated_data['output_field'])
        output_field_serializer.is_valid(raise_exception=True)
        output_field = output_field_serializer.save()

        query = Query(
            campaign_id=validated_data['campaign'].id,
            order=validated_data['order'],
            name=validated_data['name'],
            data=validated_data['data'],
            output_field=output_field,
        )
        query.save()
        return query

    def update(self, instance, validated_data):
        raise NotSupported()


class QuerySerializer(serializers.ModelSerializer):
    output_field = OutputFieldSerializer(read_only=True)

    class Meta:
        model = Query
        fields = ('id', 'order', 'name', 'data', 'output_field')
        read_only_fields = ['id', 'read_only']

    def create(self, validated_data):
        raise NotSupported()
