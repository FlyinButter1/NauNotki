#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// cleaner struct definitions
typedef uint8_t  BYTE;
typedef uint32_t DWORD;
typedef int32_t  LONG;
typedef uint16_t WORD;

// BITMAPFILEHEADER and BITMAPINFOHEADER adapted from Microsoft Corporation's publicly available resources.
// Changes have been made to BITMAPINFOHEADER due to specificities of particular Bitmap format.
typedef struct{
    WORD   bfType;
    DWORD  bfSize;
    WORD   bfReserved1;
    WORD   bfReserved2;
    DWORD  bfOffBits;
} __attribute__((__packed__))
BITMAPFILEHEADER;

typedef struct{
	DWORD   biSize;
    DWORD   biHeight; // DWORD instead of LONG for no apparent reason
    DWORD   biWidth;  // -||-
    WORD    biBitCount;
    DWORD   biCompression;
    DWORD   biSizeImage;
    LONG    biXPelsPerMeter;
    LONG    biYPelsPerMeter;
    DWORD   biClrUsed;
    DWORD   biClrImportant;
} __attribute__((__packed__))
BITMAPINFOHEADER;

typedef struct{
    BYTE  rgbtBlue;
    BYTE  rgbtGreen;
    BYTE  rgbtRed;
} __attribute__((__packed__))
RGBTRIPLE;

// RGBTRIPLE's constructor (not read from file)
RGBTRIPLE construct(BYTE rgbtBlue, BYTE rgbtGreen, BYTE rgbtRed){
	RGBTRIPLE output;
	output.rgbtBlue = rgbtBlue;
	output.rgbtGreen = rgbtGreen;
	output.rgbtRed = rgbtRed;
	return output;
}

void putcolour(FILE* ptr, BYTE rgbtBlue, BYTE rgbtGreen, BYTE rgbtRed){
	fputc(rgbtBlue, ptr);
	fputc(rgbtGreen, ptr);
	fputc(rgbtRed, ptr);
}

void generate(const char* inputname, const char* outputname, int FACTOR){
	srand(time(NULL));
	FILE *inptr = fopen(inputname, "rb");
	FILE *outptr = fopen(outputname, "wb");
	if(inptr == NULL){
        printf("Could not open template.bmp.");
        return;
    }
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER)+1, 1, inptr);
    //printf("%08X\n", bi.biHeight); debug
    //printf("%08X\n", bi.biWidth); debug
	int height = bi.biHeight, width = bi.biWidth, i, j, k;
	int padding = (4 - (width * sizeof(RGBTRIPLE)) % 4) % 4;
    //printf("%d\n%d\n", height, width); debug
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);
    fputc(0x00, outptr);
    fputc(0x00, outptr);
    RGBTRIPLE* cols = malloc(sizeof(RGBTRIPLE)*(height*width/(FACTOR*FACTOR)));
    for(i = 0; i < (height*width/(FACTOR*FACTOR)); i++){
    	cols[i] = construct(rand() % 256, rand() % 256, rand() % 256);
	}
    for(i = 0; i < height; i++){
        // Write row to outfile
        for(j = 0; j < width; j++){
        	RGBTRIPLE col = (cols[(j/FACTOR)*FACTOR+(i/FACTOR)]);
	        putcolour(outptr, col.rgbtBlue, col.rgbtGreen, col.rgbtRed);
		}
        // Write padding at end of row
        for(k = 0; k < padding; k++){
            fputc(0x00, outptr);
        }
    }
    fseek(outptr, 0, SEEK_SET);
    unsigned char byte = 0x42; // Example byte value
    fwrite(&byte, 1, 1, outptr); // Write one byte to the file
    fclose(outptr);
}
