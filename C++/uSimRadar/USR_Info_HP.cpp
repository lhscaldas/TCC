/*****************************************/
/*    NAME: Luiz Henrique Souza Caldas   */
/*    ORGN: USP                          */
/*    FILE: USR_App.cpp                  */
/*    DATE: 25 set 2021                  */
/*                                       */
/*****************************************/
 
#include <cstdlib>
#include <iostream>
#include "ColorParse.h"
#include "USR_Info_HP.h"
#include "ReleaseInfo.h"

using namespace std;

//----------------------------------------------------------------
// Procedure: showSynopsis

void showSynopsis()
{
  blk("SYNOPSIS:                                                       ");
  blk("------------------------------------                            ");
  blk("  Typically run in a shoreside community. Takes reports from    ");
  blk("  remote vehicles, notes their position. Takes a range request  ");
  blk("  from a remote vehicle and returns a range report indicating   ");
  blk("  that vehicle's range to nearby vehicles. Range requests may   ");
  blk("  or may not be answered dependent on inter-vehicle range.      ");
  blk("  Reports may also have noise added to their range values.      ");
}

//----------------------------------------------------------------
// Procedure: showHelp

void showHelpAndExit()
{
  blk("                                                          ");
  blu("==========================================================");
  blu("Usage: uSimRadar file.moos [OPTIONS]         ");
  blu("==========================================================");
  blk("                                                          ");
  showSynopsis();
  blk("                                                          ");
  blk("Options:                                                  ");
  mag("  --alias","=<ProcessName>                                ");
  blk("      Launch uSimRadar with the given        ");
  blk("      process name rather than uSimRadar.    ");
  mag("  --example, -e                                           ");
  blk("      Display example MOOS configuration block.           ");
  mag("  --help, -h                                              ");
  blk("      Display this help message.                          ");
  mag("  --interface, -i                                         ");
  blk("      Display MOOS publications and subscriptions.        ");
  mag("  --version,-v                                            ");
  blk("      Display release version of uSimRadar.  ");
  mag("  --verbose","=<setting>                                  ");
  blk("      Set verbosity. true or false (default)              ");
  blk("                                                          ");
  blk("Note: If argv[2] does not otherwise match a known option, ");
  blk("      then it will be interpreted as a run alias. This is ");
  blk("      to support pAntler launching conventions.           ");
  blk("                                                          ");
  exit(0);
}


//----------------------------------------------------------------
// Procedure: showExampleConfigAndExit

void showExampleConfigAndExit()
{
  blk("                                                                ");
  blu("=============================================================== ");
  blu("uSimRadar Example MOOS Configuration               ");
  blu("=============================================================== ");
  blk("                                                                ");
  blk("ProcessConfig = uContactRangeSensor                             ");
  blk("{                                                               ");
  blk("  AppTick   = 4                                                 ");
  blk("  CommsTick = 4                                                 ");
  blk("                                                                ");
  blk("  // Configuring aspects of the vehicles in the sim             ");
  blk("  push_dist  = default = 100  // in meters or {nolimit}         ");
  blk("  pull_dist  = default = 100  // in meters or {nolimit}         ");
  blk("  ping_wait  = default = 30   // in seconds                     ");
  blk("                                                                ");
  blk("  allow_echo_types = uuv                                        ");
  blk("                                                                ");
  blk("  // Configuring manner of reporting                            ");
  blk("  report_vars    = short // or {long, both}                     ");
  blk("  ground_truth   = true  // or {false}                          ");
  blk("  verbose        = true  // or {false}                          ");
  blk("  display_pulses = true  // or {false}                          ");
  blk("                                                                ");
  blk("  // Configuring visual artifacts                               ");
  blk("  ping_color     = white                                        ");
  blk("  echo_color     = chartreuse                                   ");
  blk("                                                                ");
  blk("  // Configuring Artificial Noise                               ");
  blk("  rn_uniform_pct    = 0.5                                        ");
  blk("  rn_gaussian_sigma = 1.5                                       ");
  blk("                                                                ");
  blk("  // Configuring Sensor Arcs                                    ");
  blk("  sensor_arc = 45:135,225:315 // or {315:45} for front          ");
  blk("  // sensor_arc = 315:45      // just for front                 ");
  blk("  // sensor_arc = 360         // default, sets full circle      ");
  blk("                                                                ");
  blk("}                                                               ");
  blk("                                                                ");
  exit(0);
}


//----------------------------------------------------------------
// Procedure: showInterfaceAndExit

void showInterfaceAndExit()
{
  blk("                                                                ");
  blu("=============================================================== ");
  blu("uSimRadar INTERFACE                                ");
  blu("=============================================================== ");
  blk("                                                                ");
  showSynopsis();
  blk("                                                                ");
  blk("SUBSCRIPTIONS:                                                  ");
  blk("------------------------------------                            ");
  blk("  NODE_REPORT                                                   ");
  blk("  NODE_REPORT_LOCAL = NAME=alpha,TYPE=UUV,TIME=1252348077.59,   ");
  blk("                      X=51.71,Y=-35.50, LAT=43.824981,          ");
  blk("                      LON=-70.329755,SPD=2.0,HDG=118.8,         ");
  blk("                      YAW=118.8,DEPTH=4.6,LENGTH=3.8,           ");
  blk("                      MODE=MODE@ACTIVE:LOITERING                ");
  blk("  USR_RANGE_REQUEST = name=archie                               ");
  blk("                                                                ");
  blk("PUBLICATIONS:                                                   ");
  blk("------------------------------------                            ");
  blk("  USR_RANGE_REPORT    = vname=archie,range=126.54,              ");
  blk("                        target=jackal,time=19656022406.44       ");
  blk("  USR_RANGE_REPORT_GT = vname=archie,range=126.54,              ");
  blk("                        target=jackal,time=19656022406.44       ");
  blk("  VIEW_RANGE_PULSE    = x=-40,y=-150,radius=40,duration=15,     ");
  blk("                        fill=0.25,fill_color=green,label=04,    ");
  blk("                        edge_color=green,time=3892830128.5,     ");
  blk("                        edge_size=1                             ");
  exit(0);
}

//----------------------------------------------------------------
// Procedure: showReleaseInfoAndExit

void showReleaseInfoAndExit()
{
  showReleaseInfo("uSimRadar", "gpl");
  exit(0);
}








