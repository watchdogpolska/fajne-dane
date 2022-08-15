from campaigns.models import Query
from campaigns.serializers.output_field import OutputFieldSerializer
from fajne_dane.core.serializers import (
    ReadCreateOnlyModelSerializer, ReadUpdateOnlyModelSerializer, ReadOnlyModelSerializer
)


class QueryCreateSerializer(ReadCreateOnlyModelSerializer):
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


class QuerySerializer(ReadUpdateOnlyModelSerializer):
    output_field = OutputFieldSerializer(read_only=True)

    class Meta:
        model = Query
        fields = ('id', 'order', 'name', 'data', 'output_field')
        read_only_fields = ['id']


class QueryDataSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Query
        fields = ('id', 'order', 'name', 'data')
        read_only_fields = ['id']


class QueryOrderSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Query
        fields = ('id', 'order')
        read_only_fields = ['id', 'order']
