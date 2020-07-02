import pandas as pd
from subprocess import Popen, PIPE
import os
from datetime import datetime

# Abrir último csv
file = "videos.csv"
if os.path.exists(file):
    videos = pd.read_csv(file)
else:
    videos = pd.DataFrame(columns=["date", "computer", "parts_filename", "filename", "size", "duration"])

# Se busca los vídeos a revisar
procesados = set(videos.parts_filename)
total = set(os.listdir(os.path.join(".", "videos", "raw")))
aprocesar = total.difference(procesados)

# Se procesan los vídeos seleccionados
for v in aprocesar:
    try:
        if v.endswith(".tar.gz"):
            name_parts = v.replace(".tar.gz", "").split("-")
            date = str(datetime.fromtimestamp(int(name_parts[0])))
            computer = name_parts[-1]
            name_end = "hubu-fis-"+computer+"_video_"+name_parts[0]+".mp4"
            if name_end in set(videos.filename):
                continue
            #Ejecucion
            p = Popen(["bash", "merge_file.sh", "videos/raw", v, name_end], stdout=PIPE)
            duration = p.communicate()[0].decode('ascii').replace("\n", "")

            size = os.stat(os.path.join(".", "videos","processed",name_end)).st_size
            videos = videos.append(
                {
                    "date": date,
                    "computer": computer,
                    "parts_filename": name_parts,
                    "filename": name_end,
                    "size": size,
                    "duration": duration
                },
                ignore_index=True)
    except:
        print(v,"ha dado error")

print(videos)
videos.to_csv(file, index=False)
