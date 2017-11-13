/*
_18_element_cube_test.ino is the code that runs on the arduino when you run an experiment. 
It is set up to work for 18 elements. This needs the calibration information as well as the desired 
phases and amplitude weights in order to set the vector modulators correctly.
*/

#include <math.h>



// if beamsteer = true --> use the x, y, and z positions to calculate the phases; otherwise, use the manual phases
// A boolean holds one of two values, true or false. (Each boolean variable occupies one byte of memory) ex. boolean running = false;
bool beamsteer = false;

// if uniform gain = true --> set all gain equal to 1; otherwise as the gain[] values
bool uniform_gain = true;

// Double precision floating point number. On the Uno and other ATMEGA based boards, this occupies 4 bytes
double Phi0 = 0;

double Theta0 = 90;

double uniGain = 1.0;

const int numElements = 16;

const double pi = 3.14159265;

double Phi0r = Phi0*(pi/180);

double Theta0r = Theta0*(pi/180);

// the pin that the LED is attached to
const int ledPin = 13;

// a variable to read incoming serial data into
int incomingByte;

const int _sck = 4;

const int _sdi = 5;

// board layer 1 activate, each other layer must have a jumper from the pin to pin 10 to create multi layered board
const int ctl = 10;

const int ldac = 9;

const int clearpin = 8;

// board layer 5 activate
const int ctl5 = 12;

// board layer 4 activate
const int ctl4 = 11;

// board layer 2 activate
const int ctl2 = 7;

// board layer 3 activate
const int ctl3 = 6;

// I voltage calibration factor, multiply this factor can make DAQ more precise
const double IVscale[] = {13140.0, 13085.0, 13095.0, 13122.0, 13140.0, 13155.0,
                          13155.0, 13095.0, 13125.0, 13060.0, 13060.0, 13095.0,
                          13080.0, 13095.0, 13115.0, 13065.0, 13115.0, 13060.0};

// Q voltage calibration factor                        
const double QVscale[] = {13110.0, 13105.0, 13110.0, 13120.0, 13140.0, 13170.0,
                          13135.0, 13140.0, 13120.0, 13100.0, 13080.0, 13115.0,
                          13065.0, 13150.0, 13100.0, 13120.0, 13110.0, 13035.0};

double testVi[] = {0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3,
                   1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2};

double testVq[] = {0.55, 0.65, 0.75, 0.85, 0.95, 1.05, 1.15, 1.25, 1.35,
                   1.45, 1.55, 1.65, 1.75, 1.85, 1.95, 2.05, 2.15, 2.25};

// manually set up the gain, range 0 to 1, 0.707 = half power
double gain[] = {
1,  // element 1
1,  // element 2
1,  // element 3
1,  // element 4
1,  // element 5
1,  // element 6
1,  // element 7
1,  // element 8
1,  // element 9
1,  // element 10
1,  // element 11
1,  // element 12
1,  // element 13
1,  // element 14
1,  // element 15
1,  // element 16
};

// if beamsteer = false, then use the manually type in phases
/*
double phase[] = {
318.24-5.346, //1
146.88+1.579, //2
19.44-94.0062, //3
90.72-88.3599, //4
61.92-96.056, //5
343.44-6.1101, //6
162.72+7.8165, //7
25.92+1.949, //8
199.44-86.1602, //9
300.24+6.9431, //10
187.2-85.2954, //11
182.16-1.748, //12
352.8-98.1325, //13
112.32-87.9425, //14
92.16-95.2064, //15
346.32+5.5433, //16
};              
*/

#ifndef TYPEDEF_H
#define TYPEDEF_H

//packet_t is a data structure for passing the phases calculated in Python to the Arduino via serial connection
typedef struct packet_ {
  double phases[numElements];
} packet_t;

#endif
packet_t packet;



// just replace first term in phase offset
// second term for calibrating phase -- everyone starts at the same time


// VNA calibration with both DC block connectors
// VCC @ 8.05 V, GND @ DAQ
// It's the data @ 2.4GHz

