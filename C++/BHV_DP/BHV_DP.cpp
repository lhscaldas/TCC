/*****************************************************************/
/*    NAME: M.Benjamin, H.Schmidt, J. Leonard                    */
/*    ORGN: Dept of Mechanical Eng / CSAIL, MIT Cambridge MA     */
/*    FILE: BHV_DP.cpp                               */
/*    DATE: July 1st 2008  (For purposes of simple illustration) */
/*                                                               */
/* This program is free software; you can redistribute it and/or */
/* modify it under the terms of the GNU General Public License   */
/* as published by the Free Software Foundation; either version  */
/* 2 of the License, or (at your option) any later version.      */
/*                                                               */
/* This program is distributed in the hope that it will be       */
/* useful, but WITHOUT ANY WARRANTY; without even the implied    */
/* warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR       */
/* PURPOSE. See the GNU General Public License for more details. */
/*                                                               */
/* You should have received a copy of the GNU General Public     */
/* License along with this program; if not, write to the Free    */
/* Software Foundation, Inc., 59 Temple Place - Suite 330,       */
/* Boston, MA 02111-1307, USA.                                   */
/*****************************************************************/

#include <cstdlib>
#include <math.h>
#include "BHV_DP.h"
#include "MBUtils.h"
#include "AngleUtils.h"
#include "BuildUtils.h"
#include "ZAIC_PEAK.h"
#include "OF_Coupler.h"
#include "OF_Reflector.h"
#include "AOF_DP.h"

using namespace std;

//-----------------------------------------------------------
// Procedure: Constructor

BHV_DP::BHV_DP(IvPDomain gdomain) : 
  IvPBehavior(gdomain)
{
  IvPBehavior::setParam("name", "DP");
  m_domain = subDomain(m_domain, "course,speed");

  // All distances are in meters, all speed in meters per second
  // Default values for configuration parameters 
  m_desired_speed  = 0; 
  m_arrival_radius = 10;
  m_ipf_type       = "zaic";

  // Default values for behavior state variables
  m_osx  = 0;
  m_osy  = 0;

  addInfoVars("NAV_X, NAV_Y");
}

//---------------------------------------------------------------
// Procedure: setParam - handle behavior configuration parameters

bool BHV_DP::setParam(string param, string val) 
{
  // Convert the parameter to lower case for more general matching
  param = tolower(param);

  double double_val = atof(val.c_str());
  if((param == "ptx")  && (isNumber(val))) {
    m_nextpt.set_vx(double_val);
    return(true);
  }
  else if((param == "pty") && (isNumber(val))) {
    m_nextpt.set_vy(double_val);
    return(true);
  }
  else if((param == "heading") && (isNumber(val))) {
    m_desired_hdg = double_val;
    return(true);
  }
  else if((param == "speed") && (double_val > 0) && (isNumber(val))) {
    m_desired_speed = double_val;
    return(true);
  }
  else if((param == "radius") && (double_val > 0) && (isNumber(val))) {
    m_arrival_radius = double_val;
    return(true);
  }
  else if(param == "ipf_type") {
    val = tolower(val);    
    if((val == "zaic") || (val == "reflector")) {
      m_ipf_type = val;
      return(true);
    }
  }
  return(false);
}

//-----------------------------------------------------------
// Procedure: onIdleState

void BHV_DP::onIdleState() 
{
  postViewPoint(false);
  postMessage("DP_MODE", "OFF");
  postStationMessage(false);
}

//-----------------------------------------------------------
// Procedure: postViewPoint

void BHV_DP::postViewPoint(bool viewable) 
{
  m_nextpt.set_label(m_us_name + "'s next waypoint");
  
  string point_spec;
  if(viewable)
    point_spec = m_nextpt.get_spec("active=true");
  else
    point_spec = m_nextpt.get_spec("active=false");
  postMessage("VIEW_POINT", point_spec);
}

//-----------------------------------------------------------
// Procedure: onRunState

IvPFunction *BHV_DP::onRunState() 
{
  // Part 1: Get vehicle position from InfoBuffer and post a 
  // warning if problem is encountered
  bool ok1, ok2;
  m_osx = getBufferDoubleVal("NAV_X", ok1);
  m_osy = getBufferDoubleVal("NAV_Y", ok2);
  if(!ok1 || !ok2) {
    postWMessage("No ownship X/Y info in info_buffer.");
    return(0);
  }
  
  // Part 2: Determine if the vehicle has reached the destination point
#ifdef WIN32
  double dist = _hypot((m_nextpt.x()-m_osx), (m_nextpt.y()-m_osy));
#else
  double dist = hypot((m_nextpt.x()-m_osx), (m_nextpt.y()-m_osy));
#endif

  // Part 3: Post the waypoint as a string for consumption by 
  // a viewer application.
  postViewPoint(true);
  postStationMessage(true);

  // Part 4: Build the IvP function with either the ZAIC tool 
  // or the Reflector tool.
  double desired_speed = 0;
  if(dist >= m_arrival_radius) {
    desired_speed = m_desired_speed;
    postMessage("DP_MODE", "OFF");
  }
  else{
    postMessage("DP_MODE", "ON");
    postMessage("DP_X", m_nextpt.x());
    postMessage("DP_Y", m_nextpt.y());
    postMessage("DP_HEADING", m_desired_hdg);
  }

  ZAIC_PEAK spd_zaic(m_domain, "speed");
  spd_zaic.setSummit(desired_speed);
  spd_zaic.setBaseWidth(0.4);
  spd_zaic.setPeakWidth(0.0);
  spd_zaic.setSummitDelta(0.0);
  spd_zaic.setMinMaxUtil(0, 25);
  IvPFunction *spd_ipf = spd_zaic.extractIvPFunction();
  
  double rel_ang_to_wpt = relAng(m_osx, m_osy, m_nextpt.x(), m_nextpt.y());
  ZAIC_PEAK crs_zaic(m_domain, "course");
  crs_zaic.setSummit(rel_ang_to_wpt);
  crs_zaic.setBaseWidth(180.0);
  crs_zaic.setValueWrap(true);
  IvPFunction *crs_ipf = crs_zaic.extractIvPFunction();
  
  OF_Coupler coupler;
  IvPFunction *ipf = coupler.couple(crs_ipf, spd_ipf);

  if(ipf)
    ipf->setPWT(m_priority_wt);
  
  return(ipf);
}

void BHV_DP::postStationMessage(bool post)
{
  string str_x = doubleToString(m_nextpt.x(),1);
  string str_y = doubleToString(m_nextpt.y(),1);

  string poly_str = "radial:: x=" + str_x;
  poly_str += ",y=" + str_y;
  poly_str += ",source=DP";
  poly_str += ",pts=32";

  string poly_str_outer = poly_str;
  poly_str_outer += ",label= DP:station-keep-out";
  poly_str_outer += ",radius=" + doubleToString(m_arrival_radius,1);

  if(post==false) {
    poly_str_outer += ",active=false";
  }

  postMessage("VIEW_POLYGON", poly_str_outer, "outer");
}
