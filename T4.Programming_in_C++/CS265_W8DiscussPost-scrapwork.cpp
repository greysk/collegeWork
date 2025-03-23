#include <iostream>
#include <iomanip>

using namespace std;

const int PIC_HEIGHT = 5; //The image must be a square.

//A representation of an RGB color value. (https://www.w3schools.com/colors/colors_rgb.asp)
struct rgbType {
    int red = 0;
    int green = 0;
    int blue = 0;
};

//A representation of a image including the image's height, width, and a 2D array of rgbType elements.
struct fakePicType {
    int height = PIC_HEIGHT;
    int width = PIC_HEIGHT;
    rgbType imgColors[PIC_HEIGHT][PIC_HEIGHT];
};

fakePicType makeFakePic(rgbType outlineColor); //Return a fakePicType.
char getPixelColor(rgbType& pixel); //Get a character representation of a color value.
void printCharPic(fakePicType& pic); //Print a character version of a fakePicType.

int main()
{
    rgbType blueRGB; //Declare rgbType structs for the color blue.
    fakePicType newPic; //Declare a fakePicType struct used to get a new fake image.

    blueRGB.blue = 255; //Set the value of the blueRGB.blue to 255, making a representation of RGB(0, 0, 255) aka the color blue.

    newPic = makeFakePic(blueRGB); //Create fake pic with blue-outlined triangle.

    printCharPic(newPic); //Print character version of the newPic.

    return 0;
}

/*
* Create and return the fakePicType struct representing a pixel image of a triangle like ◺. Two rgbType passed by value
* sets the color of the triangle's outline.
*/
fakePicType makeFakePic(rgbType outlineColor)
{
    fakePicType pic; //Declare fakePicType for the output image.
    rgbType rgbWhite; //Declare rgbType for the color white.

    //Set values for RGB(255, 255, 255) aka white.
    rgbWhite.red = 255;
    rgbWhite.green = 255;
    rgbWhite.blue = 255;

    //Row-by-row, set the color value for each pixel in the image.
    for (int y = 0; y < pic.height; y++) //rows ↓
        for (int x = 0; x < pic.width; x++) //columns →
            if (x == y || x == 0 || y == pic.height - 1)
                pic.imgColors[x][y] = outlineColor; //Create ◺ shape.
            else
                pic.imgColors[x][y] = rgbWhite; //Set remaining pixels to white.
    return pic;
}

/*
* Return a char representing the color of the rgbType struct `pixel`. The rgbType is passed by reference so the computer
* does not make a copy of the pixel, because the printCharPic() function make many calls to this function.
* Return values:
*   ' ' if all rgbType member values are 0.
*   'R' if the red value is higher than both the blue and green,
*   'G' if the green value is higher than both the red and blue value,
*   'B' if the blue value is higher than both the red and green, or
*   'X' for any other color value combinations.
*/
char getPixelColor(rgbType& pixel)
{
    if (255 == pixel.red && 255 == pixel.blue && 255 == pixel.green)
        return ' '; //empty
    else if (pixel.red > pixel.blue && pixel.red > pixel.green )
        return 'R'; //Red.
    else if (pixel.green > pixel.blue && pixel.green > pixel.red)
        return 'G'; //Green.
    else if (pixel.blue > pixel.red && pixel.blue > pixel.green)
        return 'B'; //Blue.
    else
        return 'X'; //All other colors.
}

/*
* Print a char version of the fakePicType struct `pic` using getPixelColor(). The fakePicType is passed by reference so as to not
* waste computer resources by making a copy of the fakePicType struct which is especially important for large images.
* Example output of a 5x5 image:
*  B
*  B B
*  B   B
*  B     B
*  B B B B B
*/
void printCharPic(fakePicType& pic)
{
    //Row-by-row, print the character representation of the image.
    for (int y = 0; y < pic.height; y++)
    {
        for (int x = 0; x < pic.width; x++)
            cout << setw(2) << getPixelColor(pic.imgColors[x][y]); //Print the cells (of each column) in one row ➡.
        cout << endl; //Done with one row. Will exit or repeat to print the next row ⬇.
    }
}
