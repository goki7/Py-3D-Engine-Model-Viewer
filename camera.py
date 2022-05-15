import pygame as pg
from matrix_functions import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0]) # unpuck position tuple
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.horizontal_fov = np.pi / 3
        self.vertical_fov = self.horizontal_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.02
        self.rotation_speed = 0.01

    def control(self):
        key = pg.key.get_pressed()
        
        # object motion
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:
            self.position += self.up * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.up * self.moving_speed
        
        # camera translation
        if key[pg.K_q]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_e]:
            self.position += self.forward * self.moving_speed

        # camera rotation
        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)
    
    def camera_yaw(self, angle):
        rotate = rotate_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_pitch(self, angle):
        rotate = rotate_x(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def translation_matrix(self):
        x, y, z, w = self.position

        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotation_matrix(self):
        r_x, r_y, r_z, w = self.right
        f_x, f_y, f_z, w = self.forward
        u_x, u_y, u_z, w = self.up

        return np.array([
            [r_x, u_x, f_x, 0],
            [r_y, u_y, f_y, 0],
            [r_z, u_z, f_z, 0],
            [0, 0, 0, 1]
        ])

    def camera_matrix(self):
        return self.translation_matrix() @ self.rotation_matrix()
        