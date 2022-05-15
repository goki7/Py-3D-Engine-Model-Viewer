from object_3d import *
from camera import *
from projection import *
import pygame as pg

class SoftwareRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 720, 440
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, np.array([-5, -5, -55]))
        self.projection = Projection(self)
        self.object = self.get_object_from_file("models/FinalBaseMesh.obj")
        self.object.rotate_y(-np.pi / 4)

    def get_object_from_file(self, file_name):
        vertices, faces = [], []
        with open(file_name) as file:
            for line in file:
                if line.startswith("v "):
                    vertices.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith("f "):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split("/")[0]) - 1 for face_ in faces_])
        return Object3D(self, vertices, faces)

    def draw(self):
        self.screen.fill(pg.Color("darkslategray"))
        self.object.draw()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            #pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    app = SoftwareRender()
    app.run()