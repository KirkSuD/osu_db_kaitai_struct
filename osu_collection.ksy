meta:
  id: osu_collection
  title: collection.db in osu!
  application: osu!
  file-extension: db
  ks-version: 0.7
  imports:
    - vlq_base128_le
  encoding: UTF-8
  endian: le
doc: collection.db file format in rhythm game, osu!.
doc-ref: https://github.com/ppy/osu/wiki/Legacy-database-file-structure
seq:
  - id: version
    type: s4
    doc: Int, Version (e.g. 20150203)
  - id: num_collections
    type: s4
    doc: Int, Number of collections
  - id: collections
    type: collection
    repeat: expr
    repeat-expr: num_collections
types:
  collection:
    seq:
      - id: name
        type: string
        doc: String, Name of the collection
      - id: num_beatmaps
        type: s4
        doc: Int, Number of beatmaps in the collection
      - id: beatmaps_md5s
        type: string
        repeat: expr
        repeat-expr: num_beatmaps
        doc: String*, Beatmap MD5 hash. Repeated for as many beatmaps as are in the collection.
  string:
    seq:
      - id: is_present
        type: s1
      - id: len_str
        type: vlq_base128_le
        if: is_present == 0x0b
      - id: value
        size: len_str.value
        type: str
        if: is_present == 0x0b
