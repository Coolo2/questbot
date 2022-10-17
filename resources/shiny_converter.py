
# Temporary file.

from PIL import Image, ImageSequence
import math


def get_output(background : Image.Image):

    bg = background
    animated_sparkle = Image.open('resources/shiny_sparkle.gif')

    background = Image.new("RGBA", animated_sparkle.size)
    if bg.width > bg.height:
        new_h = int(abs((bg.height / bg.width) * background.width))
        bg = bg.resize((background.width, new_h),Image.ANTIALIAS)
    elif bg.width < bg.height:
        new_w = int(abs((bg.width / bg.height) * background.height))
        bg = bg.resize((new_w, background.height),Image.ANTIALIAS)
    else:
        bg = bg.resize(background.size,Image.ANTIALIAS)

    background.paste(bg, mask=bg)

    frames = []
    final_frame_count = math.lcm(1, animated_sparkle.n_frames)
    print(final_frame_count)
    for i in range(final_frame_count):
        animated_sparkle.seek(i % animated_sparkle.n_frames)
        
        frame = background.copy()
        frame.paste(animated_sparkle, (0,0), mask=animated_sparkle.convert("RGBA"))
        frames.append(frame)
    frames[0].save("output.gif", save_all=True, duration=100, loop=0, append_images=frames[1:], disposal=2)

    return frames[0]