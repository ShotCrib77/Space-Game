import math

shot_x = 200
shot_y = 400
angle_radians = math.atan2(shot_y, shot_x)
angle_degrees = math.degrees(angle_radians)

print(angle_degrees)