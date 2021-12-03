/************************************************************/
/*    NAME: lhscaldas                                       */
/*    ORGN: USP, São Paulo SP                               */
/*    FILE: SimGPS.h                                        */
/*    DATE: 14/06/2021                                      */
/************************************************************/

#ifndef SimGPS_HEADER
#define SimGPS_HEADER
#include "MOOS/libMOOS/Thirdparty/AppCasting/AppCastingMOOSApp.h"
#include "MOOSGeodesy.h"
class SimGPS : public AppCastingMOOSApp
{
 public:
   SimGPS();
   ~SimGPS();

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
   CMOOSGeodesy m_geodesy;
   double m_real_x;
   double m_gps_x;
   double m_real_y;
   double m_gps_y;
   double m_gps_lat;
   double m_gps_lon;
   double m_real_speed;
   double m_gps_speed;

   double m_pos_error;
   double m_speed_error;


 private: // Configuration variables

 private: // State variables
};

#endif 
