from construct import (
    Struct, LazyBound, FixedSized, RepeatUntil, Computed, Adapter,
    If, GreedyString, Int8ub, this
)


class vlq_base128_le__Adapter(Adapter):
    def __init__(self):
        super().__init__(Struct(
            'groups' / RepeatUntil(lambda obj_, list_, this: (obj_ & 128) == 0, Int8ub),
            'value' / Computed(lambda this: sum(
                ((group & 127) << (7 * i)) for i, group in enumerate(this.groups)
            )),
        ))

    def _decode(self, obj, context, path):
        return obj["value"]

    def _encode(self, obj, context, path):
        groups = []
        while True:
            groups.append((obj & 127) | (128 if obj > 127 else 0))
            obj >>= 7
            if not obj:
                break
        return dict(groups=groups)


class osu_string__Adapter(Adapter):
    def __init__(self):
        super().__init__(Struct(
            'is_present' / Int8ub,
            'len_str' / If(this.is_present == 11, LazyBound(lambda: vlq_base128_le)),
            'value' / If(
                this.is_present == 11,
                FixedSized(this.len_str, GreedyString(encoding='UTF-8'))
            ),
        ))

    def _decode(self, obj, context, path):
        return obj["value"] if obj["is_present"] else None

    def _encode(self, obj, context, path):
        if obj is None:
            return dict(is_present=0, len_str=None, value=None)
        return dict(is_present=11, len_str=len(obj.encode("utf-8")), value=obj)


vlq_base128_le = vlq_base128_le__Adapter()
osu_string = osu_string__Adapter()


if __name__ == "__main__":
    import unittest

    class VlqTestCase(unittest.TestCase):
        def test_round_trip(self):
            test_numbers = [0, 1, 2, 127, 128, 129, 16383, 16384, 16385]
            for n in test_numbers:
                built = vlq_base128_le.build(n)
                parsed = vlq_base128_le.parse(built)
                self.assertEqual(n, parsed)

    class StringTestCase(unittest.TestCase):
        def test_round_trip(self):
            test_strings = [None, "", "hello"]
            for s in test_strings:
                built = osu_string.build(s)
                parsed = osu_string.parse(built)
                self.assertEqual(s, parsed)

    unittest.main()
