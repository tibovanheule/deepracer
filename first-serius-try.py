
import math

def reward_function(params):
    is_offtrack = params['is_offtrack']
    if is_offtrack:
        return -1e5
    
    # Read input parameters
    distance_from_center = params['distance_from_center']
    reward = math.exp(-6*distance_from_center)
    
    progress = params['progress']/100.0 #scale to 0...1
    waypoints = params['waypoints']
    throttle = params['speed']/5.0
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    
    if progress == 1:
        reward = 1e5
    else:
        reward *= progress
        
    ######################
    ###### Steering ######
    ######################

    # 
    waypoint_yaw = waypoints[closest_waypoints[0]][-1]
    if abs(heading - waypoint_yaw) >= math.radians(10):
        reward *= 0.25

    # penalize reward if the car is steering too much
    ABS_STEERING_THRESHOLD = 0.85
    if abs(params['steering_angle']) > ABS_STEERING_THRESHOLD:
        reward *= 0.75

    ######################
    ###### Throttle ######
    ######################

    # Gotta go fast
    reward *= 0.5 + throttle

    # decrease throttle while steering to some extent
    if throttle > 1 - (0.4 * abs(params['steering_angle'])):
        reward *= 0.8

    # min max
    if reward < -1e5:
        return float(-1e5)
    elif reward > 1e5:
        return float(1e5)

    return float(reward)
