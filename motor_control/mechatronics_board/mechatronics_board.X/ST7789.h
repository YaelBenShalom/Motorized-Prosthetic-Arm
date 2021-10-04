#ifndef ST7789_H__
#define ST7789_H__

// ST7789 registers
#define ST7789_XSTART 0x00
#define ST7789_YSTART 0x00
#define ST7789_NOP     0x00
#define ST7789_SWRESET 0x01
#define ST7789_RDDID   0x04
#define ST7789_RDDST   0x09
#define ST7789_SLPIN   0x10
#define ST7789_SLPOUT  0x11
#define ST7789_PTLON   0x12
#define ST7789_NORON   0x13
#define ST7789_INVOFF  0x20
#define ST7789_INVON   0x21
#define ST7789_DISPOFF 0x28
#define ST7789_DISPON  0x29
#define ST7789_CASET   0x2A
#define ST7789_RASET   0x2B
#define ST7789_RAMWR   0x2C
#define ST7789_RAMRD   0x2E
#define ST7789_PTLAR   0x30
#define ST7789_COLMOD  0x3A
#define ST7789_MADCTL  0x36
#define ST7789_FRMCTR1 0xB1
#define ST7789_FRMCTR2 0xB2
#define ST7789_FRMCTR3 0xB3
#define ST7789_INVCTR  0xB4
#define ST7789_DISSET5 0xB6
#define ST7789_PWCTR1  0xC0
#define ST7789_PWCTR2  0xC1
#define ST7789_PWCTR3  0xC2
#define ST7789_PWCTR4  0xC3
#define ST7789_PWCTR5  0xC4
#define ST7789_VMCTR1  0xC5
#define ST7789_RDID1   0xDA
#define ST7789_RDID2   0xDB
#define ST7789_RDID3   0xDC
#define ST7789_RDID4   0xDD
#define ST7789_PWCTR6  0xFC
#define ST7789_GMCTRP1 0xE0
#define ST7789_GMCTRN1 0xE1

#define MADCTL_MY  0x80
#define MADCTL_MX  0x40
#define MADCTL_MV  0x20
#define MADCTL_ML  0x10
#define MADCTL_RGB 0x00
#define MADCTL_BGR 0x08
#define MADCTL_MH  0x04

#define _GRAMWIDTH 240
#define _GRAMHEIGH 240 
#define _GRAMSIZE  _GRAMWIDTH * _GRAMHEIGH

// colors
#define	BLACK     0x0000
#define WHITE     0xFFFF
#define	BLUE      0x001F
#define	RED       0xF800
#define	GREEN     0x07E0
#define CYAN      0x07FF
#define MAGENTA   0xF81F
#define YELLOW    0xFFE0

void LCD_command(unsigned char); // send a command to the LCD
void LCD_data(unsigned char); // send data to the LCD
void LCD_data16(unsigned short); // send 16 bit data to the LCD
void LCD_init(void); // send the initializations to the LCD
void LCD_drawPixel(unsigned short, unsigned short, unsigned short); // set the x,y pixel to a color
void LCD_setAddr(unsigned short, unsigned short, unsigned short, unsigned short); // set the memory address you are writing to
void LCD_clearScreen(unsigned short); // set the color of every pixel
void drawChar(unsigned short x, unsigned short y, unsigned short color, unsigned char letter); //fcn 1 we write
void drawBar(unsigned short x, unsigned short y, unsigned short index, unsigned short length); //fcn 2 we write

#endif