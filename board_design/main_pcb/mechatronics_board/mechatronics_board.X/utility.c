#include "utility.h"

const double TICK = 1 / 48000000; // length of one clock cycle (20 ns)
const double GRAV = 9.81;         // gravitational constant (in m/s^2)
double ACQ_FREQ = 150.0;          // FFT frequency (200 Hz)
int t_LED = 0;

int debounce_user()
{
  int q = 0; // counter

  // iterate counter up to 10000 while button is pressed
  while (!USR && q < 10000)
  {
    q++;
  }

  // wait until button is released
  while (!USR)
  {
    ;
  }

  return q == 10000; // return debounce status (if successful,
                     // q = 10000 and function returns 1, 0 otherwise)
}

void heartbeat()
{
  // Function blinks system LED at 5 Hz
  t_LED += _CP0_GET_COUNT();

  if (t_LED > 24000000 / 10)
  {
    HB_LED = !HB_LED;
    t_LED = 0;
  }

  _CP0_SET_COUNT(0);
}

void initTimers()
{
  // initialize Timer2
  // PURPOSE: acceleration offset calculation
  T2CONbits.TCKPS = 0b111; // 256:1 prescale
  T2CONbits.TCS = 0;       // internal peripheral clock
  T2CONbits.T32 = 1;       // Timer2 as 32-bit timer
  T2CONbits.ON = 1;        // turn on Timer2

  // initialize Timer4
  // PURPOSE: timing SD card read/write operations
  T4CONbits.TCKPS = 0b111; // 256:1 prescale
  T4CONbits.TCS = 0;       // internal peripheral clock
  T4CONbits.T32 = 0;       // Timer4 as 16-bit timer
  T4CONbits.ON = 1;        // turn on Timer4

  // initialize Timer5
  // PURPOSE: acquire acceleration & perform FFT
  T5CONbits.TCKPS = 0b011; // 8:1 prescale
  T5CONbits.TCS = 0;       // internal peripheral clock
  T5CONbits.ON = 1;        // turn on Timer5
}

void shift_vector(double *vector, int size)
{
  int i = 0; // counter

  for (i = 0; i < size - 1; i++)
  {
    vector[i] = vector[i + 1];
  }
}

double max_double(double *vector, int size)
{
  int i = 0;
  double max = 0.0;

  for (i = 0; i < size - 1; i++)
  {
    if (vector[i] > max)
    {
      max = vector[i];
    }
  }
  return max;
}