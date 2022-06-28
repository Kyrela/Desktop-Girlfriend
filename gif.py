"""
Store a gif class unsed to manage animated gifs
"""
import os
import sys
from io import BytesIO

from PIL import Image


class Gif:
    """
    A class to manage animated gifs using PIL
    """

    def __init__(self, img: Image.Image | str):
        if isinstance(img, Image.Image):
            self.base_image = img
        else:
            self.base_image = Image.open(img)
        if not self.base_image.is_animated:
            raise ValueError('Not an animated gif')
        self.frames_count = self.base_image.n_frames
        self.loop = self.base_image.info['loop']
        self.size = self.base_image.size
        self.frames = self.get_frames()

    def get_frames(self) -> list[Image]:
        """
        Return a list of frames from the gif

        :return: the frame list
        """
        frames = []

        for i in range(self.frames_count):
            frames.append(self.base_image.copy().convert('RGBA'))
            self.base_image.seek(i)

        self.base_image.seek(0)
        return frames

    def save_frames(self, path: str):
        """
        Save all the gif's frames as separate images

        :param path: the path to save the frames as
        :return: None
        """
        for i in range(self.frames_count):
            self.frames[i].save(
                os.path.join(path, f"frame_{i}.png"))

    def save(self, path: str):
        """
        Save the gif as a new file

        :param path: the path to save the gif as
        :return: None
        """
        self.frames[0].save(path, 'GIF', save_all=True, append_images=self.frames[1:], loop=self.loop, disposal=2)

    def to_bytes(self) -> bytes:
        """
        Return the gif as bytes

        :return: the gif as bytes
        """
        img_bytes = BytesIO()
        self.frames[0].save(img_bytes, 'GIF', save_all=True, append_images=self.frames[1:], loop=self.loop, disposal=2)
        return img_bytes.getvalue()

    def resize(self, size: tuple | int):
        """
        Resize the gif

        :param size: the new size
        :return: self
        """
        if isinstance(size, int):
            size = ((size * self.size[0]) // 100, (size * self.size[1]) // 100)
        self.frames = [frame.resize(size) for frame in self.frames]
        self.size = size
        return self

    def crop(self, box: tuple):
        """
        Crop the gif

        :param box: the crop box
        :return: self
        """
        self.frames = [frame.crop(box) for frame in self.frames]
        return self

    def copy(self):
        """
        Copy the gif

        :return: a copy of the gif
        """
        return Gif(self.base_image)


if __name__ == '__main__':
    gif = Gif(sys.argv[1])
    gif.save_frames(sys.argv[2])
