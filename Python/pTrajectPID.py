#!/usr/bin/env python3
import pymoos
import time
import sys
import numpy as np
from MoosReader import MoosReader

class myPID:

    def __init__(self, Kp, Ki, Kd, dt, max_output):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.max_output = max_output

        self.setpoint = 0
        self.int_err = 0
        self.prev_y = 0
        self.saturated = 0

        self.P = 0
        self.I = 0
        self.D = 0

    def output(self, y):
        error = self.setpoint - y
        diff_error = -(y - self.prev_y) / self.dt
        self.int_err += error * self.dt
        self.P = self.Kp * error 
        self.I = (1-self.saturated) * self.Ki * self.int_err
        self.D = self.Kd * diff_error
        output = self.P + self.I + self.D
        if abs(output) > self.max_output:
            output = output/abs(output)*self.max_output
            self.saturated = 1
            self.int_err = 0
        else:
            self.saturated = 0
        self.prev_y = y
        return output

class pTrajectPID(pymoos.comms):

    def __init__(self, params):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(pTrajectPID, self).__init__()
        self.server = 'localhost'
        self.port = int(params['ServerPort'])
        self.name = 'pTrajectPID'

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)

        self.add_active_queue('desired_queue', self.on_desired_message)
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_SPEED')
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_HEADING')

        self.add_active_queue('sensor_queue', self.on_sensor_message)
        self.add_message_route_to_active_queue('sensor_queue', 'SENSOR_SPEED')
        self.add_message_route_to_active_queue('sensor_queue', 'SENSOR_HEADING')

        self.add_active_queue('ivphelm_queue', self.on_ivphelm_message)
        self.add_message_route_to_active_queue('ivphelm_queue', 'IVPHELM_ALLSTOP')
        self.manual="false"

        self.add_active_queue('dp_queue', self.on_dp_message)
        self.add_message_route_to_active_queue('dp_queue', 'DP_MODE')
        self.dp="off"
        
        self.desired_speed = 0
        self.desired_heading = 0

        self.sensor_speed = 0
        self.sensor_heading = 0

        self.desired_rudder = 0
        self.desired_rotation = 0

        self.run(self.server, self.port, self.name)
        pymoos.set_moos_timewarp(params['MOOSTimeWarp'])
        self.dt=0.5

        dt=self.dt
        self.coursePID = myPID(Kp=params['yaw_kp']/5, Ki=params['yaw_ki']/5, Kd=params['yaw_kd']/5, dt=dt, max_output=params['max_rudder'])
        self.speedPID = myPID(Kp=params['spd_kp'], Ki=params['spd_ki'], Kd=params['spd_kd'], dt=dt, max_output=params['max_rotation'])

    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return (self.register('DESIRED_SPEED', 0) and
                self.register('DESIRED_HEADING', 0) and
                self.register('SENSOR_SPEED', 0) and
                self.register('SENSOR_HEADING', 0) and
                self.register('IVPHELM_ALLSTOP', 0))

    def __on_new_mail(self):
        """OnNewMail callback"""
        for msg in self.fetch():
            pass
        return True

    def on_desired_message(self, msg):
        """Special callback for Desired"""
        if msg.key() == 'DESIRED_SPEED':
            self.desired_speed = msg.double()
        elif msg.key() == 'DESIRED_HEADING':
            self.desired_heading = msg.double()
        return True

    def on_sensor_message(self, msg):
        """Special callback for Sensor"""
        if msg.key() == 'SENSOR_SPEED':
            self.sensor_speed = msg.double() 
        elif msg.key() == 'SENSOR_HEADING':
            self.sensor_heading = msg.double()
        return True

    def on_ivphelm_message(self, msg):
        """Special callback for Ivphelm"""
        if msg.key() == 'IVPHELM_ALLSTOP':
            self.manual = msg.string()
        return True

    def on_dp_message(self, msg):
        """Special callback for DP"""
        if msg.key() == 'DP_MODE':
            self.dp = msg.string()
        return True


    def send(self, key, value):
        self.notify(key, value, -1)

    def update(self):
        self.send('DESIRED_RUDDER_1', self.desired_rudder)
        self.send('DESIRED_RUDDER_2', self.desired_rudder)
        self.send('DESIRED_ROTATION_1', self.desired_rotation)
        self.send('DESIRED_ROTATION_2', self.desired_rotation)

    def debug(self):
        print(" ")
        print(" ")
        print(" ")
        print("pTrajectPID Debug")


    def iterate(self):
        dt = self.dt
        dt_fast_time = dt/pymoos.get_moos_timewarp()
        while True:
            time.sleep(dt_fast_time)
           
            # Atualiza setpoint
            if self.manual!="ManualOverride" and self.dp!="on":
                self.speedPID.setpoint = self.desired_speed
                heading_diff = self.desired_heading - self.sensor_heading
                if heading_diff >= 180:
                    self.coursePID.setpoint = self.desired_heading - 360
                elif heading_diff <= -180:
                    self.coursePID.setpoint = self.desired_heading + 360
                else:
                    self.coursePID.setpoint = self.desired_heading

                # Atualiza atuadores
                self.desired_rotation = self.speedPID.output(self.sensor_speed)
                self.desired_rudder = self.coursePID.output(self.sensor_heading)

                self.update()
            self.debug()


if __name__ == "__main__":
    file = sys.argv[1] 
    params=MoosReader(file,"pTrajectPID")
    PIDcontrol = pTrajectPID(params)
    PIDcontrol.iterate()
