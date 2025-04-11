# region: package imports
import time
import math
import os
from threading import Thread

# environment objects
from qvl.qlabs import QuanserInteractiveLabs
from qvl.qcar2 import QLabsQCar2
from qvl.traffic_light import QLabsTrafficLight
from qvl.real_time import QLabsRealTime

# region: package imports
import time
import math
import numpy as np
import cv2
import os


# environment objects

from qvl.qlabs import QuanserInteractiveLabs
from qvl.qcar2 import QLabsQCar2
from qvl.free_camera import QLabsFreeCamera
from qvl.real_time import QLabsRealTime
from qvl.basic_shape import QLabsBasicShape
from qvl.system import QLabsSystem
from qvl.walls import QLabsWalls
from qvl.qcar_flooring import QLabsQCarFlooring
from qvl.stop_sign import QLabsStopSign
from qvl.yield_sign import QLabsYieldSign
from qvl.roundabout_sign import QLabsRoundaboutSign
from qvl.crosswalk import QLabsCrosswalk
from qvl.traffic_light import QLabsTrafficLight

def main():
    os.system('cls')
    qlabs = QuanserInteractiveLabs()
    print("Connecting to QLabs...")
    try:
        qlabs.open("localhost")
        print("Connected to QLabs")
    except:
        print("Unable to connect to QLabs")
        quit()

    # Delete any previous QCar instances and stop any running spawn models
    qlabs.destroy_all_spawned_actors()
    QLabsRealTime().terminate_all_real_time_models()

    setup(qlabs)

    # Start traffic lights in separate thread
    traffic_thread = Thread(target=run_traffic_lights, args=(qlabs,))
    traffic_thread.daemon = True
    traffic_thread.start()


def run_traffic_lights(qlabs):
    trafficLight1 = QLabsTrafficLight(qlabs)
    trafficLight2 = QLabsTrafficLight(qlabs)
    trafficLight3 = QLabsTrafficLight(qlabs)
    trafficLight4 = QLabsTrafficLight(qlabs)

    trafficLight1.spawn_id_degrees(actorNumber=1, location=[0.6, 1.55, 0.006], rotation=[0,0,0], scale=[0.1, 0.1, 0.1], configuration=0, waitForConfirmation=False)
    trafficLight2.spawn_id_degrees(actorNumber=2, location=[-0.6, 1.28, 0.006], rotation=[0,0,90], scale=[0.1, 0.1, 0.1], configuration=0, waitForConfirmation=False)
    trafficLight3.spawn_id_degrees(actorNumber=3, location=[-0.37, 0.3, 0.006], rotation=[0,0,180], scale=[0.1, 0.1, 0.1], configuration=0, waitForConfirmation=False)
    trafficLight4.spawn_id_degrees(actorNumber=4, location=[0.75, 0.48, 0.006], rotation=[0,0,-90], scale=[0.1, 0.1, 0.1], configuration=0, waitForConfirmation=False)

    intersection1Flag = 0
    print('Starting Traffic Light Sequence')
    
    while True:
        if intersection1Flag == 0:
            trafficLight1.set_color(color=QLabsTrafficLight.COLOR_RED)
            trafficLight3.set_color(color=QLabsTrafficLight.COLOR_RED)
            trafficLight2.set_color(color=QLabsTrafficLight.COLOR_GREEN)
            trafficLight4.set_color(color=QLabsTrafficLight.COLOR_GREEN)
        elif intersection1Flag == 1:
            trafficLight1.set_color(color=QLabsTrafficLight.COLOR_RED)
            trafficLight3.set_color(color=QLabsTrafficLight.COLOR_RED)
            trafficLight2.set_color(color=QLabsTrafficLight.COLOR_YELLOW)
            trafficLight4.set_color(color=QLabsTrafficLight.COLOR_YELLOW)
        elif intersection1Flag == 2:
            trafficLight1.set_color(color=QLabsTrafficLight.COLOR_GREEN)
            trafficLight3.set_color(color=QLabsTrafficLight.COLOR_GREEN)
            trafficLight2.set_color(color=QLabsTrafficLight.COLOR_RED)
            trafficLight4.set_color(color=QLabsTrafficLight.COLOR_RED)
        elif intersection1Flag == 3:
            trafficLight1.set_color(color=QLabsTrafficLight.COLOR_YELLOW)
            trafficLight3.set_color(color=QLabsTrafficLight.COLOR_YELLOW)
            trafficLight2.set_color(color=QLabsTrafficLight.COLOR_RED)
            trafficLight4.set_color(color=QLabsTrafficLight.COLOR_RED)

        intersection1Flag = (intersection1Flag + 1) % 4
        time.sleep(5)

#Function to setup QLabs, Spawn in QCar, and run real time model
def setup(qlabs, initialPosition = [-1.205, -0.83, 0.005], initialOrientation = [0, 0, -44.7]):