// element                             1             2              3               4              5              6             7              8              9             10               11             12             13             14          15             16
double Vmi[] =             {         1.46,         1.46,          1.45,           1.47,          1.45,          1.45,         1.46,          1.48,          1.47,          1.46,            1.49,          1.47,          1.47,          1.45,       1.46,          1.47};
double Vmq[] =             {         1.45,         1.46,          1.46,           1.45,          1.46,          1.46,         1.46,          1.46,          1.47,          1.46,            1.47,          1.46,          1.46,          1.47,       1.45,          1.46};
double Vr[] =              {         1.90,         1.92,          1.90,           1.90,          1.90,          1.90,         1.92,          1.92,          1.94,          1.92,            1.94,          1.92,          1.92,          1.90,       1.90,          1.92};
double Gnull_dB[] =        {      -55.480,      -54.343,       -56.976,        -52.850,       -54.699,       -56.011,      -57.106,       -49.735,       -56.154,       -55.487,         -61.361,       -55.503,       -61.215,       -52.553,    -56.349,       -53.912};
double Gmax[] =            {        0.540,        0.565,         0.541,          0.559,         0.561,         0.546,        0.535,         0.541,         0.572,         0.560,           0.525,         0.537,         0.526,         0.558,      0.563,         0.578};
double phase_offset[] =    {   -26.833+75, -32.129+91.4,   -3.042+45.2,     -11.034+29,  -26.790+89.8,   -33.289+90.4,  4.723+28.5,  -28.639+76.8,   -2.823+27.8,     -0.759+46.6,  -27.994+72.9,   -6.070+43.2,  -28.369+75.8,   -0.453+43.3,  -24.228+75,     5.186+26};





             
double xcoords[] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

double ycoords[] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

double zcoords[] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
               

void setup() {
   // initialize serial communication:
   Serial.begin(115200);
 
   pinMode(ctl, OUTPUT);
   
   pinMode(_sck, OUTPUT);
   
   pinMode(_sdi, OUTPUT);
   
   pinMode(ldac,OUTPUT);
   
   pinMode(clearpin, OUTPUT);
   
   pinMode(ctl2, OUTPUT);
   
   pinMode(ctl3, OUTPUT);
   
   pinMode(ctl4, OUTPUT);
   
   pinMode(ctl5, OUTPUT);
  
   digitalWrite(clearpin, HIGH);
   
   digitalWrite(ctl,HIGH);
   
   digitalWrite(ctl2,HIGH);
   
   digitalWrite(ctl3, HIGH);
   
   digitalWrite(ctl4, HIGH);
   
   digitalWrite(ctl5, HIGH);
  
   digitalWrite(_sck,HIGH);
   
   digitalWrite(ldac,HIGH);

   delay(3000);





   // if you calculate the phases by other program, you can skip this part
   if(beamsteer == true){
      double max_phase = 0; //phase[0];
      for(int i = 0; i < numElements; i++){
         
         phase[i] = 360*(xcoords[i]*cos(Phi0r)*sin(Theta0r) + ycoords[i]*sin(Theta0r)*sin(Phi0r) + zcoords[i]*cos(Theta0r));
         if(phase[i] > max_phase){
            max_phase = phase[i];
         }
      }
      for(int i = 0; i < numElements; i++){
         phase[i] = fmod(max_phase - phase[i],360);
         Serial.print(i+1);Serial.print('\t');Serial.println(phase[i],4);
      } 
   }


 
   if(uniform_gain == true){
      for(int i = 0; i < numElements; i++){
         gain[i] = uniGain;
      }
   }



   // The loss at the null point (I = Vmi, Q = Vmq) corresponds to Gnull = Gmin
   double Gnull[numElements];
                            
   for(int i = 0; i<numElements; i++){                          
      Gnull[i] = pow(10,Gnull_dB[i]/20);   
   }
  
   normalizeGain();
 
   for(int i=0; i<numElements; i++){
      int volt = getvoltage(i);
   }
}



//constantly loop and update phases for beamsteering
void loop(){
  char buf[numElements*4];
    int numChar = Serial.readBytes(buf, numElements*4);

    //Serial.println(int(buf));
    
    if (numChar != 0){
      memset(&packet, 0, sizeof(packet));

      for (int i=0; i<numElements; ++i) {
        memcpy(&packet.phases[i], &(buf[i*4]), 4);
      }
      
      double phase[numElements] = packet.phases;
      
      /* troubleshooting
      for (int i=0; i<32; ++i) {
        Serial.println(packet.phases[i],HEX);
      }
      */
    }
    
    //delay(100);
}



void writeLayer(int layer,int high, int low){
   digitalWrite(layer,LOW);
   shiftOut(_sdi, _sck, MSBFIRST, (high>>8));
   shiftOut(_sdi, _sck, MSBFIRST, high);
   shiftOut(_sdi, _sck, MSBFIRST, (low>>8));
   shiftOut(_sdi, _sck, MSBFIRST, low);
   digitalWrite(layer,HIGH);
   digitalWrite(ldac,LOW);
   digitalWrite(ldac,HIGH);
}



