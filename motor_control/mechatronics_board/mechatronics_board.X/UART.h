#ifndef UART__H__
#define UART__H__

#include<xc.h>           // processor SFR definitions
#include<sys/attribs.h>  // __ISR macro
#include <stdio.h>

char m[100]; //array for UART1

void readUART1(char * string, int maxLength);
void writeUART1(const char * string);
void initUART1();

#endif // UART__H__