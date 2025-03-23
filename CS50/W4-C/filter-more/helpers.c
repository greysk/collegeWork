#include <math.h>
#include "bmp.h"
#include "helpers.h"

/* Defined BBOX, a structure to hold the coordinates of
a 3x3 square around a pixel and the number of coordinates
recorded within it.*/
typedef struct
{
    int coord[9][2];
    int numCoords;
}
BBOX;

BBOX get_box(int y, int x, int height, int width, int include_out_of_bounds);

int finish_color(double gy_color, double gx_color);

// Convert image to black and white
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // For every pixel in the image, set a new color value by averaging the value color channels.
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            RGBTRIPLE pixel = image[y][x];
            if ((pixel.rgbtRed + pixel.rgbtGreen + pixel.rgbtBlue) < 400) {
                image[y][x].rgbtRed = 0;
                image[y][x].rgbtGreen = 0;
                image[y][x].rgbtBlue = 0;
            }
            else {
                image[y][x].rgbtRed = 255;
                image[y][x].rgbtGreen = 255;
                image[y][x].rgbtBlue = 255;
            }
        }
    }
    return;
}

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // For every pixel in the image, set a new color value by averaging the value color channels.
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            RGBTRIPLE pixel = image[y][x];
            BYTE grey = round((pixel.rgbtRed + pixel.rgbtGreen + pixel.rgbtBlue) / 3.0);
            image[y][x].rgbtRed = grey;
            image[y][x].rgbtGreen = grey;
            image[y][x].rgbtBlue = grey;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Swap the left half of the image with the right half, and vice versa. Pixel by pixel.
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width / 2; x++)
        {
            RGBTRIPLE pixel = image[y][x];
            image[y][x] = image[y][width - x - 1];
            image[y][width - x - 1] = pixel;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp_image[height][width];
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            // Calculate new values for pixel to blur it.
            int red = 0;
            int green = 0;
            int blue = 0;
            BBOX box = get_box(y, x, height, width, 0);

            for (int i = 0; i < box.numCoords; i++)
            {
                red += image[box.coord[i][0]][box.coord[i][1]].rgbtRed;
                green += image[box.coord[i][0]][box.coord[i][1]].rgbtGreen;
                blue += image[box.coord[i][0]][box.coord[i][1]].rgbtBlue;
            }
            // For each color, average the value across all coordinates in the image around the pixel.
            red = round(red / (float)(box.numCoords));
            green = round(green / (float)(box.numCoords));
            blue = round(blue / (float)(box.numCoords));

            // Set values on temp image to continue setting values based on original image.
            temp_image[y][x].rgbtRed = red;
            temp_image[y][x].rgbtGreen = green;
            temp_image[y][x].rgbtBlue =  blue;
        }
    }
    // Write temp_image color values over original image values.
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            image[y][x] = temp_image[y][x];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Sobel Operator for edge detection and color conversion.
    int gy[] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
    int gx[] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};

    RGBTRIPLE temp_image[height][width];

    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            double gy_r = 0;
            double gy_g = 0;
            double gy_b = 0;

            double gx_r = 0;
            double gx_g = 0;
            double gx_b = 0;

            int red = 0;
            int green = 0;
            int blue = 0;

            BBOX box = get_box(y, x, height, width, 1);

            // Calculate new color value for pixel to highlight edges in image.
            // Loop around surrounding pixels.
            for (int i = 0; i < box.numCoords; i++)
            {
                int y_coord = box.coord[i][0];
                int x_coord = box.coord[i][1];
                int c_red = 0;
                int c_green = 0;
                int c_blue = 0;

                // If pixel is within bounds of image, get color values from image. Otherwise, leave all as 0.
                if ((y_coord >= 0 && y_coord < height) && (x_coord >= 0 && x_coord < width))
                {
                    c_red = image[y_coord][x_coord].rgbtRed;
                    c_green = image[y_coord][x_coord].rgbtGreen;
                    c_blue = image[y_coord][x_coord].rgbtBlue;
                }

                // Sum both Gy and Gx color values.
                gy_r += c_red * gy[i];
                gy_g += c_green * gy[i];
                gy_b += c_blue * gy[i];

                gx_r += c_red * gx[i];
                gx_g += c_green * gx[i];
                gx_b += c_blue * gx[i];
            }
            // Finish calculating final color values.
            red = finish_color(gy_r, gx_r);
            green = finish_color(gy_g, gx_g);
            blue = finish_color(gy_b, gx_b);

            // Set pixel color value in temp image.
            temp_image[y][x].rgbtRed = red;
            temp_image[y][x].rgbtGreen = green;
            temp_image[y][x].rgbtBlue = blue;
        }
    }
    // Write finished temp image values over original image values.
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            image[y][x] = temp_image[y][x];
        }
    }
    return;
}

// Get the coordinates for a 3-by-3 box either skipping or including coordinates out of bounds.
BBOX get_box(int y, int x, int height, int width, int include_out_of_bounds)
{
    int py = 0;
    int px = 0;

    int box_calc[3] = {-1, 0, 1};

    BBOX box;
    // Make sure values in box are all 0 to start.
    for (int k = 0; k < 9; k++)
    {
        for (int m = 0; m < 2; m++)
        {
            box.coord[k][m] = 0;
        }
    }
    box.numCoords = 0;

    // Make coordinates for 3 by 3 box around pixel at x and y coordinates
    for (int i = 0; i < 3; i++)
    {
        py = y + box_calc[i];
        // Unless include_out_of_bounds is 1, skip any x and y coordinates out of bounds.
        if ((py >= 0 && py < height) || include_out_of_bounds == 1)
        {
            for (int j = 0; j < 3; j++)
            {
                px = x + box_calc[j];
                if ((px >= 0 && px < width) || include_out_of_bounds == 1)
                {
                    // Set adjacent coordinate and add to box
                    box.coord[box.numCoords][0] = py;
                    box.coord[box.numCoords][1] = px;
                    // Increase value indicating number of coordinates in box's coordinate array.
                    box.numCoords++;
                }
            }
        }
    }
    return box;
}

// Calculate the new color value for the Edge filter of an image.
int finish_color(double gy_color, double gx_color)
{
    double color = sqrt(pow(gy_color, 2) + pow(gx_color, 2));
    // Make sure value is not more than 255.
    if (color > 255)
    {
        color = 255;
    }
    return (int)round(color);
}
