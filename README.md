# FUI

Parameter Names:

States are ROS parameters that take an int. Macros should be defined for each state as follows: (i.e. #Define Active = 1)
*Shutdown_State
  -1 = Active
  -2 = Prepare_To_Shutdown
  -3 = Shutdown
*Main_State
  -1 = Preflight_Checks
  -2 = Takeoff
  -3 = Tracking_Target
  -4 = Relocating_Target
  
  Topic Names:
  
  Target_Position (Topic to transfer information from VA to DM. VA is publisher, DM is subscriber)
  
