/************************************************************/
/*    NAME: lhscaldas                                       */
/*    ORGN: USP, São Paulo SP                               */
/*    FILE: SimIMU.h                                        */
/*    DATE: 17/06/2021                                      */
/************************************************************/

#ifndef SimDVL_HEADER
#define SimDVL_HEADER

#include "MOOS/libMOOS/Thirdparty/AppCasting/AppCastingMOOSApp.h"

class SimDVL : public AppCastingMOOSApp
{
 public:
   SimDVL();
   ~SimDVL();

 protected: // Standard MOOSApp functions to overload  
   bool OnNewMail(MOOSMSG_LIST &NewMail);
   bool Iterate();
   bool OnConnectToServer();
   bool OnStartUp();

 protected: // Standard AppCastingMOOSApp function to overload 
   bool buildReport();

 protected:
   void registerVariables();

 protected:
   double m_real_speed;
   double m_dvl_speed;
   double m_speed_error;

 private: // Configuration variables

 private: // State variables
};

#endif 
