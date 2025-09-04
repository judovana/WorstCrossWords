import sys
import torch
from diffusers import StableDiffusionPipeline
import show_image
from PIL import Image
import time

initialized=False
#do not seem to work - assert len(imgs) == rows*cols
#n_images = 6 # Let's generate 6 images based on the prompt below
n_images=1

def initialize():
    global pipeline
    pipeline = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", torch_dtype=torch.float32)
    #will take ages
    #pipeline = StableDiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", torch_dtype=torch.float16)
    initialized=True


def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols
    w, h = imgs[0].size
    grid = Image.new('RGB', size = (cols*w, rows * w))
    grid_w, grid_h = grid.size
    for i, img in enumerate(imgs):
        grid.paste(img, box = (i%cols*w, i // cols*h))
    return grid


def generateTo(prompt, fileName):
    grid=generateImg(prompt)
    grid.save(fileName)
    return fileName

def generateImg(prompt):
    origPrompt=prompt
    prompt = prompt# + " 16x16px"#thsi will make it usually faster, and really smaller, but increases nonsenseness
    if (not initialized):
        initialize()
    images = pipeline(prompt).images
    grid = image_grid(images, rows=1, cols=1)
    return grid

def generate(prompt):
    fileName="outgen" + str(time.time()) + ".jpg"
    return generateTo(prompt, fileName)

def main():
    if len(sys.argv) != 2:
        print("expects exactly one argument - description sentence")
        sys.exit(1)
    file=generate(sys.argv[1]);
    print("eog " + file)
    show_image.display_image(file)

if __name__ == "__main__":
    main()
