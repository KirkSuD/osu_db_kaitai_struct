#-*-coding:utf-8;-*-

"""
OsuMusicPlayer - A music player for osu!, parse osu!.db, collection.db,
 then make json to form a static web music player.
Required 3rd-party module: osudb

Version 0.0
Written by: KirkSuD
Written @ 2019/08/22
Last modified @ 2019/08/22
Current found bugs: None

Roughly tested @ 2019/08/22
with osu!.db ver.20190816, collection.db ver.20190808.

osu! directory path:
Windows: %localappdata%/osu!
Mac OSX: /Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/
"""

def list_folders(path):
    for _, folders, _ in os.walk(path):
        return folders

def get_song_from_beatmap(beatmap):
    ## return [beatmap[1], beatmap[3], beatmap[7], beatmap[45]] ## no-key, reduce file size

    ## change @ 2020/04/12 due a change in Beatmap Information: Int: Size in bytes of the beatmap entry. Only present if version is less than 20191106.
    ## so beatmap_info[0] disappears, all index has to -1.
    #return {"artist": beatmap[1], "title": beatmap[3], "file": beatmap[7], "folder": beatmap[45]}
    return {"artist": beatmap[0], "title": beatmap[2], "file": beatmap[6], "folder": beatmap[44]}

def get_songs(beatmaps):
    """
    Generate a list of songs without duplication.
    """
    folders = set()
    res = []
    for bm in beatmaps:
        ## change @ 2020/04/12 due a change in Beatmap Information: Int: Size in bytes of the beatmap entry. Only present if version is less than 20191106.
        ## so beatmap_info[0] disappears, all index has to -1.
        #folder_name = bm[45]
        folder_name = bm[44]
        if folder_name in folders: continue
        folders.add(folder_name)
        res.append(get_song_from_beatmap(bm))
    return res

def generate_md5_to_song_dict(beatmaps):
    """
    Generate a dict from md5 to song with duplications.
    Used by md5_to_song_dict of get_songs_from_md5().
    """
    res = {}
    for bm in beatmaps:
        ## change @ 2020/04/12 due a change in Beatmap Information: Int: Size in bytes of the beatmap entry. Only present if version is less than 20191106.
        ## so beatmap_info[0] disappears, all index has to -1.
        #if bm[8] in res: raise ValueError("generate_md5_to_song_dict(beatmaps): md5 collision: "+bm[8])
        if bm[7] in res: raise ValueError("generate_md5_to_song_dict(beatmaps): md5 collision: "+bm[7])
        #res[bm[8]] = get_song_from_beatmap(bm)
        res[bm[7]] = get_song_from_beatmap(bm)
    return res

def get_songs_from_md5(md5_to_song_dict, md5_list):
    """
    Generate a list of songs from a given md5_list by using md5_to_song_dict.
    """
    folder_set = set()
    res = []
    for md5 in md5_list:
        song = md5_to_song_dict[md5]
        ## change @ 2020/04/12 due a change in Beatmap Information: Int: Size in bytes of the beatmap entry. Only present if version is less than 20191106.
        ## so beatmap_info[0] disappears, all index has to -1.
        ## if song[-1] in folder_set: continue ## no-key, reduce file size
        if song["folder"] in folder_set: continue
        ## folder_set.add(song[-1]) ## no-key, reduce file size
        folder_set.add(song["folder"])
        res.append(song)
    return res

def get_collections(beatmaps, collections):
    """
    Convert collections md5 to song.
    """
    md5_to_songs = generate_md5_to_song_dict(beatmaps)
    return [[col[0], get_songs_from_md5(md5_to_songs, col[2])] for col in collections]

def get_current_time():
    return datetime.datetime.now()

def get_time_str(t=None):
    if t == None:
        t = get_current_time()
    return t.strftime("%Y/%m/%d-%H:%M:%S")

if __name__ == "__main__":
    osu_root_path = r"%localappdata%/osu!"
    copy_db_path = r"./copied_osu_db"
    osudb_js_path = r"./osudb.js"

    import osudb ## 3rd-party module for parsing osu! databases

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
    osu_load_time = get_current_time()
    shutil.copyfile(pjoin(osu_root_path, "osu!.db"), pjoin(copy_db_path, "osu!.db"))
    shutil.copyfile(pjoin(osu_root_path, "collection.db"), pjoin(copy_db_path, "collection.db"))
    print("Copied.")

    print()
    print("Parsing databases...")
    osu_data = osudb.parse_osu(pjoin(copy_db_path, "osu!.db"))
    collection_data = osudb.parse_collection(pjoin(copy_db_path, "collection.db"))
    print("Parsed.")

    print()
    print("osu!.db basic information: ")
    print("""Version: %d
Folders: %d
Account unlocked: %s
Unlock time: %d
Player name: %s
Beatmaps: %d""" % tuple(osu_data[:6]))

    print()
    print("collection.db basic information:")
    print("""Version: %d
Collections: %d""" % tuple(collection_data[:2]))

    """
    ## Commented for clear view
    print()
    print("Collections (beatmaps count):")
    for col in collection_data[2]:
        print("%s (%d)" % (col[0], col[1]))
    """

    print()
    print("Folders not in osu!.db:")
    ## change @ 2020/04/12 due a change in Beatmap Information: Int: Size in bytes of the beatmap entry. Only present if version is less than 20191106.
    ## so beatmap_info[0] disappears, all index has to -1.
    #db_folder_names = {bm[45] for bm in osu_data[6]}
    db_folder_names = {bm[44] for bm in osu_data[6]}
    for i in sorted(list(set(list_folders(osu_songs_path))-db_folder_names)):
        print(i)

    print()
    ## change @ 2020/04/12 due a change in Beatmap Information: Int: Size in bytes of the beatmap entry. Only present if version is less than 20191106.
    ## so beatmap_info[0] disappears, all index has to -1.
    #md5_count = len({bm[8] for bm in osu_data[6]})
    md5_count = len({bm[7] for bm in osu_data[6]})
    if md5_count != len(osu_data[6]): ## collision
        print("MD5 collision found!")
        print("Beatmaps: %d / MD5: %d" % (len(osu_data[6]), md5_count))
    else:
        print("No MD5 collision found.")

    print()
    print("Dump to json to osudb.js...")
    wf = open(osudb_js_path, "w")
    wf.write("var osuLoaded = true;\n\n")
    wf.write("var osudbJsLoaded = true;\n\n")
    wf.write('var osuLoadTime = "%s";\n\n' % get_time_str(osu_load_time))
    wf.write('var osuSongsPath = %s;\n\n' % json.dumps("file://"+osu_songs_path))
    wf.write("var osuSongs = "+json.dumps(get_songs(osu_data[6]))+";\n\n")
    wf.write("var osuCollections = "+json.dumps(get_collections(osu_data[6], collection_data[2]))+";\n")
    wf.close()
    input("Done!")