# Try to connect to Qlabs

    os.system('cls')
    qlabs = QuanserInteractiveLabs()
    print("Connecting to QLabs...")
    try:
        qlabs.open("localhost")
        print("Connected to QLabs")
    except:
        print("Unable to connect to QLabs")
        quit()

    # Delete any previous QCar instances and stop any running spawn models
    qlabs.destroy_all_spawned_actors()
    QLabsRealTime().terminate_all_real_time_models()

    #Set the Workspace Title
    hSystem = QLabsSystem(qlabs)
    x = hSystem.set_title_string('ACC Self Driving Car Competition', waitForConfirmation=True)

    ### Flooring

    x_offset = 0.13
    y_offset = 1.67
    hFloor = QLabsQCarFlooring(qlabs)
    hFloor.spawn_degrees([x_offset, y_offset, 0.001],rotation = [0, 0, -90])


    ### region: Walls
    hWall = QLabsWalls(qlabs)
    hWall.set_enable_dynamics(False)

    for y in range (5):
        hWall.spawn_degrees(location=[-2.4 + x_offset, (-y*1.0)+2.55 + y_offset, 0.001], rotation=[0, 0, 0])

    for x in range (5):
        hWall.spawn_degrees(location=[-1.9+x + x_offset, 3.05+ y_offset, 0.001], rotation=[0, 0, 90])

    for y in range (6):
        hWall.spawn_degrees(location=[2.4+ x_offset, (-y*1.0)+2.55 + y_offset, 0.001], rotation=[0, 0, 0])

    for x in range (4):
        hWall.spawn_degrees(location=[-0.9+x+ x_offset, -3.05+ y_offset, 0.001], rotation=[0, 0, 90])

    hWall.spawn_degrees(location=[-2.03 + x_offset, -2.275+ y_offset, 0.001], rotation=[0, 0, 48])
    hWall.spawn_degrees(location=[-1.575+ x_offset, -2.7+ y_offset, 0.001], rotation=[0, 0, 48])

    # basic path-following using angle-based turning and fixed forward movement
    WAYPOINTS = [ (-0.654,-1.041,-15),(-0.388,-1.061,0),(-0.035,-1.071,0),(0.595,-1.065,0),(1.236,-1.065,-10),(1.559,-1.028,-10),(2.202,0.123,-10),(2.198,2.058,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),
                 (2.202,3.785,-20),(1.957,4.237,-9.3),(1.639,4.389,0),(0.599,4.390,0),(0,0,0),(-1.303,4.383,-3),(-1.582,4.254,-10),(0,0,-15),(0,0,-1.8),(0,0,0),(0,0,0),(0,0,-10),(0,0,-11),(0,0,-11),(0,0,10),
                 (0,0,20),(0,0,-5),(0,0,-12),(0,0,-10),(0,0,-10),(0,0,-15),(0,0,-10),(0,0,-10),(0,0,-10),(0,0,-5),(0,0,0),(0,0,0),(0,0,0),(0,0,-18),(0,0,-11),(0,0,-10),(0,0,-10)]
    
   
    #spawn a QCar with degrees
    hQCar2 = QLabsQCar2(qlabs)
    x = hQCar2.spawn_id_degrees(actorNumber=0, 
                location=initialPosition, 
                rotation=initialOrientation,
                scale=[.1, .1, .1], 
                configuration=0, 
                waitForConfirmation=True)
    

    #spawn cameras 1. birds eye, 2. edge 1, possess the qcar

    camera1Loc = [0.15, 1.7, 5]
    camera1Rot = [0, 90, 0]
    camera1 = QLabsFreeCamera(qlabs)
    camera1.spawn_degrees(location=camera1Loc, rotation=camera1Rot)

    #camera1.possess()

    camera2Loc = [-0.36+ x_offset, -3.691+ y_offset, 2.652]
    camera2Rot = [0, 47, 90]
    camera2=QLabsFreeCamera(qlabs)
    camera2.spawn_degrees (location = camera2Loc, rotation=camera2Rot)

    camera2.possess()

    # stop signs
    #parking lot
    myStopSign = QLabsStopSign(qlabs)
    
    myStopSign.spawn_degrees (location=[-1.5, 3.6, 0.006], 
                            rotation=[0, 0, -35], 
                            scale=[0.1, 0.1, 0.1], 
                            waitForConfirmation=False)    

    myStopSign.spawn_degrees (location=[-1.5, 2.2, 0.006], 
                            rotation=[0, 0, 35], 
                            scale=[0.1, 0.1, 0.1], 
                            waitForConfirmation=False)  
    
    #x+ side
    myStopSign.spawn_degrees (location=[2.410, 0.206, 0.006], 
                            rotation=[0, 0, -90], 
                            scale=[0.1, 0.1, 0.1], 
                            waitForConfirmation=False)  
    
    myStopSign.spawn_degrees (location=[1.766, 1.697, 0.006], 
                            rotation=[0, 0, 90], 
                            scale=[0.1, 0.1, 0.1], 
                            waitForConfirmation=False)  

    #roundabout signs
    myRoundaboutSign = QLabsRoundaboutSign(qlabs)
    myRoundaboutSign.spawn_degrees(location= [2.392, 2.522, 0.006],
                              rotation=[0, 0, -90],
                              scale= [0.1, 0.1, 0.1],
                              waitForConfirmation=False)
    
    myRoundaboutSign.spawn_degrees(location= [0.698, 2.483, 0.006],
                              rotation=[0, 0, -145],
                              scale= [0.1, 0.1, 0.1],
                              waitForConfirmation=False)
    
    myRoundaboutSign.spawn_degrees(location= [0.007, 3.973, 0.006],
                            rotation=[0, 0, 135],
                            scale= [0.1, 0.1, 0.1],
                            waitForConfirmation=False)


    #yield sign
    #one way exit yield
    myYieldSign = QLabsYieldSign(qlabs)
    myYieldSign.spawn_degrees(location= [0.0, -1.3, 0.006],
                              rotation=[0, 0, -180],
                              scale= [0.1, 0.1, 0.1],
                              waitForConfirmation=False)
    
    #roundabout yields
    myYieldSign.spawn_degrees(location= [2.4, 3.2, 0.006],
                            rotation=[0, 0, -90],
                            scale= [0.1, 0.1, 0.1],
                            waitForConfirmation=False)
    
    myYieldSign.spawn_degrees(location= [1.1, 2.8, 0.006],
                            rotation=[0, 0, -145],
                            scale= [0.1, 0.1, 0.1],
                            waitForConfirmation=False)
    
    myYieldSign.spawn_degrees(location= [0.49, 3.8, 0.006],
                            rotation=[0, 0, 135],
                            scale= [0.1, 0.1, 0.1],
                            waitForConfirmation=False)
    
    

    # Spawning crosswalks
    myCrossWalk = QLabsCrosswalk(qlabs)
    myCrossWalk.spawn_degrees   (location =[-2 + x_offset, -1.475 + y_offset, 0.01],
                                rotation=[0,0,0], 
                                scale = [0.1,0.1,0.075],
                                configuration = 0)

    myCrossWalk.spawn_degrees   (location =[-0.5, 0.95, 0.006],
                                rotation=[0,0,90], 
                                scale = [0.1,0.1,0.075],
                                configuration = 0)
    
    myCrossWalk.spawn_degrees   (location =[0.15, 0.32, 0.006],
                                rotation=[0,0,0], 
                                scale = [0.1,0.1,0.075],
                                configuration = 0)

    myCrossWalk.spawn_degrees   (location =[0.75, 0.95, 0.006],
                                rotation=[0,0,90], 
                                scale = [0.1,0.1,0.075],
                                configuration = 0)

    myCrossWalk.spawn_degrees   (location =[0.13, 1.57, 0.006],
                                rotation=[0,0,0], 
                                scale = [0.1,0.1,0.075],
                                configuration = 0)

    myCrossWalk.spawn_degrees   (location =[1.45, 0.95, 0.006],
                                rotation=[0,0,90], 
                                scale = [0.1,0.1,0.075],
                                configuration = 0)

    #Signage line guidance (white lines)
    mySpline = QLabsBasicShape(qlabs)
    mySpline.spawn_degrees (location=[2.21, 0.2, 0.006], 
                            rotation=[0, 0, 0], 
                            scale=[0.27, 0.02, 0.001], 
                            waitForConfirmation=False)

    mySpline.spawn_degrees (location=[1.951, 1.68, 0.006], 
                            rotation=[0, 0, 0], 
                            scale=[0.27, 0.02, 0.001], 
                            waitForConfirmation=False)

    mySpline.spawn_degrees (location=[-0.05, -1.02, 0.006], 
                            rotation=[0, 0, 90], 
                            scale=[0.38, 0.02, 0.001], 
                            waitForConfirmation=False)



    # utility to send QCar turn and move command
    def move_to_waypoint(qcar, heading_deg, speed=0.2, duration=3): 
        print(f"\nDriving: speed={speed}, turn={heading_deg}°")
        qcar.set_velocity_and_request_state_degrees(
        forward=speed,
        turn=heading_deg,
        headlights=False,
        leftTurnSignal=True,
        rightTurnSignal=True,
        brakeSignal=False,
        reverseSignal=False
    )
        time.sleep(duration)

# move through each waypoint
    for x, y, heading in WAYPOINTS:
        move_to_waypoint(hQCar2, heading, speed=1, duration=0.595)#adjust to make it faster or slower, speed goes up duration goes down if you like ferrari speed try 3 and 0.195 

    hQCar2.set_velocity_and_request_state(forward=0, turn=0,headlights=False,
        leftTurnSignal=False,
        rightTurnSignal=False,
        brakeSignal=True,
        reverseSignal=False
        )    
    
    print("\nPath completed. QCar stopped.")
    
    input("Press Enter to exit...")





if __name__ == '__main__':
    main()




    



if __name__ == '__main__':
    main()
