/************************************************************/
/*    NAME: lhscaldas                                       */
/*    ORGN: USP, São Paulo SP                               */
/*    FILE: SimIMU.h                                        */
/*    DATE: 14/06/2021                                      */
/************************************************************/

#ifndef SimIMU_HEADER
#define SimIMU_HEADER

#include "MOOS/libMOOS/Thirdparty/AppCasting/AppCastingMOOSApp.h"

class SimIMU : public AppCastingMOOSApp
{
 public:
   SimIMU();
   ~SimIMU();

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
   double m_imu_heading;
   double m_imu_speed;
   double m_imu_x;
   double m_imu_y;
   double m_imu_v;
   double m_imu_r;

   double m_real_heading;
   double m_real_speed;
   double m_real_x;
   double m_real_y;
   double m_real_v;
   double m_real_r;

   double m_pos_error;
   double m_speed_error;
   double m_hdg_error;
   double m_rot_error;

 private: // Configuration variables

 private: // State variables
};

#endif 
