codec = ""

import os
import sys

#https://phoenixnap.com/kb/ffmpeg-windows

if os.name == "nt":
    catcmd = "type"
    os.system("if not exist videos mkdir videos")
    os.system("if not exist audios mkdir audios")
else:
    catcmd = "cat"
    os.system("mkdir -p videos && mkdir -p audios")

start = int(int(input("Start value? "))/3.84) # 435274677
end = int(int(input("End value? "))/3.84) # 435274707

os.system("curl -o videos/video.init https://vs-cmaf-push-uk-live.akamaized.net/x=3/i=urn:bbc:pips:service:bbc_news_channel_hd/v=pv14/b=5070016/segment.init")
os.system("curl -o audios/audio.init https://vs-cmaf-push-uk-live.akamaized.net/x=3/i=urn:bbc:pips:service:bbc_news_channel_hd/a=pa3/b=96000/segment.init")

print("----DOWNLOADING VIDEO SEGMENTS----")
os.chdir("videos")
for i in range(int(start), int(end)+1):
    os.system("curl -o %s.m4s https://vs-cmaf-push-uk-live.akamaized.net/x=3/i=urn:bbc:pips:service:bbc_news_channel_hd/t=3840/v=pv14/b=5070016/%s.m4s" % (str(i), str(i)))
os.chdir("..")

print("----DOWNLOADING AUDIO SEGMENTS----")
os.chdir("audios")
for i in range(int(start), int(end)+1):
    os.system("curl -o %s.m4s https://vs-cmaf-push-uk-live.akamaized.net/x=3/i=urn:bbc:pips:service:bbc_news_channel_hd/t=3840/a=pa3/b=96000/%s.m4s" % (str(i), str(i)))
os.chdir("..")

final_vids = ["video.init"]
final_ads = ["audio.init"]

print("----COMBINING VIDEO SEGS----")
for i in range(int(start), int(end)+1):
    final_vids.append(f"{str(i)}.m4s")
os.chdir("videos")
os.system("%s %s > ../final_vid.m4s" % (catcmd, " ".join(final_vids)))
os.chdir("..")

print("----COMBINING AUDIO SEGS----")
for i in range(int(start), int(end)+1):
    final_ads.append(f"{str(i)}.m4s")
os.chdir("audios")
os.system("%s %s > ../final_ads.m4s" % (catcmd, " ".join(final_ads)))
os.chdir("..")

print("----ENCODING VIDEO----")
if codec == "copy":
    os.system("ffmpeg -i final_vid.m4s -c copy final_vid.mp4")
else:
    os.system("ffmpeg -i final_vid.m4s -c:v libx264 -crf 18 final_vid.mp4")
# -c:v libx264 -crf 18
print("----ENCODING AUDIO----")
if codec == "copy":
    os.system("ffmpeg -i final_ads.m4s -c copy final_ads.mp4")
else:
    os.system("ffmpeg -i final_ads.m4s final_ads.mp4")

print("----COMBINING AUDIO AND VIDEO----")
os.system("ffmpeg -i final_vid.mp4 -i final_ads.mp4 -c copy final.mp4")

print("Cleaning")

if os.name == "nt":
    os.system("rd /S /Q videos")
    os.system("rd /S /Q audios")
    os.system("del final_vid.m4s")
    os.system("del final_ads.m4s")
    os.system("del final_vid.mp4")
    os.system("del final_ads.mp4")
else:
    os.system("rm -rf videos audios")
    os.system("rm final_vid.m4s final_ads.m4s final_vid.mp4 final_ads.mp4")

print("Done!")
