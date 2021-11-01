#include "font.h"

void drawChar(unsigned char pos_x, unsigned char pos_y, char character)
{
  /*
      Arguments:
         pos_x       x-coordinate (column) of upper-left corner of character
         pos_y       y-coordinate (row) of upper-left corner of character
         character   ASCII value of character to write
   */
  int a, b; // column, row counter variables

  for (a = 0; a < 5; a++)
  {                                                  // iterate through columns
    unsigned char byte = ASCII[character - 0x20][a]; // column byte to write

    for (b = 0; b < 8; b++)
    { // iterate through rows
      unsigned char pix =
          (byte >> b) &
          1; // get each pixel value by bitshifting right, ANDing with 1

      ssd1306_drawPixel(pos_x + a, pos_y + b, pix); // turn pixel on or off
    }
  }
}

void drawString(unsigned char pos_x, unsigned char pos_y, char *message)
{
  /*
      Arguments:
          pos_x       x-coordinate (column) of first character
          pos_y       y-coordinate (row) of first character
          message     string to print to screen

      Info:
          Screen is 128c x 32r
   */
  int c = 0; // column counter
  int n;     // character number counters

  for (n = 0; n < strlen(message); n++)
  { // iterate through string
    if ((pos_x + c) * 5 > 122)
    { // check to make sure
      pos_y++;
      c = 0;
    }

    drawChar((pos_x + c) * 5, pos_y * 8, message[n]);
    c++;
  }
}