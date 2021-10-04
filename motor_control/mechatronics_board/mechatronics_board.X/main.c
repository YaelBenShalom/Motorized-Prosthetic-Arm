#include<xc.h>           // processor SFR definitions
#include<sys/attribs.h>  // __ISR macro
#include<stdio.h>
#include "i2c_master_noint.h"
#include "UART.h"
#include "spi.h"
#include "font.h"
#include "ST7789.h"
#include "imu.h"
#include "ws2812b.h"

// DEVCFG0
#pragma config DEBUG = OFF      // disable debugging
#pragma config JTAGEN = OFF     // disable jtag
#pragma config ICESEL = ICS_PGx1 // use PGED1 and PGEC1
#pragma config PWP = OFF        // disable flash write protect
#pragma config BWP = OFF        // disable boot write protect
#pragma config CP = OFF         // disable code protect

// DEVCFG1
#pragma config FNOSC = FRCPLL   // use internal pll
#pragma config FSOSCEN = OFF    // disable secondary oscillator
#pragma config IESO = OFF       // disable switching clocks
#pragma config POSCMOD = OFF    // RC mode
#pragma config OSCIOFNC = OFF   // disable clock output
#pragma config FPBDIV = DIV_1   // divide sysclk freq by 1 for peripheral bus clock
#pragma config FCKSM = CSDCMD   // disable clock switch and FSCM
#pragma config WDTPS = PS1048576 // use largest wdt
#pragma config WINDIS = OFF     // use non-window mode wdt
#pragma config FWDTEN = OFF     // wdt disabled
#pragma config FWDTWINSZ = WINSZ_25 // wdt window at 25%

// DEVCFG2 - get the sysclk clock to 48MHz from the 8MHz crystal
#pragma config FPLLIDIV = DIV_2 // divide input clock to be in range 4-5MHz
#pragma config FPLLMUL = MUL_24 // multiply clock after FPLLIDIV
#pragma config FPLLODIV = DIV_2 // divide clock after FPLLMUL to get 48MHz

// DEVCFG3
#pragma config USERID = 0       // some 16bit userid, doesn't matter what
#pragma config PMDL1WAY = OFF   // allow multiple reconfigurations
#pragma config IOL1WAY = OFF    // allow multiple reconfigurations

int main() {
    __builtin_disable_interrupts(); // disable interrupts while initializing things

    // set the CP0 CONFIG register to indicate that kseg0 is cacheable (0x3)
    __builtin_mtc0(_CP0_CONFIG, _CP0_CONFIG_SELECT, 0xa4210583);

    // 0 data RAM access wait states
    BMXCONbits.BMXWSDRM = 0x0;

    // enable multi vector interrupts
    INTCONbits.MVEC = 0x1;

    // disable JTAG to get pins back
    DDPCONbits.JTAGEN = 0;
    
    // do your TRIS and LAT commands here
    TRISBbits.TRISB4 = 1;   //B4 is input
    TRISAbits.TRISA4 = 0;   //A4 is output
    LATAbits.LATA4 = 0;     //A4 is low
    
    initUART1();            // init UART1
    initSPI();              // init SPI
    LCD_init();             // init LCD
    LCD_clearScreen(BLACK); //clear screen
    
    i2c_master_setup();     // init i2c
    imu_setup();            // setup IMU
        
    __builtin_enable_interrupts();
    
    signed short data_arr[7];
    int delay;
    while(1) {
        _CP0_SET_COUNT(0);
        LATAbits.LATA4 = !LATAbits.LATA4; //heartbeat
        
        i2c_read_multiple(IMU_ADDR, IMU_OUT_TEMP_L, data_arr, 14);
        
        sprintf(m, "Temperature: %d", data_arr[0]);
        drawString(10, 10, WHITE, m);
        
        sprintf(m, "Angular V: %d %d %d", data_arr[1], data_arr[2], data_arr[3]);
        drawString(10, 20, WHITE, m);
        
        sprintf(m, "Acceleration: %d %d %d", data_arr[4], data_arr[5], data_arr[6]);
        drawString(10, 30, WHITE, m);
        
        bar_x(-data_arr[5]);
        bar_y(data_arr[4]);
        
        delay = _CP0_GET_COUNT();       //remember time
        float fps = 24000000/delay;     //get fps from delay (48M ticks/1 sec * frame/tick)
        sprintf(m, "FPS = %.2f", fps);
        drawString(10, 220, WHITE, m);  //write FPS on screen
    }
}