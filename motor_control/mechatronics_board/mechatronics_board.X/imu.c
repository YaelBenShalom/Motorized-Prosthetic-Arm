#include <math.h>

#include "imu.h" 
#include "i2c_master_noint.h"
#include "ST7789.h"
#include "UART.h"

void imu_setup(){
    unsigned char who = 0;
    //read from IMU_WHOAMI
    
    who = readPin(IMU_ADDR,IMU_WHOAMI,1);
    
    if (who != 0b01101001) { //will stay in while loop if I2C bus isn't working
        while(1){
            LATAINV = 0b10000; //toggle pin A4
            _CP0_SET_COUNT(0);
            while(_CP0_GET_COUNT() < 0.5 * 24000000) {;} //delay half a second
        }
    }

    // init IMU_CTRL1_XL
    // Set the sample rate to 1.66 kHz, with 2g sensitivity, and 100 Hz filter.
    writePin(IMU_ADDR, IMU_CTRL1_XL, 0b10000010); //1000 => 1.66kHz, 00 => +/- 2g sensitivity, 10 => 100 Hz)
        
    // init IMU_CTRL2_G
    // Set the sample rate to 1.66 kHz, with 1000 dps sensitivity (not full scale)
    writePin(IMU_ADDR, IMU_CTRL2_G, 0b10001000);

    // init IMU_CTRL3_C (contol register, contains IF_INC,
    //if =1 reads out sequentially)
    writePin(IMU_ADDR, IMU_CTRL3_C, 0b00000100);   
}

void bar_x(signed short xaccel){
    int i; int j;
        
    float x = (xaccel / 16383.0) * 100;
    
    for (i=0; i<100; i++){ //go across 100 pixels
        for (j=0; j<10; j++){ //width of bar
            if (x < 0){ //screen is tilting left, -i
                if ( i> fabs(x)){ //if magnitude of x is bigger than index
                    LCD_drawPixel(120-i, 120+j, BLACK);
                }
                else {
                    LCD_drawPixel(120-i, 120+j, WHITE);
                }
            }
            else { //screen tilt right, +i
                if ( i> fabs(x)){ //if magnitude of x is bigger than index
                    LCD_drawPixel(120+i, 120+j, BLACK);
                }
                else {
                    LCD_drawPixel(120+i, 120+j, WHITE);
                }
            }
        }
    }
}

void bar_y(signed short yaccel){
    int i; int j;
    
    float y = (yaccel / 16383.0) * 100;
    
    for (i=0; i<100; i++){ //go across 100 pixels
        for (j=0; j<10; j++){ //width of bar
            if (y > 0){ //screen is tilting away from user, -i
                if ( i> fabs(y)){ //if magnitude of y is bigger than index
                    LCD_drawPixel(120+j, 120-i, BLACK);
                }
                else {
                    LCD_drawPixel(120+j, 120-i, GREEN);
                }
            }
            else { //screen tilt toward, +i
                if ( i> fabs(y)){ //if magnitude of y is bigger than index
                    LCD_drawPixel(120+j, 120+i, BLACK);
                }
                else {
                    LCD_drawPixel(120+j, 120+i, GREEN);
                }
            }
        }
    }
}