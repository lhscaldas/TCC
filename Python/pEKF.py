#!/usr/bin/env python3

# Modelo de EKF do Fossen com leituras de v e r
import pymoos
import time
import sys
import numpy as np
from MoosReader import MoosReader

sin = np.sin
cos = np.cos
inv = np.linalg.inv
rho=1025e-3
# diâmetros dos propulsores
D1=0.475
D2=0.475
D3=0.185
# posição dos propulsores
x1=5.52-0.7
y1=0.67
x2=5.52-0.7
y2=0.67
x3=5.78+0.7
# medidas do navio
h = 1.65 # altura
B = 3.379 # boca
T = 0.956 # calado
L = 13.095 # LOA
# massas e amortecimento
C2_90  = 3.27607
C1_180 = 0.10900
C3_90 = 0.02246
m11=18.79+1.01115
m22=18.79+10.48726
m33=240.19+90.95633
d11=rho*L*T*C1_180/2
d22=rho*L*T*C2_90/2
d33=rho*L**4*T*C2_90/32
d33_=rho*L**2*T*C3_90/2

def yaw2hdg(yaw):
    i = 0
    j = 0
    real_heading = 90 - np.rad2deg(yaw)
    if real_heading < 0:
        i = abs(real_heading) // 360 + 1
        real_heading += 360*i
    elif real_heading > 360:
        j = abs(real_heading) // 360
        real_heading -= 360*j
    return real_heading

def hdg2yaw(hdg):
    yaw = np.pi/2 - np.deg2rad(hdg)
    if yaw<0:
        yaw+=2*np.pi
    if yaw>2*np.pi:
        yaw-=2*np.pi
    return yaw 

