#include "dsp.h"

double calc_Q_scale(double * in, int len, double div) {
    /*
     
     */
    int i = 0;                      // counter
    double mx = 0;                  // "largest magnitude in array" variable
    double sf = 0.0;                // scaling factor
    
    // iterate through input array to find largest magnitude
    for (i = 0; i < len; i++) {
        mx = max(mx, fabs(in[i]));
    }
    
    // calculate scaling factor based on 
    sf = (double)QFORMAT/(mx * div);
    
    return sf;
}

void get_fft(double * out, double * signal, double div) {
    /*
        Performs a Fast Fourier Transform on a signal of defined length
     */
    int i = 0;                                              // counter
    int16c twiddle[LEN/2];                                  // twiddle factors array
    int16c fft_in[LEN], fft_out[LEN];                       // FFT input and output arrays
    int16c inter[LEN];                                      // intermediate results array
    double scale = calc_Q_scale(signal, LEN, div);          // scaling factor

    // convert each signal value to 16-bit fixed-point integer
    for (i = 0; i < LEN; i++) {
        fft_in[i].re = signal[i]*scale;
        fft_in[i].im = 0;
    }
    
    memcpy(twiddle, TWIDDLE, sizeof(twiddle));              // copy twiddle factors to RAM
    
    mips_fft16(fft_out, fft_in, twiddle, inter, LOG2N);     // perform FFT
    
    // convert FFT results back to double
    for (i = 0; i < LEN; i++) {
        double re = fft_out[i].re/scale;
        double im = fft_out[i].im/scale;
        out[i] = sqrt(re*re + im*im);
    }
}

void fft_fold(int * fft_in, int * fft_out, int size_in, int size_out) {
    /*
        "Folds" a two-sided Fast Fourier transform output vector to create the one-sided
     frequency spectrum
     */
    int i;                                  // counter
    
    // first elements (DC component) equal
    fft_out[0] = fft_in[0];
    
    // "fold" the two-sided vector in half by adding second element to second-to-last element,
    // third element to third-to-last element, etc
    for (i = 1; i < size_out; i++) {
        fft_out[i] = fft_in[i] + fft_in[size_in - (i + 1)];
    }
}