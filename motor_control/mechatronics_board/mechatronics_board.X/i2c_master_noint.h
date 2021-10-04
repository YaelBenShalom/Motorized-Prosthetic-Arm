#ifndef I2C_MASTER_NOINT_H__
#define I2C_MASTER_NOINT_H__
// Header file for i2c_master_noint.c
// helps implement use I2C1 as a master without using interrupts

#include <xc.h>
#include<sys/attribs.h> //ISR macro

void i2c_master_setup(void); // set up I2C1 as master
void i2c_master_start(void); // send a START signal
void i2c_master_restart(void); // send a RESTART signal
void i2c_master_send(unsigned char byte); // send a byte (either an address or data)
unsigned char i2c_master_recv(void); // receive a byte of data
void i2c_master_ack(int val); // send an ACK (0) or NACK (1)
void i2c_master_stop(void); // send a stop
void writePin(unsigned char address, unsigned char reg, unsigned char value); //write 1 byte
unsigned char readPin(unsigned char address, unsigned char reg, int ack);    //read 1 byte
void i2c_read_multiple(unsigned char address, unsigned char register, signed short * data, int length);

#endif