class pEKF(pymoos.comms):

    def __init__(self, params):
        """Initiates MOOSComms, sets the callbacks and runs the loop"""
        super(pEKF, self).__init__()
        self.server = 'localhost'
        self.port = int(params['ServerPort'])
        self.name = 'pEKF'

        self.set_on_connect_callback(self.__on_connect)
        self.set_on_mail_callback(self.__on_new_mail)

        self.add_active_queue('dvl_queue', self.on_dvl_message)
        self.add_message_route_to_active_queue('dvl_queue', 'DVL_SPEED')

        self.add_active_queue('gps_queue', self.on_gps_message)
        self.add_message_route_to_active_queue('gps_queue', 'GPS_SPEED')
        self.add_message_route_to_active_queue('gps_queue', 'GPS_X')
        self.add_message_route_to_active_queue('gps_queue', 'GPS_Y')

        self.add_active_queue('gyro_queue', self.on_gyro_message)
        self.add_message_route_to_active_queue('gyro_queue', 'GYRO_HEADING')
        
        self.add_active_queue('imu_queue', self.on_imu_message)
        self.add_message_route_to_active_queue('imu_queue', 'IMU_SPEED')
        self.add_message_route_to_active_queue('imu_queue', 'IMU_X')
        self.add_message_route_to_active_queue('imu_queue', 'IMU_Y')
        self.add_message_route_to_active_queue('imu_queue', 'IMU_HEADING')
        self.add_message_route_to_active_queue('imu_queue', 'IMU_V')
        self.add_message_route_to_active_queue('imu_queue', 'IMU_R')

        self.add_active_queue('desired_queue', self.on_desired_message)
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_ROTATION_1')
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_ROTATION_2')
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_ROTATION_3')
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_RUDDER_1')
        self.add_message_route_to_active_queue('desired_queue', 'DESIRED_RUDDER_2')

        self.dvl_speed = 0
        self.gps_speed = 0
        self.gps_x = 0
        self.gps_y = 0
        self.gyro_heading = 0
        self.imu_speed = 0
        self.imu_x = 0
        self.imu_y = 0
        self.imu_heading = 0
        self.imu_v = 0
        self.imu_r = 0
        
        self.ekf_speed = 0
        self.ekf_x = params['START_X']
        self.ekf_y = params['START_Y']
        self.ekf_heading = params['START_HEADING']

        self.n1 = 0
        self.n2 = 0
        self.n3 = 0
        self.beta1 = 0
        self.beta2 = 0

        self.eta_hat = [self.ekf_speed, 0, 0, self.ekf_x, self.ekf_y, hdg2yaw(self.ekf_heading)]
        self.P = 1e6*np.eye(6)
        self.Q = 1e6*np.diagflat([1,1,1,1,1,1])
        e_IMU_spd = 0.12 ** 2
        e_IMU_pos = 1.2 ** 2
        e_IMU_hdg = np.deg2rad(0.08) ** 2
        e_IMU_rot = np.deg2rad(0.03) ** 2
        e_GPS_pos = 1.2 ** 2
        e_GPS_spd = 0.03 ** 2
        e_gyro_hdg = np.deg2rad(0.25) ** 2
        e_DVL_spd = 0.002 ** 2
        self.R = np.diagflat([e_GPS_spd,e_DVL_spd,e_IMU_spd,e_IMU_spd,e_IMU_rot,e_GPS_pos,e_IMU_pos,e_GPS_pos,e_IMU_pos,e_gyro_hdg,e_IMU_hdg])
        
        
        self.run(self.server, self.port, self.name)
        pymoos.set_moos_timewarp(params['MOOSTimeWarp'])
        self.dt=0.1

       
    def __on_connect(self):
        """OnConnect callback"""
        print("Connected to", self.server, self.port,
              "under the name ", self.name)
        return (self.register('DVL_SPEED', 0) and
                self.register('GPS_SPEED', 0) and
                self.register('GPS_X', 0) and
                self.register('GPS_Y', 0) and
                self.register('GYRO_HEADING', 0) and
                self.register('IMU_SPEED', 0) and
                self.register('IMU_X', 0) and
                self.register('IMU_Y', 0) and
                self.register('IMU_HEADING', 0) and
                self.register('DESIRED_ROTATION_1', 0) and
                self.register('DESIRED_ROTATION_2', 0) and
                self.register('DESIRED_ROTATION_3', 0) and
                self.register('DESIRED_RUDDER_1', 0) and
                self.register('DESIRED_RUDDER_2', 0) and
                self.register('IMU_R', 0) and
                self.register('IMU_V', 0))
                

    def __on_new_mail(self):
        """OnNewMail callback"""
        for msg in self.fetch():
            pass
        return True

    def on_dvl_message(self, msg):
        if msg.key() == 'DVL_SPEED':
            self.dvl_speed = msg.double()
        return True

    def on_gps_message(self, msg):
        if msg.key() == 'GPS_SPEED':
            self.gps_speed = msg.double()
        elif msg.key() == 'GPS_X':
            self.gps_x = msg.double()
        elif msg.key() == 'GPS_Y':
            self.gps_y = msg.double()
        return True

    def on_gyro_message(self, msg):
        if msg.key() == 'GYRO_HEADING':
            self.gyro_heading = hdg2yaw(msg.double())
        return True

    def on_imu_message(self, msg):
        if msg.key() == 'IMU_SPEED':
            self.imu_speed = msg.double()
        elif msg.key() == 'IMU_X':
            self.imu_x = msg.double()
        elif msg.key() == 'IMU_Y':
            self.imu_y = msg.double()
        elif msg.key() == 'IMU_HEADING':
            self.imu_heading = hdg2yaw(msg.double())
        elif msg.key() == 'IMU_R':
            self.real_r = msg.double()
        elif msg.key() == 'IMU_V':
            self.real_v = msg.double()
        return True

    def on_desired_message(self, msg):
        if msg.key() == 'DESIRED_RUDDER_1':
            self.beta1 = msg.double()
        elif msg.key() == 'DESIRED_RUDDER_1':
            self.beta2 = msg.double()
        elif msg.key() == 'DESIRED_ROTATION_1':
            self.n1 = msg.double()
        elif msg.key() == 'DESIRED_ROTATION_2':
            self.n2 = msg.double()
        elif msg.key() == 'DESIRED_ROTATION_3':
            self.n3 = msg.double()
        return True



    def send(self, key, value):
        self.notify(key, value, -1)

    def update(self):
        self.send('SENSOR_HEADING', self.ekf_heading)
        self.send('SENSOR_SPEED', self.ekf_speed)
        self.send('SENSOR_X', self.ekf_x)
        self.send('SENSOR_Y', self.ekf_y)

    def estimate_inputs(self,eta):
        # calculo do thrust
        u = eta[0]
        n1 = self.n1
        n2 = self.n2
        n3 = self.n3
        if n1 != 0:
            J1=u/(n1*D1)
        else:
            J1=0
        if n2 != 0:
            J2=u/(n2*D2)
        else:
            J2=0
        if n3 != 0:
            J3=u/(n3*D3)
        else:
            J3=0
        Kt1=1.09214295e-01*J1**5 - 1.89739146e-05*J1**4 - 1.91249589e-01*J1**3 + 6.59504311e-06*J1**2 - 4.14551312e-01*J1 + 6.58016406e-01
        Kt2=1.09214295e-01*J2**5 - 1.89739146e-05*J2**4 - 1.91249589e-01*J2**3 + 6.59504311e-06*J2**2 - 4.14551312e-01*J2 + 6.58016406e-01
        Kt3=0.01476418*J3**5 - 0.03187213*J3**4 - 0.38456785*J3**3 + 0.19234734*J3**2 - 0.49985203*J3 + 0.36826644
        T1=rho*Kt1*n1**2*D1**4
        T2=rho*Kt2*n2**2*D2**4
        T3=rho*Kt3*n3**2*D3**4
        # calculo da deflexão
        beta1 = self.beta1 # leme 1
        beta2 = self.beta2 # leme 2
        alfa1 = np.deg2rad(-2.18096324e-04*beta1**3 + 1.05990036*beta1) # deflexão 1
        alfa2 = np.deg2rad(-2.18096324e-04*beta2**3 + 1.05990036*beta2) # deflexão 2
        # calculo das entradas
        Tao_u = T1*cos(alfa1)+T2*cos(alfa2)
        Tao_v = T1*sin(alfa1)+T2*sin(alfa2)-T3
        Tao_r = -T1*cos(alfa1)*y1-T1*sin(alfa1)*x1+T2*cos(alfa2)*y2-T2*sin(alfa2)*x2-T3*x3
        return [Tao_u,Tao_v,Tao_r]

    def calc_F(self,eta,tau,dt):
        [u, v, r, x, y, psi] = eta
        [Tau_u,Tau_v,Tau_r] = tau
        ukp1 = u + (- d11*u*abs(u) + m22*r*v + Tau_u)/m11*dt
        vkp1 = v + (- d22*u*abs(u) - m11*r*u + Tau_v)/m22*dt
        rkp1 = r + (- d33*r*abs(r) - d33_*u*abs(u) - (m11-m22)*u*v  + Tau_r)/m33*dt 
        xkp1 = x + (u*cos(psi)-v*sin(psi))*dt
        ykp1 = y + (u*sin(psi)+v*cos(psi))*dt
        pkp1 = psi + r*dt
        return [ukp1, vkp1, rkp1, xkp1, ykp1, pkp1]

    def calc_A(self,eta,dt):
        [u, v, r, x, y, psi] = eta
        A = list()
        A.append(np.array([-2*d11*u, m22*r, m22*v, 0, 0, 0])*dt/m11)
        A.append(np.array([-m11*r-2*d22*u,0, -m11*u, 0, 0, 0])*dt/m22)
        A.append(np.array([(m11-m22)*v-2*d33_*u, (m11-m22)*u, -2*d33*r, 0, 0, 0])*dt/m33)
        A.append(np.array([cos(psi), -sin(psi), 0, 0, 0, -u*sin(psi)-v*cos(psi)])*dt)
        A.append(np.array([sin(psi), cos(psi), 0, 0, 0, u*cos(psi)-v*sin(psi)])*dt)
        A.append(np.array([0, 0, 1, 0, 0, 0])*dt)
        A=np.array(A)
        A+=np.eye(6)
        return A

    def calc_C(self, eta):
        C = np.zeros((11,6))
        C[0:3,0]=1
        C[3,1] = 1
        C[4,2] = 1
        C[5:7,3]=1
        C[7:9,4]=1
        C[9:,5]=1
        return C

    def sensorZ(self):    
        zk = [self.gps_speed, self.dvl_speed, self.imu_speed, self.imu_v, self.imu_r, self.gps_x, self.imu_x, self.gps_y, self.imu_y, self.gyro_heading, self.imu_heading]
        return np.array(zk)

    def ekf_predict(self, eta_hat, tau):
        dt = self.dt
        P = self.P
        Q = self.Q
        eta_bar = self.calc_F(eta_hat, tau, dt)
        Phi = self.calc_A(eta_hat, dt)
        gama = dt*np.diagflat([1,1,1,0,0,0])
        P_bar = Phi@P@Phi.T + gama*Q*gama.T
        return eta_bar, P_bar

    def ekf_update(self, eta_bar, P_bar):
        R = self.R
        H = self.calc_C(eta_bar)
        y = self.sensorZ()
        K = P_bar@H.T@inv(H@P_bar@H.T+R) 
        eta_hat = eta_bar + K@(y-H@eta_bar)
        P = (np.eye(6)-K@H)@P_bar@(np.eye(6)-K@H).T + K@R@K.T
        return eta_hat, P
    

    def set_ekf_var(self):
        self.ekf_speed = self.eta_hat[0]
        self.ekf_x = self.eta_hat[3]
        self.ekf_y = self.eta_hat[4]
        self.ekf_heading = yaw2hdg(self.eta_hat[5])


    def debug(self, args=list()):
        print(" ")
        print(" ")
        print(" ")
        print("pEKF Debug")
        print(f"ekf_spd = {self.ekf_speed}")
        print(f"ekf_x = {self.ekf_x}")
        print(f"ekf_y = {self.ekf_y}")
        print(f"ekf_hdg = {self.ekf_heading}")
        print(f"imu_hdg = {yaw2hdg(self.imu_heading)}")
        print(f"gyro_hdg = {yaw2hdg(self.gyro_heading)}")

    def iterate(self):
        dt = self.dt
        dt_fast_time = dt/pymoos.get_moos_timewarp()
        while True:
            time.sleep(dt_fast_time)

            # Get last state and input
            eta_hat = self.eta_hat
            tau = self.estimate_inputs(eta_hat)
            
            # EKF steps
            eta_bar, P_bar = self.ekf_predict(eta_hat, tau)
            self.eta_hat, self.P = self.ekf_update(eta_bar, P_bar)

            # Update and debug
            self.set_ekf_var()
            self.update()
            self.debug([self.eta_hat,tau])


if __name__ == "__main__":
    file = sys.argv[1] 
    params=MoosReader(file,"pEKF")
    PIDcontrol = pEKF(params)
    PIDcontrol.iterate()
