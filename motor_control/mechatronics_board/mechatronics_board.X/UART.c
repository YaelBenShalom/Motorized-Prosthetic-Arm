#include "UART.h"

// Read from UART1
// block other functions until you get a '\r' or '\n'
// send the pointer to your char array and the number of elements in the array
void readUART1(char * message, int maxLength) {
    char data = 0;
    int complete = 0, num_bytes = 0;
    // loop until you get a '\r' or '\n'
    while (!complete) {
        if (U1STAbits.URXDA) { // if data is available
            data = U1RXREG;      // read the data
            if ((data == '\n') || (data == '\r')) {
                complete = 1;
            } else {
                message[num_bytes] = data;
                ++num_bytes;
                // roll over if the array is too small
                if (num_bytes >= maxLength) {
                    num_bytes = 0;
                }
            }
        }
    }
    // end the string
    message[num_bytes] = '\0';
}

// Write a character array using UART3
void writeUART1(const char * string) {
    while (*string != '\0') {
        while (U1STAbits.UTXBF) {;} // wait until tx buffer isn't full
        U1TXREG = *string;
        ++string;
    }
}

void initUART1(){
    U1RXRbits.U1RXR = 0b0001; // U1RX is B6
    RPB7Rbits.RPB7R = 0b0001; // U1TX is B7
    
    // turn on UART3 without an interrupt
    U1MODEbits.BRGH = 0; // set baud to NU32_DESIRED_BAUD
    U1BRG = ((48000000 / 115200) / 16) - 1;

    // 8 bit, no parity bit, and 1 stop bit (8N1 setup)
    U1MODEbits.PDSEL = 0;
    U1MODEbits.STSEL = 0;

    // configure TX & RX pins as output & input pins
    U1STAbits.UTXEN = 1;
    U1STAbits.URXEN = 1;

    // enable the UART1
    U1MODEbits.ON = 1;
}