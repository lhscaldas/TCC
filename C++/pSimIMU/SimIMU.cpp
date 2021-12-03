/************************************************************/
/*    NAME: lhscaldas                                       */
/*    ORGN: USP, São Paulo SP                               */
/*    FILE: SimIMU.cpp                                      */
/*    DATE: 14/06/2021                                      */
/************************************************************/

#include <iterator>
#include "MBUtils.h"
#include "ACTable.h"
#include "SimIMU.h"
#include <math.h>

using namespace std;

//---------------------------------------------------------
// Constructor

SimIMU::SimIMU()
{
   m_real_speed=0;
   m_real_heading=0;
   m_real_x=0;
   m_real_y=0;
   m_real_v=0;
   m_real_r=0;
   
   m_imu_speed=0;
   m_imu_heading=0;
   m_imu_x=0;
   m_imu_y=0;
   m_imu_r=0;
   m_imu_v=0;

   m_pos_error=0;
   m_speed_error=0;
   m_hdg_error=0;
   m_rot_error=0;
}

//---------------------------------------------------------
// Destructor

SimIMU::~SimIMU()
{
}

//---------------------------------------------------------
// Procedure: OnNewMail

bool SimIMU::OnNewMail(MOOSMSG_LIST &NewMail)
{
  AppCastingMOOSApp::OnNewMail(NewMail);

  MOOSMSG_LIST::iterator p;
  for(p=NewMail.begin(); p!=NewMail.end(); p++) {
    CMOOSMsg &msg = *p;
    if (msg.GetKey() == "REAL_X" && msg.IsDouble()) {
      m_real_x = msg.GetDouble();
    } else if (msg.GetKey() == "REAL_Y" && msg.IsDouble()) {
      m_real_y = msg.GetDouble();
    } else if (msg.GetKey() == "REAL_V" && msg.IsDouble()) {
      m_real_v = msg.GetDouble();
    } else if (msg.GetKey() == "REAL_R" && msg.IsDouble()) {
      m_real_r = msg.GetDouble();
    } else if (msg.GetKey() == "REAL_HEADING" && msg.IsDouble()) {
      m_real_heading = msg.GetDouble();
    } else if (msg.GetKey() == "REAL_SPEED" && msg.IsDouble()) {
      m_real_speed = msg.GetDouble();
    }
  }

#if 0 // Keep these around just for template
    string comm  = msg.GetCommunity();
    double dval  = msg.GetDouble();
    string sval  = msg.GetString(); 
    string msrc  = msg.GetSource();
    double mtime = msg.GetTime();
    bool   mdbl  = msg.IsDouble();
    bool   mstr  = msg.IsString();
#endif
	
   return(true);
}

//---------------------------------------------------------
// Procedure: OnConnectToServer

bool SimIMU::OnConnectToServer()
{
   registerVariables();
   return(true);
}

//---------------------------------------------------------
// Procedure: Iterate()
//            happens AppTick times per second

bool SimIMU::Iterate()
{
  AppCastingMOOSApp::Iterate();
  double pos_noise = MOOSWhiteNoise(m_pos_error);
  double speed_noise = MOOSWhiteNoise(m_speed_error);
  double hdg_noise = MOOSWhiteNoise(m_hdg_error);
  double rot_noise = MOOSWhiteNoise(m_rot_error);

  m_imu_heading = m_real_heading + hdg_noise;
  m_imu_speed = m_real_speed + speed_noise;
  m_imu_x = m_real_x + pos_noise;
  m_imu_y = m_real_y + pos_noise;
  m_imu_v = m_real_v + speed_noise;
  m_imu_r = m_real_r + rot_noise;
  
  m_Comms.Notify("IMU_HEADING", m_imu_heading);
  m_Comms.Notify("IMU_SPEED", m_imu_speed);
  m_Comms.Notify("IMU_X", m_imu_x);
  m_Comms.Notify("IMU_Y", m_imu_y);
  m_Comms.Notify("IMU_R", m_imu_r);
  m_Comms.Notify("IMU_V", m_imu_v);

  AppCastingMOOSApp::PostReport();
  return(true);
}

//---------------------------------------------------------
// Procedure: OnStartUp()
//            happens before connection is open

bool SimIMU::OnStartUp()
{
  AppCastingMOOSApp::OnStartUp();

  STRING_LIST sParams;
  m_MissionReader.EnableVerbatimQuoting(false);
  if(!m_MissionReader.GetConfiguration(GetAppName(), sParams))
    reportConfigWarning("No config block found for " + GetAppName());

  STRING_LIST::iterator p;
  for(p=sParams.begin(); p!=sParams.end(); p++) {
    string orig  = *p;
    string line  = *p;
    string param = toupper(biteStringX(line, '='));
    string value = tolower(line);
    double dval  = atof(value.c_str());

    bool handled = false;
    if(param == "SPEED_ERROR") {
      m_speed_error = dval;
      handled = true;
    }
    else if(param == "POS_ERROR") {
      m_pos_error = dval;
      handled = true;
    }
    else if(param == "HDG_ERROR") {
      m_hdg_error = dval;
      handled = true;
    }
    else if(param == "ROT_ERROR") {
      m_rot_error = dval;
      handled = true;
    }

    if(!handled)
      reportUnhandledConfigWarning(orig);
  }
  
  registerVariables();
  return(true);
}

//---------------------------------------------------------
// Procedure: registerVariables

void SimIMU::registerVariables()
{
  AppCastingMOOSApp::RegisterVariables();
  Register("REAL_X", 0);
  Register("REAL_Y", 0);
  Register("REAL_V", 0);
  Register("REAL_R", 0);
  Register("REAL_SPEED", 0);
  Register("REAL_HEADING", 0);
}


//------------------------------------------------------------
// Procedure: buildReport()

bool SimIMU::buildReport() 
{
  m_msgs << "============================================" << endl;
  m_msgs << "File:                                       " << endl;
  m_msgs << "============================================" << endl;

  // ACTable actab(6);
  // actab << "t_ant | t_now | dt | m_real_rot | m_imu_heading | app_name";
  // actab.addHeaderLines();
  // actab << m_t_ant << m_t_now << m_dt << m_real_rot << m_imu_heading << GetAppName();
  // m_msgs << actab.getFormattedString();

  return(true);
}




