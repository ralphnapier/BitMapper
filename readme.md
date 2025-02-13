![Screenshot 2025-02-13 082823](https://github.com/user-attachments/assets/4e9f086d-7e34-4155-829b-3b82ca8c6322)
This is a program that I made to make an image in to monochrome bitmap for an OLED display. 

The program is meant to be used with a Adafruit_SSD1306 128 x 64 I2C display.


   You can import an image of any resolution, it will convert it first into monochrome, then into 1 bit color depth.
The window displays the image you will see on the OLED display.
Each pixel represents a bit in a bianary array, you can "draw" on the image by clicking and holding the left mouse buton, or click individual pixels to set them to black.
Clicking the right mouse button will invert the tool as to make it turn black pixels white. 

   On the menu bar, the "Adjust Threshold" option will let you increase or decrease the brightness at which the program detremines if the imported image is black or white. The options have the square bracket keys mapped to them, '[' to Increase, ']' to decrease. The next option allows you to change the brush size, '+' to increase, '-' to decrease. The last option is "Shift Pixels". This takes the entire canvas and moves every pixel the direction that is selected.
   
   When the image is displayed in the way you want it to appear, choose "File>Export Bitmap Text File". This will make a "Save as" window appear, and will save the bianary array as a .txt file where you choose. You can then copy the contents of that text file and paste them as you need into your C/C++ program. If you need to change an image that you have already made a .txt file for, there is the option to "Import Text File", this will display the image that the .txt file would render. Make changes and choose to export the bitmap image to save the updated file. 
    
![Untitled-1copy](https://github.com/user-attachments/assets/683a32d6-aa36-49ed-ad6a-722494846340)

![Untitled-1 copy](https://github.com/user-attachments/assets/1e188ca0-6513-4f47-8c8d-eef9a57751b5)
