import os

os.system("ffmpeg -r 1 -i images/result%01d.jpg -vcodec mpeg4 -y movie.mp4")
