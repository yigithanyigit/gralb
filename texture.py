from OpenGL.GL import *
import numpy
from OpenGL.GL import *
from PIL import Image


class TextureList:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.textures = []
            self.textures_dict = dict()
            self.initialized = True

    def check(self, file_path):
        if hash(file_path) in self.textures_dict:
            return True
        return False

    def get_texture_id(self, file_path):
        return self.textures_dict[hash(file_path)]

    def add_texture_to_list(self, texture):
        self.textures.append(texture)
        self.textures_dict[hash(texture.file_path)] = texture.id


class Texture:
    def __init__(self, file_path=None):
        self.id = -1
        if file_path is not None:
            # Return
            self.file_path = file_path
            self.id = self.load_texture()
            """
            try:
                self.file_path = file_path
                self.id = self.load_texture(self.file_path)
            except:
                print("Texture must has a valid file/file_path")
                exit()
            """

    def _load_texture(self):
        image = Image.open(self.file_path).transpose(Image.FLIP_TOP_BOTTOM)

        mode = GL_RGBA
        if image.mode == 'RGBA':
            mode = GL_RGBA
        elif image.mode == 'RGB':
            mode = GL_RGB


        texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texID)

        # set texture params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # copy texture data
        glTexImage2D(GL_TEXTURE_2D, 0, mode, image.size[0], image.size[1], 0, mode, GL_UNSIGNED_BYTE,
                     numpy.frombuffer(image.tobytes(), dtype=numpy.uint8))
        glGenerateMipmap(GL_TEXTURE_2D)

        return texID

    def load_texture(self):
        if TextureList().check(self.file_path) is True:
            # Texture is already loaded
            self.id = TextureList().get_texture_id(self.file_path)
        else:
            self.id = self._load_texture()
            TextureList().add_texture_to_list(self)

        return self.id
