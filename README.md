# Osu DB Kaitai Struct

Rhythm game [osu!](https://osu.ppy.sh) [database](https://github.com/ppy/osu/wiki/Legacy-database-file-structure) parser & serializer.  
(For the old *stable* client, not lazer.)  
(Files: `osu!.db`, `collection.db`, `scores.db`)

## Archived

Last update is for v20250108, last tested on v20250401.

## Parser

Parser is written in [Kaitai Struct](https://kaitai.io/) `.ksy` yaml file according to [osu wiki page](https://github.com/ppy/osu/wiki/Legacy-database-file-structure),  
then transpiled to many programming languages.

Precompiled code is released. (Version is the version of osu!.)  
To compile manually, [install `kaitai-struct-compiler`](https://kaitai.io/#download),  
then run `kaitai-struct-compiler --target all --outdir ./osu_db_kaitai *.ksy`.

Some languages need runtime library to run the compiled parser.  
Please refer to [Kaitai Struct documentation](https://doc.kaitai.io/).  
For example, Python: `pip install kaitaistruct`
```py
from osu_db import OsuDb
osu_data = OsuDb.from_file(osu_db_path)
print(osu_data.osu_version)  # 20250108
```

Bool & String are user-defined types. Use `.value` to access.
```py
>>> scores_data.beatmaps[0].scores[0].perfect_combo
<osu_scores.OsuScores.Bool object at 0x...>
>>> scores_data.beatmaps[0].scores[0].perfect_combo.value
True
```

## Serializer

I compiled `.ksy` to [Python Construct](https://github.com/construct/construct),  
then edited the code manually to make it work.

This is the best solution I know.  
As of this writing, Kaitai Struct's compiled code for Python Construct is not good.  
It's missing some things, and the [CI test rating](https://ci.kaitai.io/) for Construct is <50%.  
Another possible solution is to use the [experimental serialization feature](https://doc.kaitai.io/serialization.html) (Python & Java),  
but it's immature, not included in released compiler, still in its own branch.

To use Construct, which can both parse and serialize,  
download/clone this repo (get the `osu_db_construct` folder),  
`pip install construct`,  
```py
from osu_db import osu_db
osu_data = osu_db.parse_file(osu_db_path)
print(osu_data.osu_version)  # 20250108
osu_binary_data = osu_db.build(osu_data)
```

Types are more "flat", `.value` is no longer needed,  
because I wrote [`Adapter`s](https://construct.readthedocs.io/en/latest/adapters.html) to handle them:
```py
>>> scores_data.beatmaps[0].scores[0].perfect_combo  # no `.value`
True
>>> osu_data.beatmaps[0].star_rating_osu  # no `.pairs`
[...]
```

When serializing, you don't have to specify list length like `num_beatmaps`,  
`ArrayAdapter` sets it for you behind the scene. Example:  
```py
collection_binary = osu_collection.build(dict(
    version=20250108,
    collections=[dict(
        name="my collection",
        beatmaps_md5s=["deadbeefcafebabe"]
    )]
))  # no `num_collections`
```

## Playlist Converter

A CLI playlist converter `playlist.py` is included in `osu_db_construct`.  
By default, it converts all collections to `.pls` playlist files,  
saving to `osu_collection_playlist` folder.  
`python playlist.py -h` to see all options. (`.m3u8` is also supported.)

## Bugs

If you found something wrong, maybe the [DB structure](https://github.com/ppy/osu/wiki/Legacy-database-file-structure) changed,  
please create an issue to let me know.
