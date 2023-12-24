import cv2
import numpy as np
import sys
import os
import webcolors
import re

class Canvas:
    def __init__(self, name, H, W, bg:str=None):
        self.canvas_name = name
        self.height = H
        self.width = W
        self.layer_num = 0
        self.layers = []

        if bg == None:
            background = np.zeros((H, W, 4), dtype='uint8')
        else:
            r, g, b = re.findall('=(\d+)', str(webcolors.name_to_rgb(bg)))
            r, g, b = [int(r), int(g), int(b)]
            background = np.zeros((H, W, 4), dtype='uint8')
            background += np.array([b, g, r, 255], dtype='uint8')

        self.add_layer(background, name='background', alpha=1.0)

    def add_layer(self, img, name='Layer', alpha=1.0, format='png'):
        if format == 'png':
            assert img.shape == (self.height, self.width, 4)
            layer_image = img
        elif format == 'jpg' or format == 'jpeg':
            assert img.shape == (self.height, self.width, 3)
            layer_image = cv2.cvtColor(img, code=cv2.COLOR_BGR2BGRA)
        else:
            print("Invalid format.")
        
        self.layers.append({'name':name, 'alpha':alpha, 'image':layer_image})
        self.layer_num += 1

    def info(self):
        print(f"Name:{self.canvas_name}, (H,W)=({self.height},{self.width}), {self.layer_num} Layers")
        for i in range(self.layer_num):
            print(f"{str(i).rjust(len(str(self.layer_num - 1)))} a={self.layers[i]['alpha']:.2f} {self.layers[i]['name']}")

    def get_image(self, format='jpg'):
        assert format == 'jpg' or format == 'jpeg'
        image = np.zeros((self.height, self.width, 3), dtype='uint8')

        for i in range(self.layer_num):
            layer_image = self.layers[i]['image']
            layer_alpha = self.layers[i]['alpha']

            for h in range(self.height):
                for w in range(self.width):
                    alpha = layer_alpha * layer_image[h][w][3] / 255.0
                    image[h][w] = (1 - alpha) * image[h][w] + alpha * layer_image[h][w][:3]

        return image

    def save_image(self, path:str):
        format = os.path.splitext(path)[1][1:]
        assert format == 'jpg' or format == 'jpeg'
        cv2.imwrite(path, self.get_image())
        print(f"Saving the image as \"{path}\".")
