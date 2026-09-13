const int IN1_L = 2;
const int IN2_L = 3;
const int IN3_L = 4;
const int IN4_L = 5;
const int ENA_L = 9;
const int ENB_L = 10;
const int IN1_R = 7;
const int IN2_R = 8;
const int IN3_R = 12;
const int IN4_R = 13;
const int ENA_R = 6;
const int ENB_R = 11;
const int JOY_X = A0 ;
const int JOY_Y = A1 ;
bool voiceMode = false ;
char voiceCommand ;
const int speed = 50;
void moveForward () {
45 digitalWrite ( IN1_L , HIGH ) ; digitalWrite ( IN2_L , LOW ) ;
digitalWrite ( IN3_L , HIGH ) ; digitalWrite ( IN4_L , LOW ) ;
digitalWrite ( IN1_R , HIGH ) ; digitalWrite ( IN2_R , LOW ) ;
digitalWrite ( IN3_R , HIGH ) ; digitalWrite ( IN4_R , LOW ) ;
analogWrite ( ENA_L , speed ) ; analogWrite ( ENB_L , speed ) ;
analogWrite ( ENA_R , speed ) ; analogWrite ( ENB_R , speed ) ;
}
// ... other functions ( moveBackward , turnLeft , turnRight ,
stopMotors ) go here ...
void setup () {
pinMode ( IN1_L , OUTPUT ) ; pinMode ( IN2_L , OUTPUT ) ;
pinMode ( IN3_L , OUTPUT ) ; pinMode ( IN4_L , OUTPUT ) ;
pinMode ( ENA_L , OUTPUT ) ; pinMode ( ENB_L , OUTPUT ) ;
pinMode ( IN1_R , OUTPUT ) ; pinMode ( IN2_R , OUTPUT ) ;
pinMode ( IN3_R , OUTPUT ) ; pinMode ( IN4_R , OUTPUT ) ;
pinMode ( ENA_R , OUTPUT ) ; pinMode ( ENB_R , OUTPUT ) ;
Serial . begin (9600) ;
stopMotors () ;
}
void loop () {
if ( Serial . available () > 0) {
voiceCommand = Serial . read () ;
if ( voiceCommand == ’F’) { voiceMode = true ; moveForward () ;
}
else if ( voiceCommand == ’B’) { voiceMode = true ;
moveBackward () ; }
else if ( voiceCommand == ’L’) { voiceMode = true ; turnLeft
() ; }
else if ( voiceCommand == ’R’) { voiceMode = true ; turnRight
() ; }
else if ( voiceCommand == ’S’) { stopMotors () ; voiceMode =
false ; }
}
if (! voiceMode ) {
int xVal = analogRead ( JOY_X ) ;
int yVal = analogRead ( JOY_Y ) ;
46 if ( yVal > 600) moveForward () ;
else if ( yVal < 400) moveBackward () ;
else if ( xVal < 400) turnLeft () ;
else if ( xVal > 600) turnRight () ;
else stopMotors () ;
}
}
