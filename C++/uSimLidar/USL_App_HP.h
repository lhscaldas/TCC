/*****************************************/
/*    NAME: Luiz Henrique Souza Caldas   */
/*    ORGN: USP                          */
/*    FILE: USL_App.cpp                  */
/*    DATE: 25 set 2021                  */
/*                                       */
/*****************************************/

#ifndef U_SIM_LIDAR_APP_HEADER
#define U_SIM_LIDAR_APP_HEADER

#include <vector>
#include <string>
#include <map>
#include "MOOS/libMOOS/Thirdparty/AppCasting/AppCastingMOOSApp.h"
#include "VarDataPair.h"
#include "NodeRecord.h"
#include "XYRangePulse.h"
#include "XYArc.h"

class USL_App : public AppCastingMOOSApp
{
 public:
  USL_App();
  virtual ~USL_App() {}

  bool  OnNewMail(MOOSMSG_LIST &NewMail);
  bool  OnStartUp();
  bool  Iterate();
  bool  OnConnectToServer();

  void  registerVariables();
  bool  buildReport();

 protected: // Incoming mail utility
  bool    handleNodeReport(const std::string&);
  bool    handleRangeRequest(const std::string&);

 protected: // Outgoing mail utility
  void    postNodeRangeReport(const std::string&, const std::string&, double rng); 
  void    postRangePulse(const std::string&, const std::string& color,
			 const std::string& label, double dur, double radius);

 protected: // Utilities
  double  getTrueNodeNodeRange(const std::string&, const std::string&);
  double  getTrueNodeHeading(const std::string&);
  double  getTrueNodeNodeBearing(const std::string&, const std::string&);
  double  getNoisyNodeNodeRange(double true_range) const;
  bool    setPushDistance(std::string);
  bool    setPullDistance(std::string);
  bool    setPingWait(std::string);
  bool    setReportVars(std::string);
  bool    setRandomNoiseAlgorithm(std::string);
  bool    setAllowableEchoTypes(std::string);
  bool    allowableEchoType(std::string);
  bool    setSensorArc(std::string);

 protected: // State variables

  // Map is keyed on the name of the vehicle
  std::map<std::string, NodeRecord>   m_map_node_records;
  std::map<std::string, unsigned int> m_map_node_reps_recd;
  std::map<std::string, unsigned int> m_map_node_pings_gend;
  std::map<std::string, unsigned int> m_map_node_echos_recd;
  std::map<std::string, unsigned int> m_map_node_echos_sent;
  std::map<std::string, unsigned int> m_map_node_xping_freq;
  std::map<std::string, unsigned int> m_map_node_xping_dist;
  std::map<std::string, double>       m_map_node_last_ping;

 protected: // Configuration variables
  double               m_default_node_push_dist;
  double               m_default_node_pull_dist;
  double               m_default_node_ping_wait;
  std::vector<double>  m_left_arcs;
  std::vector<double>  m_right_arcs;

  // Map is keyed on the name of the vehicle
  std::map<std::string, double> m_map_node_push_dist;
  std::map<std::string, double> m_map_node_pull_dist;
  std::map<std::string, double> m_map_node_ping_wait;

  std::vector<std::string> m_allow_echo_types;

  std::string m_ping_color;
  std::string m_echo_color;
  std::string m_report_vars;
  bool        m_ground_truth;

  std::string m_rn_algorithm;   // Empty string = no random noise
  double      m_rn_uniform_pct;
  double      m_rn_gaussian_sigma;

  std::string m_ignore_group;
  
  bool        m_display_range_pulse;
};

#endif 








