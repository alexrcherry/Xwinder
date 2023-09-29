from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *
from Phidget22.Devices.Stepper import *
import time
import numpy as np

class winder:
    def __init__(self):

        self.position = 0 #home position is zero, far end of part is one
        #place to store stuff
        self.Mv100degs = 0
        self.RF_Mandrel = .1125
        self.RF_Carriage = .1125
        self.RF_Head = .1125



    def connect(self,
                 mandrel_SN=615813, mandrel_factor=1/60.444,
                 carriage_SN=615519, carriage_factor=-1/3624,
                 head_SN=616004, head_factor=9/1040,):

        self.mandrel = Stepper()
        self.carriage = Stepper()
        self.head = Stepper()
        self.mandrel.setDeviceSerialNumber(mandrel_SN)
        self.mandrel.openWaitForAttachment(5000)
        self.mandrel.setAcceleration(10000)
        self.mandrel.setRescaleFactor(mandrel_factor) #convert so set target is in degrees


        self.carriage.setDeviceSerialNumber(carriage_SN)
        self.carriage.openWaitForAttachment(5000)
        self.carriage.setAcceleration(10000)
        self.carriage.setRescaleFactor(head_factor)


        self.head.setDeviceSerialNumber(head_SN)
        self.head.openWaitForAttachment(5000)
        self.head.setAcceleration(4800)
        self.head.setRescaleFactor(head_factor)




    def parameter_calculation(self,
                              alpha_desired:float = 55,
                              radius = 1.985/2,
                              fiber_thickness_hoop = .152,
                              linear_velocity_hoop = .02,
                              travel_distance = 15.5,
                              fiber_thickness_helical = .16,
                              linear_velocity_helical=.05
                              ):
        self.travel_distance = travel_distance
        self.linear_velocity_hoop = linear_velocity_hoop
        self.linear_velocity_helical = linear_velocity_helical
        t = fiber_thickness_hoop/linear_velocity_hoop
        self.angular_velocity = 360/t
        print('angular velocity:', self.angular_velocity)
        self.fiber_thickness_hoop = fiber_thickness_hoop
        self.fiber_thickness_helical = fiber_thickness_helical

        #helical
        def calc_alpha(N, B, D):
            return np.degrees(np.arccos((N*B)/(np.pi*D)))



        offset_fudge_factor = 1# percent multiplier for offset angle
        head_angle_length = .25 #in length that the head turns during
        self.head_angle_length = head_angle_length
        r = radius
        B = fiber_thickness_helical
        D = 2*r
        possible_alphas = []
        alpha_error = 0
        previous_alpha_error = 100
        N = 5
        while alpha_error< previous_alpha_error:
            N += 1
            alpha_error = abs(calc_alpha(N, B, D) - alpha_desired )
            previous_alpha_error = abs(calc_alpha(N-1, B, D) - alpha_desired )


        alpha = calc_alpha(N-1, B, D)
        print('alpha', alpha)
        print('N:', N)
        self.alpha = alpha
        self.N = N

        width1 = fiber_thickness_helical/np.cos(np.radians(alpha))
        self.angular_offset = width1*(360/(2*np.pi*r))*offset_fudge_factor

        self.W_mand = linear_velocity_helical*np.tan(np.radians(alpha))*(360/(2*np.pi*r))
        self.W_head = (90-alpha)/(360/self.W_mand)*1.5

        self.T = travel_distance/linear_velocity_helical
        self.Total_angle = self.W_mand*self.T
        self.head_F = -(90-alpha+15)
        self.head_B = 90-alpha+15


    def helical(self):
        if self.position == 0:
            self.carriage.setVelocityLimit(self.linear_velocity_helical)
            self.mandrel.setVelocityLimit(self.W_mand)
            print("Total Iterations Helical Forwards:", self.N)
            for i in range(self.N):

                temp_string = 'Iter:' + str(i) + '/' + str(self.N)
                print(temp_string)

                #Helical Path forwards
                self.head.setTargetPosition(self.head_F)
                self.head.setEngaged(True)

                self.carriage.setTargetPosition(self.travel_distance)
                self.mandrel.setTargetPosition(self.mandrel.getTargetPosition()-self.Total_angle)

                self.head.setEngaged(True)
                self.mandrel.setEngaged(True)
                self.carriage.setEngaged(True)

                while (self.mandrel.getIsMoving()):
                    time.sleep(.5)

                self.head.setVelocityLimit(self.W_head)
                self.head.setTargetPosition(0)
                self.mandrel.setTargetPosition(self.mandrel.getTargetPosition() - 360)

                self.mandrel.setEngaged(True)
                self.head.setEngaged(True)

                while (self.mandrel.getIsMoving()):
                    time.sleep(.5)

                # move head to helical angle
                self.head.setVelocityLimit(abs(self.head_B)/(self.head_angle_length/self.linear_velocity_helical))
                self.head.setTargetPosition(self.head_B)

                #return on helical path
                self.carriage.setTargetPosition(0)
                self.mandrel.setTargetPosition(self.mandrel.getTargetPosition()-self.Total_angle)

                self.head.setEngaged(True)
                self.mandrel.setEngaged(True)
                self.carriage.setEngaged(True)

                while (self.mandrel.getIsMoving()):
                    time.sleep(.5)

                #turn head while tapering
                self.head.setVelocityLimit(self.W_head)
                self.ead.setTargetPosition(0)
                self.mandrel.setTargetPosition(self.mandrel.getTargetPosition() - 360-self.angular_offset)

                self.mandrel.setEngaged(True)
                self.head.setEngaged(True)

                while (self.mandrel.getIsMoving()):
                    time.sleep(.5)

                # move head to helical angle
                self.head.setVelocityLimit(abs(self.head_B)/(self.head_angle_length/self.linear_velocity_helical))
                self.head.setTargetPosition(self.head_F)

            self.position = 1
            print("Helical Forwards End")
        else:
            self.carriage.setVelocityLimit(self.linear_velocity_helical)
            self.mandrel.setVelocityLimit(self.W_mand)
            print("Total Iterations Helical Backwards:", self.N)
            for i in range(self.N):

                temp_string = 'Iter:' + str(i) + '/' + str(self.N)
                print(temp_string)

                # move head to helical angle
                self.head.setVelocityLimit(abs(self.head_B)/(self.head_angle_length/self.linear_velocity_helical))
                self.head.setTargetPosition(self.head_B)
                print('move head to helical angle 182')

                # return on helical path
                self.carriage.setTargetPosition(0)
                self.mandrel.setTargetPosition(self.mandrel.getTargetPosition()-self.Total_angle)


                self.head.setEngaged(True)
                self.mandrel.setEngaged(True)
                self.carriage.setEngaged(True)
                print('return on helical path 192')

                while (self.mandrel.getIsMoving()):
                    print('mandrel moving 195')
                    time.sleep(.5)

                #turn head while tapering
                self.head.setVelocityLimit(self.W_head)
                self.head.setTargetPosition(0)
                self.mandrel.setTargetPosition(self.mandrel.getTargetPosition() - 360-self.angular_offset)

                self.mandrel.setEngaged(True)
                self.head.setEngaged(True)

                print('turn head while tapering 206')

                while (self.mandrel.getIsMoving()):
                    print('mandrel moving 209')
                    time.sleep(.5)

                # move head to helical angle
                self.head.setVelocityLimit(abs(self.head_B)/(self.head_angle_length/self.linear_velocity_helical))
                self.head.setTargetPosition(self.head_F)

                #Helical Path forwards
                self.head.setTargetPosition(self.head_F)
                self.head.setEngaged(True)
                print('Helical Path forwards 219')

                self.carriage.setTargetPosition(self.travel_distance)
                self.mandrel.setTargetPosition(self.mandrel.getTargetPosition()-self.Total_angle)

                self.head.setEngaged(True)
                self.mandrel.setEngaged(True)
                self.carriage.setEngaged(True)

                while (self.mandrel.getIsMoving()):
                    print('229 mandrel moving')
                    time.sleep(.5)

                #taper
                self.head.setVelocityLimit(self.W_head)
                self.head.setTargetPosition(0)
                self.mandrel.setTargetPosition(self.mandrel.getTargetPosition() - 360)

                self.mandrel.setEngaged(True)
                self.head.setEngaged(True)

                while (self.mandrel.getIsMoving()):
                    time.sleep(.5)

            self.position = 0
            print("Helical Backwards Ends")


    def part_size(radius, length):
        self.radius = radius
        self. length = length


    def hoop(self):
        if self.position == 0:
            print('Hoop Forward Start')

            self.carriage.setVelocityLimit(self.linear_velocity_hoop)
            self.mandrel.setVelocityLimit(self.angular_velocity)

            self.head.setTargetPosition(0)
            self.carriage.setTargetPosition(self.travel_distance)
            self.mandrel.setTargetPosition(self.mandrel.getTargetPosition()-self.travel_distance*(360/self.fiber_thickness_hoop))

            self.head.setEngaged(True)
            self.mandrel.setEngaged(True)
            self.carriage.setEngaged(True)

            self.position = 1
            print('Hoop Forward End')
        else:
            print('Hoop Backward Start')
            self.carriage.setVelocityLimit(self.linear_velocity)
            self.mandrel.setVelocityLimit(self.angular_velocity)

            self.head.setTargetPosition(0)
            self.carriage.setTargetPosition(0)
            self.mandrel.setTargetPosition(self.mandrel.getTargetPosition()-self.travel_distance*(360/self.fiber_thickness_hoop))

            self.head.setEngaged(True)
            self.mandrel.setEngaged(True)
            self.carriage.setEngaged(True)

            self.position = 0
            print('Hoop Backward End')

    def tape_winding(self):
        self.mandrel.setTargetPosition(200000)
        self.mandrel.setEngaged(True)


    def engage_motors(self):
        val = 1
        self.mandrel.setEngaged(val)
        self.head.setEngaged(val)
        self.mandrel.setEngaged(val)


    def disengage_motors(self):
        val = 0
        self.mandrel.setEngaged(val)
        self.head.setEngaged(val)
        self.mandrel.setEngaged(val)


    def close_connection(self):
        self.head.close()
        self.mandrel.close()
        self.carriage.close()


    def calibrate(self, Mand_Carr_Head = [0, 1, 0]):
        RescaleFactors = np.array[.0625*1.8, .0625*1.8, .0625*1.8]
        Mand_Carr_Head = np.array[Mand_Carr_Head]
        masked_rescale_factors = RescaleFactors*Mand_Carr_Head

        if Mand_Carr_Head[0] == 1:
            self.mandrelRescaleFactor = .0625*1.8
            self.mandrel.setTargetPosition(100)

            while (self.mandrel.getIsMoving()):
                    time.sleep(.5)

            time.sleep(5)

        if Mand_Carr_Head[1] == 1:
            self.carriageRescaleFactor = .0625*1.8 #assuming stepper is 1.8 deg/s this makes it so one unit is 1 deg
            self.carriage.setTargetPosition(100)

            while (self.carriage.getIsMoving()):
                    time.sleep(.5)

            time.sleep(5)

        if Mand_Carr_Head[2] == 1:
            self.headRescaleFactor = .0625*1.8
            self.head.setTargetPosition(100)

            while (self.head.getIsMoving()):
                    time.sleep(.5)

            time.sleep(5)





