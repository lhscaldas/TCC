/************************************************************/
/*    NAME: lhscaldas                                       */
/*    ORGN: USP, São Paulo SP                               */
/*    FILE: SimGyro.h                                        */
/*    DATE: 14/06/2021                                      */
/************************************************************/

#ifndef SimGyro_HEADER
#define SimGyro_HEADER

#include "MOOS/libMOOS/Thirdparty/AppCasting/AppCastingMOOSApp.h"

class SimGyro : public AppCastingMOOSApp
{
 public:
   SimGyro();
   ~SimGyro();

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
   double m_real_heading;
   double m_gyro_heading;

   double m_hdg_error;

 private: // Configuration variables

 private: // State variables
};

#endif 
