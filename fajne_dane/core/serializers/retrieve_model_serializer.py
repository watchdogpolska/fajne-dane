from rest_framework import serializers

from users.exceptions import ObjectNotFound


class RetrieveModelSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_model(self):
        return getattr(self.Meta, 'model', None)

    @property
    def key_fields(self):
        return getattr(self.Meta, 'key_fields', None)

    def _load_instance(self, args):
        validated_data = {**args}
        if self.key_fields:
            validated_data = {k: args[k] for k in self.key_fields}

        model = self.get_model()
        self.instance = model.objects.filter(**validated_data).first()

    def retrieve(self):
        return self.instance

    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        raise NotImplemented()

    def validate(self, attrs):
        self._load_instance(attrs)
        if not self.instance:
            raise ObjectNotFound()

        return super().validate(attrs)
