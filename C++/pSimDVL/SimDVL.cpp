/************************************************************/
/*    NAME: lhscaldas                                       */
/*    ORGN: USP, São Paulo SP                               */
/*    FILE: SimIMU.cpp                                      */
/*    DATE: 17/06/2021                                      */
/************************************************************/

#include <iterator>
#include "MBUtils.h"
#include "ACTable.h"
#include "SimDVL.h"

using namespace std;

//---------------------------------------------------------
// Constructor

SimDVL::SimDVL()
{
   m_real_speed=0;
   m_dvl_speed=0;
   m_speed_error=0;
}

//---------------------------------------------------------
// Destructor

SimDVL::~SimDVL()
{
}

//---------------------------------------------------------
// Procedure: OnNewMail

bool SimDVL::OnNewMail(MOOSMSG_LIST &NewMail)
{
  AppCastingMOOSApp::OnNewMail(NewMail);

  MOOSMSG_LIST::iterator p;
  for(p=NewMail.begin(); p!=NewMail.end(); p++) {
    CMOOSMsg &msg = *p;
    if (msg.GetKey() == "REAL_SPEED" && msg.IsDouble()) {
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

bool SimDVL::OnConnectToServer()
{
   registerVariables();
   return(true);
}

//---------------------------------------------------------
// Procedure: Iterate()
//            happens AppTick times per second

bool SimDVL::Iterate()
{
  AppCastingMOOSApp::Iterate();
  double noise = MOOSWhiteNoise(m_speed_error);
  m_dvl_speed=m_real_speed+noise;
  m_Comms.Notify("DVL_SPEED", m_dvl_speed);
  AppCastingMOOSApp::PostReport();
  return(true);
}

//---------------------------------------------------------
// Procedure: OnStartUp()
//            happens before connection is open

bool SimDVL::OnStartUp()
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

    if(!handled)
      reportUnhandledConfigWarning(orig);

  }
  
  registerVariables();	
  return(true);
}

//---------------------------------------------------------
// Procedure: registerVariables

void SimDVL::registerVariables()
{
  AppCastingMOOSApp::RegisterVariables();
  Register("REAL_SPEED", 0);
}


//------------------------------------------------------------
// Procedure: buildReport()

bool SimDVL::buildReport() 
{
  m_msgs << "============================================" << endl;
  m_msgs << "File:                                       " << endl;
  m_msgs << "============================================" << endl;

  ACTable actab(4);
  actab << "Alpha | Bravo | Charlie | Delta";
  actab.addHeaderLines();
  actab << "one" << "two" << "three" << "four";
  m_msgs << actab.getFormattedString();

  return(true);
}




