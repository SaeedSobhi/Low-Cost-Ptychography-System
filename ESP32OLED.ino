
//https://unsinnsbasis.de/oled-display-ssd1306/
#include <Adafruit_SSD1306.h>
 
// großes Display am Standard-I2C-Interface
// (SDA Pin 21, SCL Pin 22)
#define DISPLAY_1_I2C_ADDRESS 0x3C // or 0x3D
#define DISPLAY_1_WIDTH 128  // Breite in Pixeln
#define DISPLAY_1_HEIGHT 64  // Höhe in Pixeln
#define I2C_SDA 22
#define I2C_SCL 21
// je I2C-Kanal ein Interface definieren
TwoWire I2C_1 = TwoWire(0);
 
// Datenstrukturen für die Displays
// (-1 -> Display hat keinen Reset-Pin)
Adafruit_SSD1306 display(DISPLAY_1_WIDTH, DISPLAY_1_HEIGHT, &I2C_1, -1);
 
// Bitrate für die Datenübertragung zum seriellen Monitor
// (ESP: z.B. 115200, Arduino: zwingend 9600)
#define BITRATE 115200  // Arduino: 9600
 
void setup() {
  bool status1;
 
  // Übertragungsrate zum seriellen Monitor setzen
  Serial.begin(BITRATE);
  Serial.println("Start");
  
  // beide I2C-Interfaces nutzen
  I2C_1.begin(I2C_SDA, I2C_SCL);  // Standard-Interface

  // Displays initialisieren
  // im Fehlerfall Meldung ausgeben und Programm nicht
  // fortsetzen (leere Dauerschleife))
  status1 = display.begin(SSD1306_SWITCHCAPVCC, DISPLAY_1_I2C_ADDRESS);

  if (!(status1)) {
    Serial.println("Fehler beim Initialisieren der Displays");
    Serial.print("Status Display 1: ");
    Serial.print(status1);
  }
 
  display.clearDisplay();
  display.setTextSize(2);  // große Schrift
  display.setTextColor(SSD1306_WHITE); // helle Schrift auf dunklem Grund
  display.setCursor(0, 0);
  display.print("  150 mum \n Pixelsize");
  display.display();

  delay(1000);
  display.clearDisplay();
  display.display();


  Serial.println("Displaying individiual pixels");
  // draw grid
  
  for (int ix=0; ix<DISPLAY_1_WIDTH/2; ix++){
    for (int iy=0; iy<DISPLAY_1_HEIGHT/2; iy++){
      
      display.drawPixel(ix*2, iy*2, SSD1306_WHITE);
      
    }
  }
  display.display();
  
 
}
 
void loop() {
}
