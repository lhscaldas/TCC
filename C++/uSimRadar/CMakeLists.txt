#--------------------------------------------------------
# The CMakeLists.txt for:          uSimRadar
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
   USR_App_HP.cpp
   USR_Info_HP.cpp
   main.cpp
)

ADD_EXECUTABLE(uSimRadar ${SRC})

TARGET_LINK_LIBRARIES(uSimRadar
  ${MOOS_LIBRARIES}
  apputil
  mbutil
  geometry 
  contacts
  ${SYSTEM_LIBS}
)
