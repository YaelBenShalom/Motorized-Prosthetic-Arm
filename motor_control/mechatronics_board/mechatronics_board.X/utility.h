#ifndef UTIL__H__
#define UTIL__H__

#include <stdio.h> // standard input/output
#include <xc.h>

// pin definitions
#define SD_CS_TRIS TRISAbits.TRISA0 // sd card chip select
#define SD_CS LATAbits.LATA0
#define CD_TRIS TRISAbits.TRISA1 // sd card detect
#define CD PORTAbits.RA1
#define ERR_LED_TRIS TRISBbits.TRISB4 // indicator LED
#define ERR_LED LATBbits.LATB4
#define HB_LED_TRIS TRISBbits.TRISB5 // heartbeat LED
#define HB_LED LATBbits.LATB5
#define USR_TRIS TRISBbits.TRISB6 // USER button
#define USR PORTBbits.RB6
#define IMU_CS_TRIS TRISBbits.TRISB15 // IMU chip select
#define IMU_CS LATBbits.LATB15

// constants
extern const double TICK;
extern const double GRAV;
extern double ACQ_FREQ;

extern int t_LED;

int debounce_user();
void heartbeat();
void initTimers();
void shift_vector(double *vector, int size);
double max_double(double *vector, int size);

#endif