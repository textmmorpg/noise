# python3.7
import os
from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx
import glob
from PIL import Image
def make_gif(frame_folder):
    images = glob.glob(f"{frame_folder}/*.jpg")
    images.sort()
    frames = [Image.open(image) for image in images]
    frames[0].save("noise2.gif", format="GIF", append_images=frames[1:],
                   save_all=True, duration=100, loop=0)

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

# make gif
# make_gif("images")
