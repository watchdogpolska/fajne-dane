from rest_framework import serializers
from campaigns.models import Query
from campaigns.serializers.output_field import OutputFieldSerializer


class QuerySerializer(serializers.ModelSerializer):
    output_field = OutputFieldSerializer()


    class Meta:
        model = Query
        fields = ('order', 'name', 'data', 'output_field')


    def create(self, validated_data):
        output_field_serializer = OutputFieldSerializer(data=validated_data['output_field'])
        if not output_field_serializer.is_valid():
            raise Exception()
        output_field = output_field_serializer.save()

        query = Query(
            campaign=validated_data['campaign'],
            order=validated_data['order'],
            name=validated_data['name'],
            data=validated_data['data'],
            output_field=output_field,
        )
        return query
