import numpy as np
from PIL import Image, ImageSequence

# this needs commenting
def normalize_grayscale(image, level=2, distribute=1, pixel_offset=0, 
    stretch=False, invert=False
):
    image_max = image.max()
    if stretch:
        image = np.interp(image, 
            (image.min(), image_max), 
            (0, 255)
        )
        image_max = 255
    
    image = np.divide(image, image_max)
    threshold = 1 / level / distribute
    np.divide(image, threshold, out=image)
    np.floor(image, out=image)
    np.clip(image, a_min=0, a_max=level-1, out=image)
    np.divide(image, image.max(), out=image)
    np.multiply(image, image_max, out=image)
    np.add(image, pixel_offset, out=image)
           
    if invert: np.add(np.negative(image), image_max, out=image) 
    return image

def normalize_video(path, out, level=2, distribute=1, pixel_offset=0, 
    stretch=False, invert=False
):
    gif = Image.open(path)

    # Initialize a list to store the grayscale frames
    modified_frames = []

    for frame in ImageSequence.Iterator(gif):
        # Convert the current frame to grayscale
        grayscale_frame = frame.convert("L")
        # Convert the grayscale frame to a NumPy array
        numpy_frame = np.array(grayscale_frame)
        numpy_frame = normalize_grayscale(numpy_frame, 
            level=level, 
            distribute=distribute, 
            pixel_offset=pixel_offset, 
            stretch=stretch, 
            invert=invert
        )
        image_frame = Image.fromarray(numpy_frame)

        # Append the NumPy array to the list
        modified_frames.append(image_frame)

    modified_frames[0].save(
        out,
        save_all=True,
        append_images=modified_frames[1:],
        duration=gif.info.get('duration', []),
        loop=gif.info.get('loop', 0)
    )