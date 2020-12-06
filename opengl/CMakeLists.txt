cmake_minimum_required(VERSION 2.8)

project(glproject)
add_executable(main main.cpp)
find_package(OpenGL REQUIRED)
find_package(FreeGLUT REQUIRED)
include_directories( ${GLEW_INCLUDE_DIRS} ${GLFW_INCLUDE_DIRS} ${SOIL_INCLUDE_DIRS})
target_link_libraries(main libopengl32.a ${GLEW_LIBRARY} ${GLFW_LIBRARY} ${SOIL_LIBRARY} )