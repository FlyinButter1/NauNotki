#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <ctype.h>

// cleaner stdint.h datatype definitions in accordance with microsoft guidelines
typedef uint8_t  BYTE;
typedef uint32_t DWORD;
typedef int32_t  LONG;
typedef uint16_t WORD;

// BITMAPFILEHEADER and BITMAPINFOHEADER adapted from Microsoft Corporation's publicly available resources.
// Changes have been made to BITMAPINFOHEADER due to specificities of particular bitmap format.
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

// basic RGB pixel struct
typedef struct{
    BYTE  Blue;
    BYTE  Green;
    BYTE  Red;
} __attribute__((__packed__))
RGBTRIPLE;

// RGBTRIPLE's constructor (not read from file, constructed from random data)
RGBTRIPLE construct(BYTE Blue, BYTE Green, BYTE Red){
	RGBTRIPLE output;
	output.Blue = Blue;
	output.Green = Green;
	output.Red = Red;
	return output;
}

// places all three RGB colour values of the pixel defined in RGBTRIPLE
void putcolour(FILE* ptr, RGBTRIPLE colour){
	fputc(colour.Blue, ptr);
	fputc(colour.Green, ptr);
	fputc(colour.Red, ptr);
}

// calculated using web standard established by the W3 Consortium: https://www.w3.org/TR/AERT/#color-contrast
BYTE brightness(RGBTRIPLE colour){
    return (BYTE)(0.299 * colour.Red + 0.587 * colour.Green + 0.114 * colour.Blue);
}

// function calculates reverse blandness: the lower the number, the grayer (or more bland) the pixel
// calculated using the difference between lowest and highest RGB value to find grayest pixels
BYTE rev_blandness(RGBTRIPLE colour){
    BYTE min = colour.Blue, max = colour.Blue;
    if (colour.Green < min)
        min = colour.Green;
    if (colour.Red < min)
        min = colour.Red;
    if (colour.Green > max)
        max = colour.Green;
    if (colour.Red > max)
        max = colour.Red;
    return max - min;
}
// hashing function used to generate numbers from usernames
//               a,  b,  c,  d,  e,  f,  g,  h,  i, j,  k,  l,  m,  n,  o, p,  q, r, s, t, u,  v,  w,  x,  y,   z
int weights[] = {-2, 43, 17, 11, -1, 31, 37, 5, -5, 59, 53, 13, 23, 2, -3, 41, 0, 7, 3, 1, -7, 47, 29, 61, -11, 67};
unsigned int hash(const char* word){
    unsigned int output = 1048576;
    for(int i = 1; i <= strlen(word); i *= 2){
        output += weights[(word[i-1]%32)-1]*toupper(word[i-1]);
    }
    return (unsigned int)((output ^ 12200160415121876738llu)&(4294967295));
} // fibonacci hashing in unsigned long long casted to unsigned int using modulo expressed as bitwise AND

void generate(const char* inputname, const char* outputname, const char* username, int FACTOR){
    clock_t start_time, end_time; // time measurement for debug and control purposes
    start_time = clock();
    unsigned int randomness_hash = hash(username);
	srand(randomness_hash); // randomness using specific randomness source
	FILE *inptr = fopen(inputname, "rb");
	FILE *outptr = fopen(outputname, "wb");
	if(inptr == NULL){
        printf("Could not open template.bmp.");
        return;
    }
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    //printf("%08X\n", bi.biHeight); debug
    //printf("%08X\n", bi.biWidth); debug
	int height = bi.biHeight, width = bi.biWidth;
	int padding = (4 - (width * sizeof(RGBTRIPLE)) % 4) % 4; // one byte of padding after each line is necessary
    //printf("%d\n%d\n", height, width); debug
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr); // writes the template headers into a new file
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr); // mandatory for the file to even open at all
    fputc(0x00, outptr); // two bytes of nothing loaded into the files, deleting this breaks the program, do not delete
    fputc(0x00, outptr);
    RGBTRIPLE* cols = malloc(sizeof(RGBTRIPLE)*(height*width/(FACTOR*FACTOR)));
    for(int i = 0; i < (height*width/(FACTOR*FACTOR)); i++){
        RGBTRIPLE col = construct(rand() % 256, rand() % 256, rand() % 256);
        if(brightness(col) <= 35 || brightness(col) >= 215 || rev_blandness(col) <= 25){
            i--; // blocking too dark, too bright and too gray colours for maximising colourfulness
            continue;
        }
        cols[i] = col;
	}
    for(int l = 0; l < height; l++){
        // write row to outfile
        for(int j = 0; j < width; j++){
        	RGBTRIPLE col = (cols[(j/FACTOR)*FACTOR+(l/FACTOR)]);
	        putcolour(outptr, col);
		}
        // write padding at end of row - necessary due to specifics of the BMP format
        for(int k = 0; k < padding; k++){
            fputc(0x00, outptr);
        }
    }
    fclose(inptr); // closing files - important, deleting this causes segmentation faults, do not delete
    fclose(outptr);
    end_time = clock();
    printf("Generated profile picture for user %s at %s, factor %d, hash %u, size %d x %d. Took %.10g seconds.\n",
    username, outputname, FACTOR, randomness_hash, height, width, (((double)(end_time - start_time)) / CLOCKS_PER_SEC));
}
