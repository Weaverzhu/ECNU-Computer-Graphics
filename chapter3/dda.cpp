#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void dda(int x0, int y0, int x1, int y1, void (*setPixel)(int, int)) {
    int dx = abs(x1 - x0), dy = abs(y1 - y0);
    int offset = dx > dy ? dx : dy;
    float sx = float(dx) / offset, sy = float(dy) / offset;
    
    float x = x0, y = y0;
    for (int i=0; i<offset; ++i) {
        setPixel(round(x), round(y));
        x += sx;
        y += sy;
    }
}

void print(int x, int y) {
    printf("setPixel %d %d\n", x, y);
}

int main() {
    dda(1, 3, 5, 10, print);
    return 0;
}