int getvoltage(int i){
  
  double corrected_phase = fmod((phase[i] - phase_offset[i]+360),360)-180;
  
  Serial.println(i+1);   
  Serial.print("Mag: ");Serial.print(gain[i],5); 
  Serial.print("\tPhase: ");Serial.println(phase[i]);
  
  if(corrected_phase == 90 || corrected_phase == -90){
   corrected_phase -= 0.001;
  } 
  
  double a = tan(corrected_phase*pi/180);
    
  double Iset = (gain[i]*Vr[i]/(2*Gmax[i]*sqrt(pow(a,2)+1)))+Vmi[i];
     
  double Qset = (gain[i]*Vr[i]*a/(2*Gmax[i]*sqrt(pow(a,2)+1)))+Vmq[i];
     
  if(corrected_phase > 90.0 || corrected_phase < -90){
    Iset = -Iset + 2*Vmi[i];
    Qset = -Qset + 2*Vmq[i];
  }
     
  Serial.print("\tIset= ");Serial.print(Iset,3);Serial.print("\tQset= ");Serial.println(Qset,3);
 
unsigned int Ihighword = 0;
unsigned int Ilowword = 0;
unsigned int Iconverted = 0;

unsigned int Qhighword = 0;
unsigned int Qlowword = 0;
unsigned int Qconverted = 0;

/************************************
 MANUAL VOLTAGE OVERRIDE:
 ************************************/
 //Iset = testVi[i];
 //Qset = testVq[i];

 // temp /= 2.5; //gain associated on board
 // temp /= 0.001; //how many millivolts
 // temp /= 4980.0; //supply voltage
 // temp *= intMax;  //normailze to 16 bit i.e. 65535
 
 double Iscaled =  Iset*IVscale[i];//5375.0; // DAC Word / Voltage (LSB/volt) from Nick
 Iconverted = (int) Iscaled;
 Ihighword = Iconverted >> 12; //the command bytes require that the LSB of the highword have value
 Ilowword = Iconverted << 4; //rest of value to be written to register...
 
 double Qscaled =  Qset*QVscale[i];//5375.0; // DAC Word / Voltage (LSB/volt) from Nick
 Qconverted = (int) Qscaled;
 Qhighword = Qconverted >> 12; //the command bytes require that the LSB of the highword have value
 Qlowword = Qconverted << 4; //rest of value to be written to register...
 
 int antennaNum = i;
 
 if( (0 <= antennaNum) && (antennaNum <= 3)){
   Ihighword += 0x0300 + (2*antennaNum)*16;
   Qhighword += 0x0300 + (2*antennaNum+1)*16;
   Serial.println("C1");
   writeLayer(ctl,Ihighword,Ilowword);
   writeLayer(ctl,Qhighword,Qlowword);
 }else if( (4 <= antennaNum) && (antennaNum <= 7)){
   antennaNum -= 4;
   Ihighword += 0x0300 + (2*antennaNum)*16;
   Qhighword += 0x0300 + (2*antennaNum+1)*16;
   Serial.println("C2");
   writeLayer(ctl2,Ihighword,Ilowword);
   writeLayer(ctl2,Qhighword,Qlowword);
 }else if( (8 <= antennaNum) && (antennaNum <= 11)){
   antennaNum -= 8;
   Ihighword += 0x0300 + (2*antennaNum)*16;
   Qhighword += 0x0300 + (2*antennaNum+1)*16;
   Serial.println("C3");
   writeLayer(ctl3,Ihighword,Ilowword);
   writeLayer(ctl3,Qhighword,Qlowword);
 }else if( (12 <= antennaNum) && (antennaNum <= 15)){
   antennaNum -= 12;
   Ihighword += 0x0300 + (2*antennaNum)*16;
   Qhighword += 0x0300 + (2*antennaNum+1)*16;
   Serial.println("C4");
   writeLayer(ctl4,Ihighword,Ilowword);
   writeLayer(ctl4,Qhighword,Qlowword);
 }else if( (16 <= antennaNum) && (antennaNum <= 17)){
   antennaNum -= 16;
   Ihighword += 0x0300 + (4*antennaNum+1)*16;
   Qhighword += 0x0300 + (4*antennaNum+3)*16;
   Serial.println("C5");
   writeLayer(ctl5,Ihighword,Ilowword);
   writeLayer(ctl5,Qhighword,Qlowword);
 }
 Serial.print(Iset);Serial.print("\t");Serial.print(Ihighword,HEX);Serial.print("\t");Serial.println(Ilowword,HEX);
 return (int) Iset;

}

double minArray(double array[]){
  double minimum = array[0];
  
  for(int i=0;i<numElements;i++){
   if(array[i] < minimum){
     minimum = array[i];
   }
  }  
  return(minimum);
}

double maxArray(double array[]){
  double maximum = array[0];
  
  for(int i=0;i<numElements;i++){
   if(array[i] > maximum){
     maximum = array[i];
   }
  }  
  return(maximum);
}

void normalizeGain(){
  double scale = minArray(Gmax);
  
  for(int i=0;i<numElements;i++){
    gain[i] = gain[i]*scale;
    //Serial.println(gain[i], 5);
  }
}
