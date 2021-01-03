#-*-coding:utf-8;-*-

from osu_db import OsuDb
from osu_collection import OsuCollection
from osu_scores import OsuScores
from vlq_base128_le import VlqBase128Le

if __name__ == "__main__":
    ## simple testing code, set path accordingly before running

    ## your osu root path
    osu_root_path = r"%localappdata%/osu!"
    ## 2 folders to save output files
    output_json_path = r"./exported_json"
    output_serialized_path =  r"./serialized_db" ## should be completely same as original db

    import time, json, os, pickle

    def pkl_dump(obj, fpath):
        with open(fpath, "wb") as f:
            pickle.dump(obj, f)

    pjoin = os.path.join ## shortcut

    osu_root_path = os.path.expandvars(osu_root_path) ## https://stackoverflow.com/questions/53112401/percent-signs-in-windows-path
    osu_db_path = pjoin(osu_root_path, "osu!.db")
    collection_db_path = pjoin(osu_root_path, "collection.db")
    scores_db_path = pjoin(osu_root_path, "scores.db")

    output_json_path = os.path.abspath(os.path.realpath(output_json_path))
    osu_json = pjoin(output_json_path, "osu!.json")
    collection_json = pjoin(output_json_path, "collection.json")
    scores_json = pjoin(output_json_path, "scores.json")

    output_serialized_path = os.path.abspath(os.path.realpath(output_serialized_path))
    osu_serialized = pjoin(output_serialized_path, "osu!.db")
    collection_serialized = pjoin(output_serialized_path, "collection.db")
    scores_serialized = pjoin(output_serialized_path, "scores.db")

##    def trans(s):
##        t, d = s.strip().split(" \t", maxsplit=1)
##        print("- id:", d)
##        print("  type:", {"String": "string", "Short": "s2", "Boolean": "bool", "Long": "s8", "Byte": "s1", "Int": "s4", "Double": "f8"}[t])
##        print("  doc:", t+",", d)
##    while True:
##        s=input("")
##        if s: trans(s)
##        else: break
    
    input("Press ENTER...")

    st = time.time()
    osu_data = OsuDb.from_file(osu_db_path)
    print(osu_data.osu_version)
    print("Parsed osu!.db in", time.time()-st, "sec")

    st = time.time()
    collection_data = OsuCollection.from_file(collection_db_path)
    print(collection_data.version)
    print("Parsed collection.db in", time.time()-st, "sec")

    st = time.time()
    scores_data = OsuScores.from_file(scores_db_path)
    print(scores_data.version)
    print("Parsed scores.db in", time.time()-st, "sec")



