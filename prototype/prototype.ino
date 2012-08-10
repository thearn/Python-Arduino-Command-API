#include <SoftwareSerial.h>
#include <Wire.h>
#include <Servo.h>

SoftwareSerial *sserial = NULL;
Servo servos[8];
int servo_pins[] = {0, 0, 0, 0, 0, 0, 0, 0};
boolean connected = false;

int Str2int (String Str_value)
{
  char buffer[10]; //max length is three units
  Str_value.toCharArray(buffer, 10);
  int int_value = atoi(buffer);
  return int_value;
}

void split(String results[], int len, String input, char spChar) {
  String temp = input;
  for (int i=0; i<len; i++) {
    int idx = temp.indexOf(spChar);
    results[i] = temp.substring(0,idx);
    temp = temp.substring(idx+1);
  }
}

void DigitalHandler(int mode, String data){
      int pin = Str2int(data);
    if(mode<=0){ //read
        Serial.println(digitalRead(pin));
    }else{
        if(pin <0){
            digitalWrite(-pin,LOW);
        }else{
            digitalWrite(pin,HIGH);
        }
        //Serial.println('0');
    }
}

void AnalogHandler(int mode, String data){
     if(mode<=0){ //read
        int pin = Str2int(data);
        Serial.println(analogRead(pin));
    }else{
        String sdata[2];
        split(sdata,2,data,'%');
        int pin = Str2int(sdata[0]);
        int pv = Str2int(sdata[1]);
        analogWrite(pin,pv);
    }
}

void ConfigurePinHandler(String data){
    int pin = Str2int(data);
    if(pin <=0){
        pinMode(-pin,INPUT);
    }else{
        pinMode(pin,OUTPUT);
    }
}

void SS_set(String data){
  delete sserial;
  String sdata[3];
  split(sdata,3,data,'%');
  int rx_ = Str2int(sdata[0]);
  int tx_ = Str2int(sdata[1]);
  int baud_ = Str2int(sdata[2]);
  sserial = new SoftwareSerial(rx_, tx_);
  sserial->begin(baud_);
  Serial.println("ss OK");
}

void SS_write(String data) {
 int len = data.length()+1;
 char buffer[len];
 data.toCharArray(buffer,len);
 Serial.println("ss OK");
 sserial->write(buffer); 
}
void SS_read(String data) {
 char c = sserial->read(); 
 Serial.println(c);
}

void pulseInHandler(String data){
    int pin = Str2int(data);
    long duration;
    if(pin <=0){
          pinMode(-pin, INPUT);
          duration = pulseIn(-pin, LOW);      
    }else{
          pinMode(pin, INPUT);
          duration = pulseIn(pin, HIGH);      
    }
    Serial.println(duration);
}

void pulseInSHandler(String data){
    int pin = Str2int(data);
    long duration;
    if(pin <=0){
          pinMode(-pin, OUTPUT);
          digitalWrite(-pin, HIGH);
          delayMicroseconds(2);
          digitalWrite(-pin, LOW);
          delayMicroseconds(5);
          digitalWrite(-pin, HIGH);
          pinMode(-pin, INPUT);
          duration = pulseIn(-pin, LOW);      
    }else{
          pinMode(pin, OUTPUT);
          digitalWrite(pin, LOW);
          delayMicroseconds(2);
          digitalWrite(pin, HIGH);
          delayMicroseconds(5);
          digitalWrite(pin, LOW);
          pinMode(pin, INPUT);
          duration = pulseIn(pin, HIGH);      
    }
    Serial.println(duration);
}

void SV_add(String data) {
    String sdata[3];
    split(sdata,3,data,'%');
    int pin = Str2int(sdata[0]);
    int min = Str2int(sdata[1]);
    int max = Str2int(sdata[2]);
    int pos = -1;
    for (int i = 0; i<8;i++) {
        if (servo_pins[i] == pin) { //reset in place
            servos[pos].detach();
            servos[pos].attach(pin, min, max);
            servo_pins[pos] = pin;
            Serial.println(pos);
            return;
            }
        }
    for (int i = 0; i<8;i++) {
        if (servo_pins[i] == 0) {pos = i;break;} // find spot in servo array
        }
    if (pos == -1) {;} //no array position available!
    else {
        servos[pos].attach(pin, min, max);
        servo_pins[pos] = pin;
        Serial.println(pos);
        }
}

void SV_remove(String data) {
    int pos = Str2int(data);
    servos[pos].detach();
    servo_pins[pos] = 0;
}

void SV_read(String data) {
    int pos = Str2int(data);
    int angle;
    angle = servos[pos].read();
    Serial.println(angle);
}

void SV_write(String data) {
    String sdata[2];
    split(sdata,2,data,'%');
    int pos = Str2int(sdata[0]);
    int angle = Str2int(sdata[1]);
    servos[pos].write(angle);
}

void SV_write_ms(String data) {
    String sdata[2];
    split(sdata,2,data,'%');
    int pos = Str2int(sdata[0]);
    int uS = Str2int(sdata[1]);
    servos[pos].writeMicroseconds(uS);
}


void SerialParser(void) {
  char readChar[64];
  Serial.readBytesUntil(33,readChar,64);
  String read_ = String(readChar);
  //Serial.println(readChar);
  int idx1 = read_.indexOf('%');
  int idx2 = read_.indexOf('$');
  // separate command from associated data
  String cmd = read_.substring(1,idx1);
  String data = read_.substring(idx1+1,idx2);
  
  // determine command sent
  if (cmd == "dw") {
      DigitalHandler(1, data);   
  }
  else if (cmd == "dr") {
      DigitalHandler(0, data);   
  }  
  else if (cmd == "aw") {
      AnalogHandler(1, data);   
  }    
  else if (cmd == "ar") {
      AnalogHandler(0, data);   
  }      
  else if (cmd == "pm") {
      ConfigurePinHandler(data);   
  }    
  else if (cmd == "ps") {
      pulseInSHandler(data);   
  }    
  else if (cmd == "pi") {
      pulseInHandler(data);   
  }        
  else if (cmd == "ss") {
      SS_set(data);   
  }
  else if (cmd == "sw") {
      SS_write(data);   
  }
  else if (cmd == "sr") {
      SS_read(data);   
  }    
  else if (cmd == "sva") {
      SV_add(data);   
  }      
  else if (cmd == "svr") {
      SV_read(data);   
  }   
 else if (cmd == "svw") {
      SV_write(data);   
  }    
 else if (cmd == "svwm") {
      SV_write_ms(data);   
  }      
  else if (cmd == "svd") {
      SV_remove(data);   
  }       
}


void setup()  {
  Serial.begin(9600); 
    while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
}

void loop() {
   SerialParser();
   }
