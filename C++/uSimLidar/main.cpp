/*****************************************/
/*    NAME: Luiz Henrique Souza Caldas   */
/*    ORGN: USP                          */
/*    FILE: USL_App.cpp                  */
/*    DATE: 25 set 2021                  */
/*                                       */
/*****************************************/

#include <iostream>
#include "MBUtils.h"
#include "ColorParse.h"
#include "USL_App_HP.h"
#include "USL_Info_HP.h"

using namespace std;

int main(int argc, char *argv[])
{
  string mission_file;
  string run_command = argv[0];
  string verbose;

  for(int i=1; i<argc; i++) {
    string argi = argv[i];
    if((argi=="-v") || (argi=="--version") || (argi=="-version"))
      showReleaseInfoAndExit();
    else if((argi=="-e") || (argi=="--example") || (argi=="-example"))
      showExampleConfigAndExit();
    else if((argi=="-h") || (argi == "--help") || (argi=="-help"))
      showHelpAndExit();
    else if((argi=="-i") || (argi == "--interface"))
      showInterfaceAndExit();
    else if(strEnds(argi, ".moos") || strEnds(argi, ".moos++"))
      mission_file = argv[i];
    else if(strBegins(argi, "--alias="))
      run_command = argi.substr(8);
    else if(i == 2)
      run_command = argi;
  }
  
  if(mission_file == "")
    showHelpAndExit();

  cout << termColor("green");
  cout << "uSimRadar Launching as " << run_command << endl;
  cout << termColor() << endl;

  USL_App contact_range_sensor;

  contact_range_sensor.Run(run_command.c_str(), mission_file.c_str(), argc, argv);
 
  return(0);
}









