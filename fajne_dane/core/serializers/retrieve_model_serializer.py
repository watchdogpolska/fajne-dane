from rest_framework import serializers


class RetrieveModelSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_model(self):
        return getattr(self.Meta, 'model', None)

    @property
    def key_fields(self):
        return getattr(self.Meta, 'key_fields', None)

    def retrieve(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        if self.key_fields:
            validated_data = {k: validated_data[k] for k in self.key_fields}

        model = self.get_model()
        instance = model.objects.filter(**validated_data).first()
        return instance

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()
