
class Element:
    def __init__(self, attrs):
        self.attributes = attrs

    @property
    def dataset(self):
        def strip_data(key):
            return key.split('-')[1]

        _dataset = {
            strip_data(key): value for key, value in self.attributes.items()
            if key.startswith('data-')
        }
        return _dataset
