
import math

# Collinear: d == 0
# Clockwise turn: d > 0
# Counterclockwise turn: d < 0
# This is used to progmatically determine how fast we can go.
def is_ccw(p0, p1, p2):
    return ((p1[0] - p0[0]) * (p2[1] - p0[1]) -  (p2[0] - p0[0]) * (p1[1] - p0[1]))

def reward_function(params):

    
    is_offtrack = params['is_offtrack']
    if is_offtrack:
        return 0.001
    
    # Read input parameters
    distance_from_center = params['distance_from_center']
    reward = math.exp(-6*distance_from_center)
    
    waypoints = params['waypoints']
    throttle = params['speed']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # if steering is too much a away from next heading () to big angle, give smaller reward
    waypoint_yaw = waypoints[closest_waypoints[1]][-1]
    if abs(heading - waypoint_yaw) >= math.radians(10):
        reward *= 0.25
    else:
        reward *= 1.20

    # indexes
    current_waypoint = closest_waypoints[1] - 1
    next_waypoint = closest_waypoints[1] % len(waypoints)
    next_next_waypoint = (closest_waypoints[1] + 1) % len(waypoints)
    
    waypoint_first = waypoints[current_waypoint]
    waypoint_second = waypoints[next_waypoint]
    waypoint_third = waypoints[next_next_waypoint]

    turn = is_ccw(waypoint_first,waypoint_second,waypoint_third)
  
    if abs(turn) < 0.01:
        # go fast, next 3 waypoint are nearly on one line
        if speed == 3:
          reward += 14
        else:
          reward -= (5-speed)**2
    elif abs(turn) < 0.02:
        # go medium, next 3 waypoint are not exactly on one line, small turn
        if speed == 2:
          reward += 14
        else:
          reward -= 7
    else:
        # go slow, next 3 waypoint are not on one line
        if speed == 1:
          reward += 14
        else:
          reward -= (2+speed)**2

  
    if reward > 1e5:
        return float(1e5)
    
    return float(reward)
