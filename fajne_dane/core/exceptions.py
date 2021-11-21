
class NotSupported(Exception):
    def __init__(self, msg='Operation is not supported.', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
