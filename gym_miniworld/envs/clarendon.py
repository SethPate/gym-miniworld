import numpy as np
import math
from gym import spaces
from ..miniworld import MiniWorldEnv, Room
from ..entity import ImageFrame, MeshEnt, Box, Key, Ball, COLOR_NAMES
from time import sleep

class Clarendon(MiniWorldEnv):
    """
    What, cause I been in the lab,
    with a pen and a pad,
    tryna get this damn label off?
    """

    def __init__(self, **kwargs):
        super().__init__(
            max_episode_steps=2000,
            **kwargs
        )

        # Allow only the movement actions
        self.action_space = spaces.Discrete(self.actions.move_forward+1)

        self.refreshrate = 1 / 10

    def run(self):
        while True:
            event = self.dispatch_events()
            sleep(1.0/self.refreshrate)


    def _gen_world(self):
        con = 'concrete'
        cont = 'concrete_tiles'
        ft = 'floor_tiles_bw'
        # room x,x,z,z
        coords = [
            (0,5,0,4, 'grass','cinder_blocks','concrete_tiles',True),
            (0,3,4,6, 'grass','cinder_blocks','ceiling_tiles',True),
            (2,3,6,7, 'grass','cinder_blocks',cont,True),
            (3,5,4,7, 'wood_planks','brick_wall','wood_planks',False),
            (3,5,7,9,'wood_planks','brick_wall','wood_planks',False),
            (0,3,7,9,'wood','drywall','wood_planks',False),
            (0,8,9,14,'wood','brick_wall','wood_planks',False),
            (2,8,14,19,'wood','brick_wall','wood_planks',False),
            (4,8,19,21,'wood','brick_wall','wood_planks',False),
            (8,13,8,18,'grass','cinder_blocks',cont,True),
            (8,21,18,21,'grass','cinder_blocks',cont,True),
            (13,16,13,18,'water','marble',cont,True),
            (13,16,11,13,'grass','cinder_blocks',cont,True),
            (16,21,8,18,'grass','cinder_blocks',cont,True),
            (21,25,14,21,ft,'brick_wall','drywall',False),
            (25,27,15,17,'wood','brick_wall','drywall',False),
            (21,25,12,14,'wood_planks','brick_wall',cont,False),
            (21,25,9,12,ft,'brick_wall',cont,False),
            (25,29,9,15,'wood_planks','drywall','stucco',False),
            (25,27,7,9,'wood','drywall','stucco',False),
            (27,29,7,9,'wood_planks','drywall','stucco',False),
            (25,27,4,7,'wood','drywall','stucco',False),
            (27,29,4,7,'wood_planks','drywall','stucco',False),
            (25,29,0,4,'wood_planks','brick_wall','stucco',False)
        ]

        coords = [(x[0],x[1],-x[3],-x[2],x[4],x[5],x[6],x[7]) for x in coords]

        rooms = []

        for ix, room in enumerate(coords):
            x1,x2,z1,z2,f,w,c,ce = room
            rooms.append(self.add_rect_room(
                min_x=x1, max_x=x2,
                min_z=z1, max_z=z2,
                floor_tex=f,
                wall_tex=w,
                ceil_tex=c,
                no_ceiling=ce
            ))

        # Connect the rooms with portals/openings
        raw_connections = [
            (False, 1, 2, 0, 2),
            (False,1,4,3,5),
            #(True,3,4,5,7),
            (False,4,5,3,5),
            (False,5,7,3,5),
            (False,6,7,0,2),
            (True,7,10,9,11),
            (True,8,10,15,17),
            (True,9,11,19,21),
            (False,8,9,4,8),
            (False,11,12,13,16),
            (True,10,13,11,13),
            (True,13,14,11,13),
            (True,11,15,19,21),
            (True,14,15,14,16),
            (True,15,16,15,17),
            (False,15,17,22,24),
            (False,17,18,21,23),
            (True,17,19,12,14),
            (True,18,19,9,11),
            (False,19,20,25,27),
            (False,19,21,27,29),
            (True,23,22,5,7),
            (False,21,23,27,29),
            (False,23,24,27,29),
        ]

        connections = []
        for c in raw_connections:
            if c[0]:
                new = (True,c[1],c[2],-c[4],-c[3])
                connections.append(new)
            else:
                connections.append(c)

        for ix, pos in enumerate(connections):
            vertical, r1, r2, x1, x2 = pos
            r1 -= 1
            r2 -= 1
            if vertical:
                self.connect_rooms(rooms[r1], rooms[r2], min_z=x1, max_z=x2)
            else:
                self.connect_rooms(rooms[r1], rooms[r2], min_x=x1, max_x=x2)

        hor = math.pi/2
        ver = math.pi

        # x,y,z, orientation, width, name

        mid = 1.35

        paintings = [
            ([3,mid,-8], ver, 1, 'byron'),
            ([3,mid,-5], ver, 1, 'adelaide_hanscom'),
            #([3,mid,-5], ver, 1, 'alessandro_allori'),
            ([4,mid,-14], hor, 1, 'alexandre_cabanel'),
            ([2,mid,-15], ver, 1, 'alexei_harlamov'),
            ([10,mid,-18], hor, 1, 'alexey_petrovich_antropov'),
            ([10,mid,-8], hor, 1, 'alice_pike_barney'),
            ([18,mid,-18], hor, 1, 'aman_theodor'),
            ([18,mid,-8], hor, 1, 'antonello_messina'),
            ([26,mid,-17], hor*3, 1, 'antonio_herrera_toro'),
            ([24,mid,-12], hor*3, 1, 'cramacj_lucas'),
            ([26,mid,-7], hor*3, 1, 'alexei_harlamov'),
            ([26,mid,-7], hor, 1, 'benjamin_constant'),
            ([26,mid,-4], hor*3, 1, 'carl_frederic_breda'),
            ]

        for p in paintings:
            pos, d, w, n = p
            self.entities.append(ImageFrame(
                pos=pos,
                dir=d,
                width=w,
                tex_name=n
                ))

        # mesh_name, height
        stuff = [
            ('duckie',1.5),
            ('office_desk',1.25),
            ('barrel',1),
            ('tree',2.5),
            ('tree_pine',2.5),
            ('ball_red',1.5),
            ('cone',1),
            ('key_red',1),
            ('office_chair',1),
            ]

        objects = []

        for s in stuff:
            n,h = s
            objects.append(MeshEnt(
                mesh_name=n,
                height=h)
                )

        # ent, room, pos, dir, x0, x1, z0, x1

        entities = [
            (0, [2,0,-1], hor),
            (7, [4,0,-12], ver),
            (9, [5,0,-19], ver),
            (10, [12,0,-16], ver),
            (14, [17,0,-15], hor),
            (15, [24,0,-20], ver),
            (19, [28,0,-13], ver),
            (24, [26,0,-1], ver),
        ]

        for i, e in enumerate(entities):
            r,p,d = e

            self.place_entity(
                objects[i],
                pos=p,
                dir=d
                )

        self.place_agent(dir=hor,min_x=28,max_x=29,min_z=0,max_z=-1)

    def step(self, action):
        obs, reward, done, info = super().step(action)

        return obs, reward, done, info
