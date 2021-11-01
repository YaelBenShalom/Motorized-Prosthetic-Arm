#include "sd_card.h"

/*   send a command to the SD card   */
int SDcmd(unsigned char comd, unsigned int a, unsigned char crc)
{
  /*
   comd   command code
   a      data block address
   */
  int i, r;

  // send 6-byte command packet
  spi_io(comd | 0x40); // send command
  spi_io(a >> 24);     // address MSB
  spi_io(a >> 16);
  spi_io(a >> 8);
  spi_io(a);          // address LSB
  spi_io(crc | 0x01); // CRC

  // send up to 8 bytes while waiting for response
  for (i = 0; i < 8; i++)
  {
    r = spi_io(0xFF);
    if (r != 0xFF)
    {
      break;
    }
  }

  return r;
}

int initSD()
{
  /*

   */
  int i, r;
  int res[5];
  char message[50];

  SPI1BRG =
      95; // set SPI baud rate to 250kHz until SD card properly initialized

  // allow 80 clock cycles for startup
  for (i = 0; i < 10; i++)
  {
    spi_io(0xFF);
  }

  // reset the SD card
  SD_CS = 0;
  r = SDcmd(CMD0, CMD0_ARG, CMD0_CRC); // GO_IDLE_STATE
  SD_CS = 1;
  if (r != 1)
  { // return command error if IDLE not returned
    return COMD_ERR;
  }

  // send interface condition
  SD_CS = 0;
  res[0] = SDcmd(CMD8, CMD8_ARG, CMD8_CRC); // SEND_IF_COND

  // R1 byte of R7 response must equal 0x00 or 0x01
  if (res[0] > 1)
  {
    return res[0];
  }

  // read remaining four bytes of R7 response
  for (i = 1; i < 5; i++)
  {
    res[i] = spi_io(0xFF);
  }
  SD_CS = 1;

  // send operating condition
  SD_CS = 0;
  for (i = 0; i < 10000; i++)
  {
    SDcmd(CMD55, CMD55_ARG, CMD55_CRC);        // application command notifier
    r = SDcmd(ACMD41, ACMD41_ARG, ACMD41_CRC); // operating condition command
    if (!r)
    { // break loop once IDLE ends (command response = 0)
      SD_CS = 1;
      break;
    }
  }
  if (i == 10000)
  {
    return TIMEOUT_ERR; // return timeout error if IDLE does not terminate
  }

  // return SPI communication rate to maximum
  SPI1CON = 0;      // disable SPI1
  SPI1BRG = 1;      // set baud rate to 12 MHz
  SPI1CON = 0x8120; // re-enable SPI1

  return r;
}

int SDwrite(unsigned int addr, char *p, unsigned char *token)
{
  /*
   Write a 512-byte-wide block of data to the SD card

   addr       32-bit logic block address
   p          pointer to data buffer
   token      pointer to response token
   */
  int i, r, read;
  char message[50];

  *token = 0xFF;

  // set CS pin low
  SD_CS = 0;

  // WRITE_BLOCK
  r = SDcmd(CMD24, addr, CMD24_CRC);

  if (r == 0)
  { // check if command was accepted
    // send data start token
    spi_io(DAT_START);

    // write buffer to card
    for (i = 0; i < SD_BLOCKLEN; i++)
    {
      spi_io(p[i]);
    }
    // send 16-bit dummy CRC
    spi_io(0xFF);
    spi_io(0xFF);

    // wait for a response, 250ms timeout
    TMR4 = 0;
    while (TMR4 < 46874)
    {
      if ((read = spi_io(0xFF)) != 0xFF)
      {
        *token = 0xFF;
        break;
      }
    }

    // check if data accepted
    if ((read & 0x1F) == DAT_ACC)
    {
      *token = DAT_ACC; // set token to data accepted

      // wait for write completion, 250ms timeout
      TMR4 = 0;
      while (spi_io(0xFF) == 0x00)
      {
        if (TMR4 > 46874)
        {                // if timeout reached
          *token = 0x00; // set token to write complete timeout
          break;
        }
      }
    }
  }

  SD_CS = 1; // set CS pin high

  return r; // returns 0 if command accepted,
            // combine with token to know if write successful
}

int SDread(unsigned int addr, char *p, unsigned char *token)
{
  /*
   Read a 512-byte-wide block of data from the SD card
   */
  int i, r, read;

  *token = 0xFF;

  SD_CS = 0; // set CS pin low

  r = SDcmd(CMD17, addr, CMD17_CRC); // READ_BLOCK

  // if the card sends a response
  if (r != 0xFF)
  {
    // wait for a response token
    TMR4 = 0;
    while (TMR4 < 18749)
    {
      if ((read = spi_io(0xFF)) != 0xFF)
      {
        break;
      }
    }

    // if response token is received
    if (read == 0xFE)
    {
      // read 512-byte block
      for (i = 0; i < SD_BLOCKLEN; i++)
      {
        p[i] = spi_io(0xFF);
      }

      // read 16-bit CRC
      spi_io(0xFF);
      spi_io(0xFF);
    }

    // set token to card response
    *token = read;
  }

  SD_CS = 1; // set CS pin high

  return r; // returns card response to CMD17,
            // combine with token to know if read successful
}