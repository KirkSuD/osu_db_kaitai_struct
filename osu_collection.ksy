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
doc: |
  collection.db file format in rhythm game osu!,
  the legacy DB file structure used in the old osu stable client (not lazer).

  DB files are in the `osu-stable` installation directory:
  Windows: `%localappdata%\osu!`
  Mac OSX: `/Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/`

  Unless otherwise specified, all numerical types are stored little-endian.
  Integer values, including bytes, are all unsigned.
  UTF-8 characters are stored in their canonical form, with the higher-order byte first.

  collection.db contains the user's beatmap collection data.
  This file can be transferred from one osu! installation to another.
  However, this will not work if the PC does not have all of the collected beatmaps installed.
doc-ref: https://github.com/ppy/osu/wiki/Legacy-database-file-structure
seq:
  - id: version
    type: u4
    doc: Int, Version (e.g. 20150203)
  - id: num_collections
    type: u4
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
        type: u4
        doc: Int, Number of beatmaps in the collection
      - id: beatmaps_md5s
        type: string
        repeat: expr
        repeat-expr: num_beatmaps
        doc: String*, Beatmap MD5 hash. Repeated for as many beatmaps as are in the collection.
  string:
    doc: |
      Has three parts; a single byte which will be either 0x00, indicating that
      the next two parts are not present, or 0x0b (decimal 11), indicating that
      the next two parts are present.
      If it is 0x0b, there will then be a ULEB128, representing the byte length
      of the following string, and then the string itself, encoded in UTF-8.
      See https://en.wikipedia.org/wiki/UTF-8.
    seq:
      - id: is_present
        type: u1
      - id: len_str
        type: vlq_base128_le
        if: is_present == 0x0b
      - id: value
        size: len_str.value
        type: str
        if: is_present == 0x0b
