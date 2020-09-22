#include <stdlib.h>
#include <math.h>
#include <stdio.h>

void bresenham(int x0, int y0, int x1, int y1, void (*setPixel)(int, int)) {
    int dx = abs(x1 - x0), dy = abs(y1 - y0);
    int offset = dx > dy ? dx : dy;
    int x = x0, y = y0;


    // if (dx < dy) {
    //     int p = 2 * dx * y - 2 * dy * x + 
    //     for (int i=y0; i<=y1; ++i) {

    //     }   
    // }
}

int main(int argc, char const *argv[])
{
    
    return 0;
}
