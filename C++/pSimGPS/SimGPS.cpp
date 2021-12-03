/************************************************************/
/*    NAME: lhscaldas                                       */
/*    ORGN: USP, São Paulo SP                               */
/*    FILE: SimGPS.cpp                                      */
/*    DATE: 14/06/2021                                      */
/************************************************************/

#include <iterator>
#include "MBUtils.h"
#include "ACTable.h"
#include "SimGPS.h"
#include <math.h>

using namespace std;

//---------------------------------------------------------
// Constructor

SimGPS::SimGPS()
{
   m_real_x=0;
   m_gps_x=0;
   m_real_y=0;
   m_gps_y=0;
   m_gps_lat=0;
   m_gps_lon=0;

   m_real_speed=0;
   m_gps_speed=0;

   m_pos_error=0;
   m_speed_error=0;
}

//---------------------------------------------------------
// Destructor

SimGPS::~SimGPS()
{
}

//---------------------------------------------------------
// Procedure: OnNewMail

bool SimGPS::OnNewMail(MOOSMSG_LIST &NewMail)
{
  AppCastingMOOSApp::OnNewMail(NewMail);

  MOOSMSG_LIST::iterator p;
  for(p=NewMail.begin(); p!=NewMail.end(); p++) {
    CMOOSMsg &msg = *p;
    if (msg.GetKey() == "REAL_X" && msg.IsDouble()) {
      m_real_x = msg.GetDouble();
    } else if (msg.GetKey() == "REAL_Y" && msg.IsDouble()) {
      m_real_y = msg.GetDouble();
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

bool SimGPS::OnConnectToServer()
{
   registerVariables();
   return(true);
}

//---------------------------------------------------------
// Procedure: Iterate()
//            happens AppTick times per second

bool SimGPS::Iterate()
{
  AppCastingMOOSApp::Iterate();
  double pos_noise = MOOSWhiteNoise(m_pos_error);
  m_gps_x=m_real_x + pos_noise;
  m_gps_y=m_real_y + pos_noise;
  m_Comms.Notify("GPS_X", m_gps_x);
  m_Comms.Notify("GPS_Y", m_gps_y);

  m_geodesy.LocalGrid2LatLong(m_gps_x, m_gps_y, m_gps_lat, m_gps_lon);
  m_Comms.Notify("NAV_LAT", m_gps_lat);
  m_Comms.Notify("NAV_LONG", m_gps_lon);
  m_Comms.Notify("REAL_LAT", m_gps_lat);
  m_Comms.Notify("REAL_LONG", m_gps_lon);
  
  double spd_noise = MOOSWhiteNoise(m_speed_error);
  m_gps_speed=m_real_speed + spd_noise;
  m_Comms.Notify("GPS_SPEED", m_gps_speed);

  AppCastingMOOSApp::PostReport();
  return(true);
}

//---------------------------------------------------------
// Procedure: OnStartUp()
//            happens before connection is open

bool SimGPS::OnStartUp()
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

    if(!handled)
      reportUnhandledConfigWarning(orig);

    // look for latitude, longitude global variables
    double latOrigin, longOrigin;
    m_MissionReader.GetValue("LatOrigin", latOrigin);
    m_MissionReader.GetValue("LongOrigin", longOrigin);
    m_geodesy.Initialise(latOrigin, longOrigin);

  }
  registerVariables();
  return(true);
}

//---------------------------------------------------------
// Procedure: registerVariables

void SimGPS::registerVariables()
{
  AppCastingMOOSApp::RegisterVariables();
  Register("REAL_X", 0);
  Register("REAL_Y", 0);
  Register("REAL_SPEED", 0);
}


//------------------------------------------------------------
// Procedure: buildReport()

bool SimGPS::buildReport() 
{
  m_msgs << "============================================" << endl;
  m_msgs << "File:                                       " << endl;
  m_msgs << "============================================" << endl;

  // ACTable actab(6);
  // actab << "t_ant | t_now | dt | vx | vy | gps_speed";
  // actab.addHeaderLines();
  // actab << m_t_ant << m_t_now << m_dt << m_vx << m_vy << m_gps_speed;
  // m_msgs << actab.getFormattedString();

  return(true);
}




