project(week16)

add_executable(teapot teapot.cpp)

target_link_libraries(teapot libopengl32.a libglu32.a libfreeglut.dll.a)


set_property(TARGET teapot PROPERTY CXX_STANDARD 17)