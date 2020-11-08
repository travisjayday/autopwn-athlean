import sys
import json
import re 
import os
import sys
import time
import urllib.request
import random

logfile = open("log/pylog-" + str(time.time()), "a")

def get_page(url): 
    with urllib.request.urlopen(url) as resp:
        return resp.read()

def get_page_as(url, ua):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", ua)
    with urllib.request.urlopen(req) as response:
       return str(response.read(), 'utf-8'), response.info(), response.geturl()

def log(*args):
    s = " ".join(map(str,args))
    print(s)
    logfile.write(s + "\n")
    logfile.flush()
    os.fsync(logfile)

if len(sys.argv) != 1: 
    vid = sys.argv[1]
else:
    f = open("request.log", "r", encoding="utf-8")
    vid = f.read().split("<id>yt:video:")[-1].split("</id")[0]
    f.close()

log("Targeting video", vid)
if len(vid) > 20: 
    log("not a valid video")
    quit()

current = ""
try: 
    f = open("target.vid", "r")
    current = f.read()
except: 
    pass

if vid in current: 
    log("Already targeting video, so exiting...")
    quit()

f = open("target.vid", "w")
f.write(vid)
f.close()

api = "GOOGLE_API_KEY" 
s = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={}&key={}".format(vid, api)

r = str(get_page(s), 'utf-8')
r = json.loads(r)

duration = 15 * 60  # hammer for 10 minutes
start_t = time.time()

foundcomment = False
won = False
uai = 0
while foundcomment == False: 
    for comment in r["items"]:
        author = comment["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        content = comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        if "ATHLEAN-X" in author: 
            foundcomment = True
            url = content.split("href=\"")[1].split("\"")[0]
            log("extractd url", url)
            while not won and time.time() - start_t < duration: 
                try: 
                    uai += 1

                    agent = str(random.random())
                    log("making request with user agent: ", agent)
                    page, info, resp_url = get_page_as(url, agent)

                    if "please try again next time" in page.lower(): 
                        log("Failed...")
                    elif "this giveaway has expired" in page.lower(): 
                        log("Expired...")
                    else:
                        log(resp_url)
                        log(page)
                        log(agent)
                        log(info)
                        f = open("success", "w")
                        f.write(str(info) + '\n')
                        f.write(str(agent) + "\n---\n")
                        f.write(str(page))
                        f.close()
                        won = True
                except:
                    pass
                time.sleep(.2)
    if won == False:
        log("Failed to find comment...")
    if uai >= 3000:  # 10 minutes later
        log("Giving up. Exausted UAS")
        quit()
    time.sleep(10)

