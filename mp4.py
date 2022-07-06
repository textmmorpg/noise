# python3.7
import os
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx

# write initial video
os.system("ffmpeg -r 1 -i images/result%01d.jpg -vcodec mpeg4 -y movie.mp4")

# speed up video

in_loc = 'movie.mp4'
out_loc = 'noise.mp4'

# Import video clip
clip = VideoFileClip(in_loc)
print("fps: {}".format(clip.fps))

# Modify the FPS
clip = clip.set_fps(clip.fps * 10)

# Apply speed up
final = clip.fx(vfx.speedx, 10)
print("fps: {}".format(final.fps))

# Save video clip
final.write_videofile(out_loc)
