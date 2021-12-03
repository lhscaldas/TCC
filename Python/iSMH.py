#!/usr/bin/env python3
import pymoos
import time
import sys
import numpy as np
import socket
import pybuzz
from MoosReader import MoosReader
from threading import Event
from numpy import cos, sin, deg2rad



class Ship(pymoos.comms):

    def __init__(self, params):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(Ship, self).__init__()
        self.server = 'localhost'
        self.port = int(params['ServerPort'])
        self.name = 'iSMH'

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
        self.real_v = 0
        self.real_r = 0
        
        self.run(self.server, self.port, self.name)
        pymoos.set_moos_timewarp(params['MOOSTimeWarp'])
        self.dt = 0.1
        

        self.pid = '911'
        self.server_addr = '172.16.11.38'
        self.db_conn_str = 'mongodb://172.16.11.10:27017'
        self.db_name = 'smh'
        self.ds = pybuzz.create_bson_data_source(self.db_conn_str, self.db_name)
        self.session = pybuzz.join_simco_session(self.pid, pybuzz.create_bson_serializer(self.ds))
        self.session.initialize()
        self.session.is_publisher(pybuzz.rudder_tag(), pybuzz.rudder_tag.SMH_DEMANDED_ANGLE)
        self.session.is_publisher(pybuzz.thruster_tag(), pybuzz.thruster_tag.SMH_DEMANDED_ROTATION)
        self.session.connect(self.server_addr)
        self.navio = []


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

    def sendMOSS(self, key, value):
        self.notify(key, value, -1)

    def updateMOOS(self):
        # to MOOS
        self.sendMOSS('REAL_SPEED', self.real_speed)
        self.sendMOSS('REAL_HEADING', self.real_heading)
        self.sendMOSS('REAL_X', self.real_x)
        self.sendMOSS('REAL_Y', self.real_y)
        self.sendMOSS('REAL_R', self.real_v)
        self.sendMOSS('REAL_V', self.real_r)

        self.sendMOSS('NAV_SPEED', self.real_speed) # para o visualizador 
        self.sendMOSS('NAV_HEADING', self.real_heading) # para o visualizador 
        self.sendMOSS('NAV_X', self.real_x) # para o visualizador 
        self.sendMOSS('NAV_Y', self.real_y) # para o visualizador 

    def receiveSMH(self):
        self.session.sync(self.navio)
        self.real_x = self.navio.linear_position[0]
        self.real_y = self.navio.linear_position[1]
        self.real_heading = self.navio.angular_position[2]
        yaw=-deg2rad(self.real_heading)
        self.real_speed = self.navio.linear_velocity[0]*cos(yaw)-self.navio.linear_velocity[1]*sin(yaw)
        self.real_v = self.navio.linear_velocity[0]*sin(yaw)+self.navio.linear_velocity[1]*cos(yaw)
        self.real_r = self.navio.angular_velocity[2]

    def updateSMH(self):    
        # to SMH
        self.session.vessels[0].thrusters[0].dem_rotation = self.desired_rotation_1*60
        self.session.sync(self.session.vessels[0].thrusters[0])
        self.session.vessels[0].thrusters[1].dem_rotation = self.desired_rotation_2*60
        self.session.sync(self.session.vessels[0].thrusters[1])
        self.session.vessels[0].thrusters[2].dem_rotation = self.desired_rotation_3*60
        self.session.sync(self.session.vessels[0].thrusters[2])
        self.session.vessels[0].rudders[0].dem_angle = -self.desired_rudder_1
        self.session.sync(self.session.vessels[0].rudders[0])
        self.session.vessels[0].rudders[1].dem_angle = -self.desired_rudder_2
        self.session.sync(self.session.vessels[0].rudders[1])

    def debug(self):
        print(" ")
        print(" ")
        print(" ")
        print("iSMH Debug")  

    def iterate(self):
        dt = self.dt
        dt_fast_time = dt/pymoos.get_moos_timewarp()
        while True:
            time.sleep(dt_fast_time)
            if len(self.session.vessels)>0:
                self.navio = self.session.vessels[0]
            if self.navio:
                try:
                    self.receiveSMH()
                    self.updateMOOS()
                    self.updateSMH()
                except pybuzz.exception as e:
                    print (e)
                except:
                    for e in sys.exc_info():
                        print(e)
            self.debug()

        
if __name__ == "__main__":
    file = sys.argv[1] 
    params = MoosReader(file,"iSMH")
    ship = Ship(params)
    ship.iterate()