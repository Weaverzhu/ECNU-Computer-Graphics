#include <GL\freeglut.h>
#include <math.h>  // For math routines (such as sqrt & trig).

GLfloat xRotated, yRotated, zRotated;
GLdouble radius = 2;
GLfloat qaBlack[] = {0.0, 0.0, 0.0, 1.0};  // Black Color
GLfloat qaGreen[] = {1.0, 0.0, 0.0, 1.0};  // Green Color
GLfloat qaWhite[] = {1.0, 1.0, 1.0, 1.0};  // White Color
GLfloat qaRed[] = {1.0, 0.0, 0.0, 1.0};    // Red Color

// Set lighting intensity and color
GLfloat qaAmbientLight[] = {0.1, 0.1, 0.1, 1.0};
GLfloat qaDiffuseLight[] = {1, 1, 1, 1.0};
GLfloat qaSpecularLight[] = {1.0, 1.0, 1.0, 1.0};
GLfloat emitLight[] = {0.9, 0.9, 0.9, 0.01};
GLfloat Noemit[] = {0.0, 0.0, 0.0, 1.0};
// Light source position
GLfloat qaLightPosition[] = {0, 0, 0, 1};   // Positional Light
GLfloat qaLightDirection[] = {1, 1, 1, 0};  // Directional Light

void display(void);
void reshape(int x, int y);

void idleFunc(void) {
    if (zRotated > 360.0) {
        zRotated -= 360.0 * floor(zRotated / 360.0);  // Don't allow overflow
    }

    if (yRotated > 360.0) {
        yRotated -= 360.0 * floor(yRotated / 360.0);  // Don't allow overflow
    }
    zRotated += 0.1;
    yRotated += 0.1;

    display();
}
void initLighting() {
    // Enable lighting
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);

    // Set lighting intensity and color
    glLightfv(GL_LIGHT0, GL_AMBIENT, qaAmbientLight);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, qaDiffuseLight);
    glLightfv(GL_LIGHT0, GL_POSITION, qaLightPosition);
    glLightfv(GL_LIGHT0, GL_SPECULAR, qaSpecularLight);
    ////////////////////////////////////////////////
}
void keyboard(unsigned char key, int x, int y) {
    if (key == 'l' || key == 'L') {
        glEnable(GL_LIGHTING);
    } else if (key == 'd' || key == 'D') {
        glDisable(GL_LIGHTING);
    }
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(350, 350);
    glutCreateWindow("Teapot -");
    initLighting();

    xRotated = yRotated = zRotated = 0.0;

    glutIdleFunc(idleFunc);
    glutDisplayFunc(display);
    glutKeyboardFunc(keyboard);  // Register keyboard callback
    glutReshapeFunc(reshape);
    glutMainLoop();
    return 0;
}

void display(void) {
    glMatrixMode(GL_MODELVIEW);
    // clear the drawing buffer.
    glClear(GL_COLOR_BUFFER_BIT);
    // clear the identity matrix.
    glLoadIdentity();

    glTranslatef(0.0, 0.0, -20.0);

    glPushMatrix();

    glTranslatef(0.0, 0.0, 0);
    // Set material properties
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, qaRed);

    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, qaRed);

    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, qaWhite);

    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 1);

    glutSolidTeapot(radius);
    glPopMatrix();

    glPushMatrix();
    glRotatef(yRotated, 0.0, 1.0, 0.0);
    glTranslatef(5.0, 0.0, 0.0);
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION,
                 emitLight);  // Make sphere glow (emissive)
    glutSolidSphere(radius / 6, 25, 25);
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, Noemit);
    glPopMatrix();

    glPushMatrix();
    glRotatef(-yRotated, 0.0, 1.0, 0.0);
    glTranslatef(5.0, 0.0, 0.0);
    glLightfv(GL_LIGHT0, GL_POSITION, qaLightPosition);
    glPopMatrix();

    glFlush();
    glutSwapBuffers();
}

void reshape(int x, int y) {
    if (y == 0 || x == 0) return;
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    gluPerspective(39.0, (GLdouble)x / (GLdouble)y, 0.6, 40.0);
    glMatrixMode(GL_MODELVIEW);
    glViewport(0, 0, x, y);  // Use the whole window for rendering
}
