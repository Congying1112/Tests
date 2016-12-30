cmake_minimum_required(VERSION 3.3)
project("test-match")

find_package( OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})


set(SOURCE_FILES main.cpp)

add_executable(${PROJECT_NAME} ${SOURCE_FILES})

target_link_libraries( ${PROJECT_NAME} ${OpenCV_LIBS})
