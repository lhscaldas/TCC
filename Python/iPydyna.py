#!/usr/bin/env python3
import pymoos
import pydyna
import time
import sys
import numpy as np
from MoosReader import MoosReader

class Ship(pymoos.comms):

    def __init__(self, params):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(Ship, self).__init__()
        self.server = 'localhost'
        self.port = int(params['ServerPort'])
        self.name = 'iPydyna'

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)

        self.add_active_queue('desired_queue', self.on_desired_message)
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_ROTATION_1')
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_ROTATION_2')
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_ROTATION_3')
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_RUDDER_1')
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_RUDDER_2')
        
        self.desired_rotation_1 = 0
        self.desired_rotation_2 = 0
        self.desired_rotation_3 = 0
        self.desired_rudder_1 = 0
        self.desired_rudder_2 = 0

        self.real_x = params['START_X']
        self.real_y = params['START_Y']
        self.real_heading = params['START_HEADING']
        self.real_speed = 0
        
        self.sim = pydyna.create_simulation("NACMM_2021.p3d")
        self.ship = self.sim.vessels['292']
        self.rudder1 = self.ship.rudders['0']
        self.rudder2 = self.ship.rudders['1']
        self.propeller1 = self.ship.thrusters['0']
        self.propeller2 = self.ship.thrusters['1']
        self.propeller3 = self.ship.thrusters['4']

        self.ship._set_linear_position([self.real_x, self.real_y, 0])
        if self.real_heading > 270:
            self.ship._set_angular_position([0, 0, np.deg2rad(450 - self.real_heading)])
        elif self.real_heading > 180:
            self.ship._set_angular_position([0, 0, np.deg2rad(360 - self.real_heading)])
        else:
            self.ship._set_angular_position([0, 0, np.deg2rad(90 - self.real_heading)])
        self.ship._set_linear_velocity([0, 0, 0])

        self.rudder1.dem_angle = - self.desired_rudder_1
        self.rudder2.dem_angle = - self.desired_rudder_2
        self.propeller1.dem_rotation = self.desired_rotation_1
        self.propeller2.dem_rotation = self.desired_rotation_2
        self.propeller3.dem_rotation = self.desired_rotation_3

        self.run(self.server, self.port, self.name)
        pymoos.set_moos_timewarp(params['MOOSTimeWarp'])


    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        self.notify('NAV_DEPTH', float(0), -1) # para o visualizador 
        return (self.register('DESIRED_ROTATION_1', 0) and
                self.register('DESIRED_ROTATION_2', 0) and
                self.register('DESIRED_ROTATION_3', 0) and
                self.register('DESIRED_RUDDER_1', 0) and
                self.register('DESIRED_RUDDER_2', 0))

    def __on_new_mail(self):
        """OnNewMail callback"""
        for msg in self.fetch():
            pass
        return True

    def on_desired_message(self, msg):
        if msg.key() == 'DESIRED_ROTATION_1':
            self.desired_rotation_1 = msg.double()
        elif msg.key() == 'DESIRED_ROTATION_2':
            self.desired_rotation_2 = msg.double()
        elif msg.key() == 'DESIRED_ROTATION_3':
            self.desired_rotation_3 = msg.double()
        elif msg.key() == 'DESIRED_RUDDER_1':
            self.desired_rudder_1 = msg.double()
        elif msg.key() == 'DESIRED_RUDDER_2':
            self.desired_rudder_2 = msg.double()
        return True

    def send(self, key, value):
        self.notify(key, value, -1)

    def update(self):
        self.send('REAL_SPEED', self.real_speed)
        self.send('REAL_HEADING', self.real_heading)
        self.send('REAL_X', self.real_x)
        self.send('REAL_Y', self.real_y)
        self.send('REAL_R', self.ship.angular_velocity[2])
        self.send('REAL_V', self.ship.linear_velocity[1])

        self.send('NAV_SPEED', self.real_speed) # para o visualizador 
        self.send('NAV_HEADING', self.real_heading) # para o visualizador 
        self.send('NAV_X', self.real_x) # para o visualizador 
        self.send('NAV_Y', self.real_y) # para o visualizador 

    def debug(self):
        print(" ")
        print(" ")
        print(" ")
        print("iPydyna Debug")

    def calculate_heading(self):
        real_heading = 0
        i = 0
        j = 0
        real_yaw = self.ship.angular_position[2]
        real_heading = 90 - np.rad2deg(real_yaw)
        if real_heading < 0:
            i = abs(real_heading) // 360 + 1
            real_heading += 360*i
        if real_heading > 360:
            j = abs(real_heading) // 360
            real_heading -= 360*j
        return real_heading


    def iterate(self):
        dt = 0.1 # dt do p3d
        dt_fast_time = dt/pymoos.get_moos_timewarp()
        while True:
            time.sleep(dt_fast_time)

            # Atualiza leme e thrust
            self.propeller1.dem_rotation = self.desired_rotation_1
            self.propeller2.dem_rotation = self.desired_rotation_2
            self.propeller3.dem_rotation = self.desired_rotation_3
            self.rudder1.dem_angle = np.deg2rad(self.desired_rudder_1)
            self.rudder2.dem_angle = np.deg2rad(self.desired_rudder_2)

            # Calcula a iteração
            self.sim.step()
            self.real_speed = self.ship.linear_velocity[0]
            self.real_x = self.ship.linear_position[0]
            self.real_y = self.ship.linear_position[1]
            self.real_heading = self.calculate_heading()

            self.update()
            self.debug()

        
if __name__ == "__main__":
    file = sys.argv[1] 
    params=MoosReader(file,"iPydyna")
    ship = Ship(params)
    ship.iterate()
