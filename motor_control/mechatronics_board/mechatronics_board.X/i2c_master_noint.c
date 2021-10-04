#include "i2c_master_noint.h"
#include "UART.h"

// I2C Master utilities, using polling rather than interrupts
// The functions must be called in the correct order as per the I2C protocol
// I2C pins need pull-up resistors, 2k-10k

void i2c_master_setup(void) {
    // using a large BRG to see it on the nScope, make it smaller after verifying that code works
    // look up TPGD in the datasheet
    I2C1BRG = 1000; // I2CBRG = [1/(2*Fsck) - TPGD]*Pblck - 2 (TPGD is the Pulse Gobbler Delay) 
    //make 400kHz later on ^
    ANSELA = 0;
    ANSELB = 0;
    I2C1CONbits.ON = 1; // turn on the I2C1 module
}

void i2c_master_start(void) {
    I2C1CONbits.SEN = 1; // send the start bit
    while (I2C1CONbits.SEN) {
        ;
    } // wait for the start bit to be sent
}

void i2c_master_restart(void) {
    I2C1CONbits.RSEN = 1; // send a restart 
    while (I2C1CONbits.RSEN) {;} // wait for the restart to clear
}

void i2c_master_send(unsigned char byte) { // send a byte to slave
    I2C1TRN = byte; // if an address, bit 0 = 0 for write, 1 for read
    while (I2C1STATbits.TRSTAT) {
        ;
    } // wait for the transmission to finish
    if (I2C1STATbits.ACKSTAT) { // if this is high, slave has not acknowledged
        // ("I2C1 Master: failed to receive ACK\r\n");
        while(1){   // get stuck here if the chip does not ACK back
            LATASET = 0x10; //turn A4 on
        } 
    }
}

unsigned char i2c_master_recv(void) { // receive a byte from the slave
    I2C1CONbits.RCEN = 1; // start receiving data
    while (!I2C1STATbits.RBF) {;} // wait to receive the data
    return I2C1RCV; // read and return the data
}

void i2c_master_ack(int val) { // sends ACK = 0 (slave should send another byte)
    // or NACK = 1 (no more bytes requested from slave)
    I2C1CONbits.ACKDT = val; // store ACK/NACK in ACKDT
    I2C1CONbits.ACKEN = 1; // send ACKDT
    while (I2C1CONbits.ACKEN) {;} // wait for ACK/NACK to be sent
}

void i2c_master_stop(void) { // send a STOP:
    I2C1CONbits.PEN = 1; // comm is complete and master relinquishes bus
    while (I2C1CONbits.PEN) {;} // wait for STOP to complete
}

void writePin(unsigned char address, unsigned char reg, unsigned char value) {
    i2c_master_start();
    i2c_master_send(address);  //send address + write bit
    i2c_master_send(reg);  //send command register address
    i2c_master_send(value);  //send value
    i2c_master_stop();
}

unsigned char readPin(unsigned char address, unsigned char reg, int ack) {
    unsigned char value;
    i2c_master_start();
    
    i2c_master_send(address);  //send address + read bits
    i2c_master_send(reg);  //send command register address
    i2c_master_restart();   //send a restart
    
    i2c_master_send(address | 0b1); //send read bit by making last digit 1
    value = i2c_master_recv();  //receive byte from device
    i2c_master_ack(ack);  //send acknowledge bit
    i2c_master_stop();
    return value;
}

void i2c_read_multiple(unsigned char address, unsigned char reg, signed short * data, int length){

    i2c_master_start();
    
    i2c_master_send(address);  //send address + write bit
    i2c_master_send(reg);  //send command register address
    i2c_master_restart();   //send a restart
    i2c_master_send(address | 0b01); //send address + read bit
    
    int i;
    unsigned char temp_data[length];
    
    for (i=0; i<length+1; i++){
        
        temp_data[i] = i2c_master_recv();
        if (i < length){
            i2c_master_ack(0); //send 0 to continue
        }
        else {
            i2c_master_ack(1); //if i is length then send 1 to ack
        }
    }
    i2c_master_stop();
    int k = 0;
    for (i=0; i<7; i++){ //turn unsigned char into signed short
        data[i] = (temp_data[k+1] << 8) | temp_data[k];
        k = k+2;
    }
}