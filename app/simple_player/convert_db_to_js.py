#-*-coding:utf-8;-*-

"""
OsuMusicPlayer - A music player for osu!, parse osu!.db, collection.db,
 then make json to form a static web music player.
Use the Kaitai Struct osu db parser.

Version 0.0
Roughly tested @ 2019/08/22
with osu!.db ver.20190816, collection.db ver.20190808.

osu! directory path:
Windows: %localappdata%/osu!
Mac OSX: /Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/
"""

from osu_db import OsuDb
from osu_collection import OsuCollection

def list_folders(path):
    for _, folders, _ in os.walk(path):
        return folders

def get_song_from_beatmap(beatmap):
    return {
        "artist": beatmap.artist_name.value,
        "title": beatmap.song_title.value,
        "file": beatmap.audio_file_name.value,
        "folder": beatmap.folder_name.value
    }

def get_songs(beatmaps):
    """
    Generate a list of songs without duplication.
    """
    folders = set()
    res = []
    for bm in beatmaps:
        if bm.folder_name.value in folders:
            continue
        folders.add(bm.folder_name.value)
        res.append(get_song_from_beatmap(bm))
    return res

def generate_md5_to_song_dict(beatmaps):
    """
    Generate a dict from md5 to song with duplications.
    Used by md5_to_song_dict of get_songs_from_md5().
    """
    res = {}
    for bm in beatmaps:
        if bm.md5_hash.value in res:
            raise ValueError("generate_md5_to_song_dict(beatmaps): md5 collision: " + bm.md5_hash)
        res[bm.md5_hash.value] = get_song_from_beatmap(bm)
    return res

def get_songs_from_md5(md5_to_song_dict, md5_list):
    """
    Generate a list of songs from a given md5_list by using md5_to_song_dict.
    """
    folder_set = set()
    res = []
    for md5 in md5_list:
        song = md5_to_song_dict[md5.value]
        if song["folder"] in folder_set:
            continue
        folder_set.add(song["folder"])
        res.append(song)
    return res

def get_collections(beatmaps, collections):
    """
    Convert collections md5 to song.
    """
    md5_to_songs = generate_md5_to_song_dict(beatmaps)
    return [[col.name.value, get_songs_from_md5(md5_to_songs, col.beatmaps_md5s)] for col in collections]

def get_current_time():
    return datetime.datetime.now()

def get_time_str(t=None):
    if t == None:
        t = get_current_time()
    return t.strftime("%Y/%m/%d-%H:%M:%S")

if __name__ == "__main__":
    osu_root_path = r"%localappdata%/osu!"
    copy_db_path = r"./user_data/copied_osu_db"
    osudb_js_path = r"./user_data/osudb.js"

    import os, shutil, json, datetime

    pjoin = os.path.join ## shortcut

    osu_root_path = os.path.expandvars(osu_root_path) ## https://stackoverflow.com/questions/53112401/percent-signs-in-windows-path
    copy_db_path = os.path.abspath(os.path.realpath(copy_db_path)) ## https://stackoverflow.com/questions/37863476/why-would-one-use-both-os-path-abspath-and-os-path-realpath
    osudb_js_path = os.path.abspath(os.path.realpath(osudb_js_path))
    osu_songs_path = pjoin(osu_root_path, "Songs")

    print("osu! root path:", osu_root_path)
    print("osu! songs path:", osu_songs_path)
    print("Copy databases to:", copy_db_path)
    print("osudb.js path:", osudb_js_path)
    input("Press ENTER to continue...")

    print()
    print("Copying osu!.db and collection.db...")
    os.makedirs(copy_db_path, exist_ok = True)
    osu_load_time = get_current_time()
    shutil.copyfile(pjoin(osu_root_path, "osu!.db"), pjoin(copy_db_path, "osu!.db"))
    shutil.copyfile(pjoin(osu_root_path, "collection.db"), pjoin(copy_db_path, "collection.db"))
    print("Copied.")

    print()
    print("Parsing databases...")
    osu_data = OsuDb.from_file(pjoin(copy_db_path, "osu!.db"))
    collection_data = OsuCollection.from_file(pjoin(copy_db_path, "collection.db"))
    print("Parsed.")

    print()
    print("osu!.db basic information: ")
    print(f"Version: {osu_data.osu_version}")
    print(f"Folders: {osu_data.folder_count}")
    print(f"Account unlocked: {osu_data.account_unlocked.value}")
    print(f"Unlock time: {osu_data.account_unlock_date}")
    print(f"Player name: {osu_data.player_name.value}")
    print(f"Beatmaps: {osu_data.num_beatmaps}")

    print()
    print("collection.db basic information:")
    print(f"Version: {collection_data.version}")
    print(f"Collections: {collection_data.num_collections}")

    """
    ## Commented for clear view
    print()
    print("Collections (beatmaps count):")
    for col in collection_data.collections:
        print(f"{col.name} ({col.num_beatmaps})")
    """

    print()
    print("Folders not in osu!.db:")
    db_folder_names = {bm.folder_name.value for bm in osu_data.beatmaps}
    for i in sorted(set(list_folders(osu_songs_path)) - db_folder_names):
        print(i)

    print()
    md5_count = len({bm.md5_hash.value for bm in osu_data.beatmaps})
    if md5_count != osu_data.num_beatmaps: ## collision
        print("MD5 collision found!")
        print(f"Beatmaps: {osu_data.num_beatmaps} / MD5: {md5_count}")
    else:
        print("No MD5 collision found.")

    print()
    print("Dump to json to osudb.js...")
    wf = open(osudb_js_path, "w")
    wf.write("var osuLoaded = true;\n\n")
    wf.write("var osudbJsLoaded = true;\n\n")
    wf.write(f'var osuLoadTime = "{get_time_str(osu_load_time)}";\n\n')
    wf.write(f'var osuSongsPath = {json.dumps("file://"+osu_songs_path)};\n\n')
    wf.write(f"var osuSongs = {json.dumps(get_songs(osu_data.beatmaps))};\n\n")
    wf.write(f"var osuCollections = {json.dumps(get_collections(osu_data.beatmaps, collection_data.collections))};\n")
    wf.close()
    input("Done!")
