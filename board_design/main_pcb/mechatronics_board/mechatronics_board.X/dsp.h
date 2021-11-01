#ifndef DSP__H__
#define DSP__H__

#include "utility.h"
#include <dsplib_dsp.h>
#include <fftc.h> // FFT twiddle factors
#include <math.h>
#include <string.h>
#include <xc.h>

// change these to variables
#define TWIDDLE                                                          \
  fft16c128     // FFT twiddle factors; 16-bit fixed-point fractional    \
                // IMPORTANT: change this to appropriate value if length \
                // of FFT input signal changes
#define LOG2N 7 // log base 2 of signal buffer length (length = 1024)
#define LEN (1 << LOG2N)
#define QFORMAT (1 << 15) // factor mapping (-1, 1) range to 16-bit integer
#define FFTDIV 10.0       // FFT input scaling factor

double calc_Q_scale(double *in, int len, double div);
void get_fft(double *out, double *signal, double scale);
void fft_fold(int *fft_in, int *fft_out, int size_in, int size_out);

#endif