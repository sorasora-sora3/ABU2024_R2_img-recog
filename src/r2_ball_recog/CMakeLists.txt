cmake_minimum_required(VERSION 3.0.2)
project(r2_ball_recog)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  #message_generation
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES r2_ball_recog
#  CATKIN_DEPENDS roscpp rospy std_msgs
#  DEPENDS system_lib
)

include_directories(
#  include
  ${catkin_INCLUDE_DIRS}
)

# add_executable(r2-ball-recog src/r2-ball-recog.py)
# target_link_libraries(r2-ball-recog ${catkin_LIBRARIES})

# catkin_install_python(PROGRAMS  nodes/r2-ball-recog DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
# add_excutableとかtarget_link_librariesとかの代わりにcatkin_install_python


