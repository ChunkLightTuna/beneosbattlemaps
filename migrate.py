#!/usr/bin/python3
import os
import re
import json
import shutil

os.system("git checkout .")

# prepare
TARGET = "maps"
#if os.path.isdir(TARGET):
#  os.system("rm -rf %s" % TARGET)
#os.system("mkdir %s" % TARGET)

##
## extract all mappings
##
mappings = {}
with open("mappings.txt") as f:
  for line in f:
    index = line.split("_")[0]
    mappings[index] = line.strip()

##
## move all videos 03-01_TempleStatue_1-4K_Scen.webm
##
for file in os.listdir("map-assets"):
  if file.endswith(".webm"):
    match = re.match("(\d\d)-(\d\d_.+)-((HD|4K).*)\.webm", file)
    if match:
      index = match.group(1)
      # create folder if not exist
      if not index in mappings:
        print("No match for index %s" % index)
        exit(1)
        
      folder = os.path.join(TARGET, mappings[index], match.group(2))
      if not os.path.isdir( folder ):
        os.system("mkdir -p %s" % folder)
      
      # move file
      os.rename( os.path.join("map-assets", file), os.path.join(folder, "%s.webm" % (match.group(3))) )
        
    else:
      print("No match for %s" % file)
      exit(1)

##
## change all compendium paths
##
packs = ["packs/beneosbattlemapsHD.db", "packs/beneosbattlemapsSceneryHD.db", "packs/beneosbattlemaps4K.db", "packs/beneosbattlemapsScenery4K.db"]
for p in packs:
  content = ""
  with open(p, 'r') as f:
    for line in f:
      
      #re.findall( r'all (.*?) are', 'all cats are smarter than dogs, all dogs are dumber than cats')
      
      #matches = re.findall("\"modules/beneosbattlemaps/map-assets/Map-Sounds_DontChange/([^\"]+)\"", line)
      #if len(matches) > 0:
        #line = re.sub(r"modules/beneosbattlemaps/map-assets/Map-Sounds_DontChange/", "modules/beneosbattlemaps/others/", line)
        #folder = os.path.join(TARGET, mappings[index], mappings[index], "others")
        #if not os.path.isdir( folder ):
          #os.system("mkdir -p %s" % folder)
        #for m in matches:
          #if m == "campfire.mp3":
            #m = "campfire.ogg"
            #line = re.sub(r"campfire.mp3", "campfire.ogg", line)
            
          #shutil.copy("map-assets/Map-Sounds_DontChange/%s" % m, folder)
      
      data = json.loads(line)
        
      if "name" in data and "img" in data:
        match = re.match("modules/beneosbattlemaps/map-assets/(\d\d)-(\d\d_.+)-((HD|4K).*)\.webm", data["img"])
        if match:
          index = match.group(1)
          folder = os.path.join(TARGET, mappings[index], match.group(2))
          file = os.path.join(folder, "%s.webm" % (match.group(3)))
          
          # check that video exists
          if os.path.isfile(file):
            # replace img path and write file
            data["img"] = "modules/beneosbattlemaps/%s" % file
            
            # should not exist!!
            scenePath = os.path.splitext(file)[0] + ".json"
            if os.path.isfile(scenePath):
              print("Scene already exists! %s" % scenePath)
              exit(1)
            
            content += json.dumps(data) + "\n"
            #with open(scenePath, 'w') as out:
            #  json.dump(data, out)
              
          else:
            print("[Not found] %s : %s" % (data["name"], data["img"]))
          
          
        else:
          match = re.match("modules/beneosbattlemaps/(maps/.*\.webm)", data["img"])
          if match and os.path.isfile(match.group(1)):
            content += line
          else:
            print("No match for %s!" % data["img"])
            exit(1)
        
        #print( data["name"], data["img"] )
      
  with open(p, 'w') as f:
    f.write(content)
