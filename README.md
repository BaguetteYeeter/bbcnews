# BBC News Downloader

This program downloads footage from BBC News. To use, run the news.py file. Type in the unix timestamps (https://unixtimestamp.com) of the beginning and end of the clip, and it will download into `final.mp4`.

Requirements: python3.7+, ffmpeg, (and curl on linux)

The program supports Windows 10+, MacOS 10.13+, and most linux distros.

It is recommended to run the program outside of the home folder, because it WILL delete "videos".

The files are saved using the original codec, meaning they will only play in VLC. To disable this behaviour, change `codec = "copy"` to `codec = ""` in news.py. If you change this, it might take longer.

## FAQ

Q: The video is corrupted

A: Try opening them in VLC, if they are still corrupted, raise a github issue. 


Q: There is no final.mp4

A: You most likely don't have ffmpeg installed, and the download process failed.