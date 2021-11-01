#ifndef SD__H__
#define SD__H__

#include "spi.h"
#include <xc.h>

#define CMD0 0 // CMD0
#define CMD0_ARG 0
#define CMD0_CRC 0x94
#define CMD8 8 // CMD8
#define CMD8_ARG 0x1AA
#define CMD8_CRC 0x86
#define CMD17 17 // CMD17
#define CMD17_CRC 0x00
#define CMD24 24 // CMD24
#define CMD24_CRC 0x00
#define ACMD41 41 // CMD41
#define ACMD41_ARG 0x40000000
#define ACMD41_CRC 0x00
#define CMD55 55 // CMD55
#define CMD55_ARG 0
#define CMD55_CRC 0x00
#define READ_SINGLE 17

#define DAT_ACC 0x05
#define DAT_START 0xFE
#define COMD_ERR 0x80
#define TIMEOUT_ERR 0x81

#define SD_BLOCKLEN 512

int initSD();
int SDcmd(unsigned char comd, unsigned int a, unsigned char crc);
int SDwrite(unsigned int addr, char *p, unsigned char *token);
int SDread(unsigned int addr, char *p, unsigned char *token);

#endif