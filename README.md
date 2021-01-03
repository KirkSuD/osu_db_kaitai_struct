# Osu DB Kaitai Struct

A simple [osu!](https://osu.ppy.sh) parser written in [Kaitai Struct](https://kaitai.io/).

Version: 0.1  
Written by: KirkSuD  
Project started @ 2021/01/03  
Last update @ 2021/01/04  
Current found bugs: None

It is written according to [the osu! wiki page](https://osu.ppy.sh/help/wiki/osu!_File_Formats/Db_(file_format)).  
Currently, there are 4 databases: osu!.db, scores.db, collection.db, and presence.db.  
But presence.db is not described on the wiki page and is not supported.

Last test: Roughly tested @ 2021/01/04
 with osu!.db ver.20201229, collection.db ver.20200724, scores.db ver.20190828.

osu! directory path:  
Windows: %localappdata%/osu!  
Mac OSX: /Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/

## Requirements

* None. Download latest release from the release folder. Then pick the language you like! :)
* Oh. But you may still have to install Kaitai runtime for your chosen language.

## How to use

Take Python as an example:

```py
from osu_db import OsuDb
osu_data = OsuDb.from_file(osu_db_path)
print(osu_data.osu_version)
```

Yes, it's that easy, yet cross-language. Thanks to Kaitai Struct.

But, I wrote Bool & String as user-defined types; so you have to use `.value` to access real value of Bool or String object. Maybe I'll fix it later...

```py
>>> scores_data.beatmaps[0].md5_hash
<osu_scores.OsuScores.String object at 0x00000237D85D4160>
>>> scores_data.beatmaps[0].md5_hash.value
'3c8b50ebd123458beb39160c6aaf148c'
>>> scores_data.beatmaps[0].scores[0].perfect_combo
<osu_scores.OsuScores.Bool object at 0x00000237D85D43A0>
>>> scores_data.beatmaps[0].scores[0].perfect_combo.value
True
```

## How it works

Write binary format in Kaitai's `.ksy` file, then transpile to real programming languages.

## Related projects

* [osudb](https://github.com/KirkSuD/osudb) is able to parse and serialize osu! databases.
* [OsuMusicPlayer](https://github.com/KirkSuD/OsuMusicPlayer) parses osu! databases and play music for you!

## TODO

* Remove the need of `.value`; or, prove it's needed.

## Bugs

Currently, there are no bugs found.  
It parsed the DBs successfully on my computer.

However, the databases' format may change, and the current parsing method may fail.  
If you find any bug, please inform me.  
If you think the code can be better, tell me how to do it.  
Or, even better, send me a PR with better code. :)

## Thanks to

* You for testing and using this open source project.
