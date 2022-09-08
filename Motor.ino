
#include <Arduino.h>

const int Xpinstep = 13;
const int Xpindir = 12;

const int Ypinstep = 14;
const int Ypindir = 27;

void setup() {
  // Sets the two pins as Outputs
 Serial.begin(115200);
 Serial.setTimeout(.1);
 
pinMode(Xpinstep,OUTPUT); 
pinMode(Xpindir,OUTPUT);

pinMode(Ypinstep,OUTPUT); 
pinMode(Ypindir,OUTPUT);
}
/*
void loop() {
  digitalWrite(Xpindir,HIGH); // Enables the motor to move in a particular direction
  digitalWrite(Ypindir,HIGH);
  // Makes 200 pulses for making one full cycle rotation
  for(int x = 0; x < 200; x++) {
    digitalWrite(Xpinstep,HIGH); 
    digitalWrite(Ypinstep,HIGH); 
    delayMicroseconds(500); 
    digitalWrite(Xpinstep,LOW); 
    digitalWrite(Ypinstep,LOW); 
    delayMicroseconds(500); 
  }
  delay(1000); // One second delay

  digitalWrite(Xpindir,LOW); // Enables the motor to move in a particular direction
  digitalWrite(Ypindir,LOW);
  //digitalWrite(dirPin,LOW); //Changes the rotations direction
  // Makes 400 pulses for making two full cycle rotation
  for(int x = 0; x < 400; x++) {
    digitalWrite(Xpinstep,HIGH); 
    digitalWrite(Ypinstep,HIGH);    
    delayMicroseconds(500);
    digitalWrite(Xpinstep,LOW); 
    digitalWrite(Ypinstep,LOW); 
    delayMicroseconds(500);
  }
  delay(1000);
}*/

void loop() 
{
 while (!Serial.available());
 {

 
String serial_message = Serial.readString();//1000y2000 xteps = 1000, ysteps = 2000
Serial.print(serial_message);
char* str;
char* ptr;

strcpy (str, serial_message.c_str());
strtok_r (str, "y", &ptr);

printf("'%s'  '%s'\n", str, ptr);

int x_Steps = atoi(str);
int y_Steps = atoi(ptr);

Serial.print(str);
Serial.print(ptr);



/*Serial.print(x + 1);


   for(int x = 0; x < 200; x++) {
    digitalWrite(Xpinstep,HIGH); 
    digitalWrite(Ypinstep,HIGH); 
    delayMicroseconds(500); 
    digitalWrite(Xpinstep,LOW); 
    digitalWrite(Ypinstep,LOW); 
    delayMicroseconds(500); */
  }
}
