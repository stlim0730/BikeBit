/*
 TITLE: BikerBit
 AUTHOR: Seongtaek Lim
 LATEST UPDATE: Nov 27 2014
 
 ARDUINO SCHEMATIC:
 
 SD CARD SLOT
 CS -> 4
 MOSI -> ~11
 MISO -> 12
 SCK -> 13
 5V
 GND
 
 HALL EFFECT SENSOR
 DATA -> 7
 5V
 GND
 
 STATUS LED
 DATA -> ~9
 GND
 */

#include <SD.h>

// START CONSTANTS
// START CONTROL CONSTANTS
#define SERIAL_PORT 9600
//#define LOOP_DELAY 100
#define SECOND 1000
// END CONTROL CONSTANTS

// START DATA MODULE CONSTANTS
// On the Ethernet Shield, CS is pin 4. Note that even if it's not
// used as the CS pin, the hardware CS pin (10 on most Arduino boards,
// 53 on the Mega) must be left as an output or the SD library
// functions will not work.
#define CHIP_SELECT 4
#define DEFAULT_CHIP_SELECT 10
// END DATA MODULE CONSTANTS

// START HALL EFFECT MODULE CONSTANTS
#define HALL_PIN 7
// END HALL EFFECT MODULE CONSTANTS

// START STATUS LED MODULE CONSTANTS
#define LED_PIN 9
// END STATUS LED MODULE CONSTANTS
// END CONSTANTS

// START GLOBAL VARIABLES
char FILE_NAME[] = "BikerBit.dat";
byte hallState = 0;
// END GLOBAL VARIABLES

void setup()
{
  // START SERIAL CONNECTION
  Serial.begin(SERIAL_PORT);
  // END SERIAL CONNECTION

  // START SETTING DATA MODULE
  Serial.print("Initializing SD card...");
  // make sure that the default chip select pin is set to
  // output, even if you don't use it:
  pinMode(DEFAULT_CHIP_SELECT, OUTPUT);
  // see if the card is present and can be initialized:
  if (!SD.begin(CHIP_SELECT)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  Serial.println("card initialized.");
  // END SETTING DATA MODULE

  // START SETTING STATUS LED MODULE
  pinMode(LED_PIN, OUTPUT);
  // END SETTING STATUS LED MODULE
}

void loop()
{
  hallState = digitalRead(HALL_PIN);

  if(hallState) {
    // MAGNETIC FIELD ISN'T DETECTED
    // TURN OFF STATUS LED
    analogWrite(LED_PIN, LOW);
  }
  else {
    // MAGNETIC FIELD IS DETECTED
    // TURN ON STATUS LED
    analogWrite(LED_PIN, HIGH);
    
    // RECORD TIMESTAMP
    String timestamp = String(millis());
    File dataFile = SD.open(FILE_NAME, FILE_WRITE);
    if(dataFile) {
      dataFile.println(timestamp);
      dataFile.close();
      // print to the serial port too:
      Serial.println(timestamp);
    }
    else {
      Serial.println("error opening " + String(FILE_NAME));
    }
  }
  
  // delay(LOOP_DELAY);
}

