#include <Servo.h>

Servo myservo;
const byte motor = ; //pin that motor is connected to
const byte servo = ; //pin servo is connected to
const byte potentiometer = //pin speed adjustment is connected to
int speed; // based off potentiometer values
int serialValue;
int firingTime = ; //Time balls are fired | will fine tune to figure out how many balls per int
int positionpv;// Used to calculate position of rotating motor
int positionsv;//
const byte forward = ; //pin forward motor rotator is connected to
const byte backward = ; //pin backward motor rotator is connected to
//set proper pin values and begin serial
void setup(){
    Serial.begin(9600);
    //set up pins
    pinMode()
    pinMode()
}

void loop(){
  //set speed
  speed = ;
  Serial.print(speed);
  serialValue = Serial.read();
  //motor turns on
  if(serialValue == 1){
      analogWrite(motor,speed);
      loadBall();
      digitalWrite(motor,LOW);
  }
  //motor turns off
  if(serialValue == 0){
      digitalWrite(motor,LOW);
  }
}

void loadBall(){
  servo.attatch(servo);
  //main firing mehanicsm code
  for(int i = 0; i<= firingTime;i++){
      servo.write(i);
      delay(); // time inbetween balls
  }
  //feed ball into mechanism
  for(int i = firingTime; i >= 0;i--){
      servo.write(i);
      delay(); //time inbetween balls
      servo.detatch(); // detach servo

  }
}

//Skeleton code for motor position change will depend on specifics of what motor we use
void changePosition(){
    positionpv = ; // set pos values
    positionsv = ; 
    if(positionpv - positionsv < 0){
        digitalWrite(forward, 1);// forward rotation
        digitalWrite(backward, 0); // stop backward rotation
    }
    else{
        if(positionpv - positionsv > 0){
            digitalWrite(forward, 0 ); //stop forward rotation
            digitalWrite(backward, 1); //backward rotation
        }
        //position is 0, stop motor
        else{
            digitalWrite(forward,0);
            digitalWrite(backward,0);
        }
    }
}
