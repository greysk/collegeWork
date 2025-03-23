#include <stdio.h>
#include <stdint.h>

typedef uint8_t BYTE;

void write_img(FILE *inptr, FILE *outptr, int depth);

/* Declare a global structure type of 4 bytes
 Variables in structure roughly based off:
    https://en.wikipedia.org/wiki/JPEG#Syntax_and_structure */
typedef struct
{
    BYTE so;
    BYTE im;
    BYTE st;
    BYTE mk;
} JPGSIG;

JPGSIG js;

// Declare a global structure type of 508 bytes
typedef struct
{
    JPGSIG rf[127];
} MEMBLOCK;

MEMBLOCK mb;

int main(int argc, char *argv[])
{
    // Ensure proper command line arguments provided.
    if (argc != 2)
    {
        printf("Usage: ./recovery <file_to_recover>\n");
        return 1;
    }

    // Declare variables for file reading and output file name.
    int images_found = 0;
    char *in_file = argv[1];
    char f_name[7];

    // Open input file in read binary mode and check for errors.
    FILE *inptr = fopen(in_file, "rb");
    if (inptr == NULL)
    {
        printf("Could not open %s\n", in_file);
        return 1;
    }

    // Check for jpg images to be recovered.
    while (fread(&js, sizeof(JPGSIG), 1, inptr))
    {
        // Check start of the memory block for the JPG signature.
        if (js.so == 0xff && js.im == 0xd8 && js.st == 0xff &&
            (js.mk > 0xdf && js.mk < 0xef))
        {
            // Generate name for output file and declare pointer to output.
            sprintf(f_name, "%03i.jpg", images_found);
            FILE *outptr = fopen(f_name, "wb");

            // Write data to file until a JPG signature is encountered.
            write_img(inptr, outptr, 0);

            // Clean up after and record that and image has been recovered.
            fclose(outptr);
            images_found++;

            /* Move back to the beginning of the current memory block
              because write_images() read into it.*/
            fseek(inptr, -1 * sizeof(JPGSIG), SEEK_CUR);
        }
        else
        {
            // Skip to the next memory block.
            fseek(inptr, 508, SEEK_CUR);
        }
    }
    // End of file reached, close input file and exit progrgam.
    fclose(inptr);
    return 0;
}

/* Write the JPG signature and the rest of the memory block to inptr file until
 another JPG signature or the end of the inptr file is encountered .*/
void write_img(FILE *inptr, FILE *outptr, int depth)
{
    // Write to file the JPG signature that triggered the call to write_img.
    fwrite(&js, sizeof(JPGSIG), 1, outptr);

    // Read and write to output the rest of this memory block.
    fread(&mb, sizeof(MEMBLOCK), 1, inptr);
    fwrite(&mb, sizeof(MEMBLOCK), 1, outptr);

    // Read the beginning 4 bytes of the next memory block.
    fread(&js, sizeof(JPGSIG), 1, inptr);

    // Write the entire image to file until the end of the image/memory card is reached.
    if (feof(inptr) || (js.so == 0xff && js.im == 0xd8 && js.st == 0xff && (js.mk > 0xdf && js.mk < 0xef)))
    {
        return;
    }
    else
    {
        write_img(inptr, outptr, depth);
    }
    return;
}
