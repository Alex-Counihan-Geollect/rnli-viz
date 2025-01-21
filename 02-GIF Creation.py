# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 00:03:09 2022

@author: alexc
"""

import glob
from PIL import Image

image_path = "./images/"


def make_gif(frame_folder):
    frames = [
        Image.open(image) for image in glob.glob(f"{frame_folder}/*.JPG")
    ]
    frame_one = frames[0]
    frame_one.save(
        "rnli.mp4",
        format="mp4",
        append_images=frames,
        save_all=True,
        duration=27.4,
        loop=0,
    )


make_gif(image_path)


duration = 0.01 / 365
