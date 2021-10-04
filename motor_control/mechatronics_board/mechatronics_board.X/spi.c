#include "spi.h"
#include <xc.h>

// initialize SPI1
void initSPI() {
// Turn of analog functionality of A and B pins
    ANSELA = 0;
    ANSELB = 0;
    
    // Pin B14 has to be SCK1 -> SCL
    
    // set SDO1 - B13 -> SDA 

    TRISBbits.TRISB13 = 0;
    LATBbits.LATB13 = 1;
    RPB13Rbits.RPB13R = 0b0011;
    // set B15 -> RES (reset), initialize to High

    TRISBbits.TRISB15 = 0; //B15 is output
    LATBbits.LATB15 = 1; //B15 is high
    // set B12 -> DC (data control), initialize Low

    TRISBbits.TRISB12 = 0; //B12 is output
    LATBbits.LATB12 = 0; //B12 is low

    // setup SPI1
    SPI1CON = 0; // turn off the spi module and reset it
    SPI1BUF; // clear the rx buffer by reading from it
    SPI1BRG = 1; // baud rate to 10 MHz [SPI1BRG = (48000000/(2*desired))-1]
    SPI1STATbits.SPIROV = 0; // clear the overflow bit
    SPI1CONbits.CKP = 1; // clock idle high **This is specific to ST77898**
    SPI1CONbits.CKE = 1; // data changes when clock goes from logic hi to lo 
    SPI1CONbits.MSTEN = 1; // master operation
    SPI1CONbits.ON = 1; // turn on spi 
    
    // blink the reset pin to reset the display
    LATBbits.LATB15 = 0;
    _CP0_SET_COUNT(0);
    while(_CP0_GET_COUNT()<24000000/1000){} // 1ms
    LATBbits.LATB15 = 1;
}

// send a byte via spi and return the response
unsigned char spi_io(unsigned char o) {
  SPI1BUF = o;
  while(!SPI1STATbits.SPIRBF) { // wait to receive the byte
    ;
  }
  return SPI1BUF;
}