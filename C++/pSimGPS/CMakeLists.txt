#--------------------------------------------------------
# The CMakeLists.txt for:                       pSimGPS
# Author(s):                              lhscaldas
#--------------------------------------------------------

SET(SRC
  SimGPS.cpp
  MOOSGeodesy.cpp
  SimGPS_Info.cpp
  main.cpp
)

ADD_EXECUTABLE(pSimGPS ${SRC})

TARGET_LINK_LIBRARIES(pSimGPS
   ${MOOS_LIBRARIES}
   apputil
   mbutil
   m
   pthread)

