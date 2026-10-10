cmake_minimum_required(VERSION 3.5)
project(asymmetric_radiation_nav)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch maps behavior_trees
  DESTINATION share/${PROJECT_NAME}
)

ament_package()