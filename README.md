# ToyRobot_Simulator
Robotic Arm Simulator

Description

The application is a simulation of a toy robot for Celluar Origins moving on a square tabletop, of dimensions 5 units x 5 units. There are no other obstructions on the table surface. The robot is free to roam around the surface of the table, but it is prevented from falling to destruction. Any movement that would result in the robot falling from the table is prevented, however further valid movement commands is still allowed.

How to command the robot

PLACE X,Y,F - will put the toy robot on the table in position X,Y and facing NORTH, SOUTH, EAST or WEST.
MOVE - will move the toy robot one unit forward in the direction it is currently facing.
LEFT | RIGHT - will rotate the robot in the specified direction without changing the position of the robot.
REPORT - will announce the X,Y and F of the robot.
RESET - will reset the simulator and remove the robot from the table.

test
