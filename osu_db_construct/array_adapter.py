from construct import Adapter


class ArrayAdapter(Adapter):
    def __init__(self, subcon, array_name_length_dict, only_one_field=False):
        super().__init__(subcon)
        self.array_name_length_dict = array_name_length_dict
        self.only_one_field = only_one_field

    def _decode(self, obj, context, path):
        if self.only_one_field:
            array_name = next(iter(self.array_name_length_dict.keys()))
            return obj[array_name]
        return obj

    def _encode(self, obj, context, path):
        if self.only_one_field:
            array_name, array_length = next(iter(self.array_name_length_dict.items()))
            return {array_name: obj, array_length: len(obj)}
        for array_name, array_length in self.array_name_length_dict.items():
            obj[array_length] = len(obj[array_name])
        return obj
