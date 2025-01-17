from construct import Struct, LazyBound, Array, Int32ul, this
from osu_string import osu_string
from array_adapter import ArrayAdapter

osu_collection__collection = Struct(
    'name' / LazyBound(lambda: osu_string),
    'num_beatmaps' / Int32ul,
    'beatmaps_md5s' / Array(this.num_beatmaps, LazyBound(lambda: osu_string)),
)

osu_collection = Struct(
    'version' / Int32ul,
    'num_collections' / Int32ul,
    'collections' / Array(this.num_collections, LazyBound(lambda: osu_collection__collection)),
)

osu_collection__collection = ArrayAdapter(
    osu_collection__collection, {"beatmaps_md5s": "num_beatmaps"})
osu_collection = ArrayAdapter(osu_collection, {"collections": "num_collections"})

if __name__ == "__main__":
    import unittest
    from path_util import get_osu_dir

    file_path = get_osu_dir() / "collection.db"
    with open(file_path, "rb") as file:
        data = file.read()

    class CollectionTestCase(unittest.TestCase):
        def test_round_trip(self):
            parsed = osu_collection.parse(data)
            built = osu_collection.build(parsed)
            self.assertEqual(data, built)

        def test_build_dummy(self):
            test_data = dict(
                version=20250108,
                collections=[dict(
                    name="my collection",
                    beatmaps_md5s=["deadbeef"]
                )]
            )
            built = osu_collection.build(test_data)
            parsed = osu_collection.parse(built)
            built_again = osu_collection.build(parsed)
            self.assertEqual(built, built_again)

    unittest.main()
