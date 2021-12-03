#--------------------------------------------------------
# The CMakeLists.txt for:          uSimLidar
# Author(s):                       lhscaldas
#--------------------------------------------------------

# Set System Specific Libraries
if (${WIN32})
  SET(SYSTEM_LIBS
    wsock32)
else (${WIN32})
  SET(SYSTEM_LIBS
    m
    pthread)
endif (${WIN32})

SET(SRC
   USL_App_HP.cpp
   USL_Info_HP.cpp
   main.cpp
)

ADD_EXECUTABLE(uSimLidar ${SRC})

TARGET_LINK_LIBRARIES(uSimLidar
  ${MOOS_LIBRARIES}
  apputil
  mbutil
  geometry 
  contacts
  ${SYSTEM_LIBS}
)
