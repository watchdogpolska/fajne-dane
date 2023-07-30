from rest_framework import generics


class GenericTwoTypeAPIView(generics.GenericAPIView):
    output_serializer_class = None

    def get_input_serializer(self, *args, **kwargs):
        """
        Return the input serializer instance.
        """
        serializer_class = self.get_input_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_input_serializer_class(self):
        return self.get_serializer_class()

    def get_output_serializer(self, *args, **kwargs):
        """
        Return the output serializer instance.
        """
        serializer_class = self.get_input_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_input_serializer_class(self):
        return self.get_serializer_class()
