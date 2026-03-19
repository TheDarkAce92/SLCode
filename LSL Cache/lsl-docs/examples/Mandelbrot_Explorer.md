---
name: "Mandelbrot Explorer"
category: "example"
type: "example"
language: "LSL"
description: "list faces = [3,7,4,6,1];"
wiki_url: "https://wiki.secondlife.com/wiki/Mandelbrot_Explorer"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// Mandelbrot Explorer by Babbage Linden
//
// Interactive Fractal Explorer Demo
//
// Add this script to a screen made from 245 linked prisms each manipulated to show 5 faces in one direction
//(The script here will create the correct shape object http://wiki.secondlife.com/wiki/XyText_1.5)
// to form a 35x35 pixel display. When rezzed or reset the object will calculate and display a mandelbrot set.
// Clicking on the display will centre the view on the clicked prim and zoom in, allowing the fractal to be
// explored. To return to the initial image either reset the script, or take and rez the object.
//
// Available under the Creative Commons Attribution-ShareAlike 2.5 license
// http://creativecommons.org/licenses/by-sa/2.5/

list faces = [3,7,4,6,1];

integer xsize=35;
integer ysize=35;
integer numfaces=5;
integer fwidth=7;

integer linkNumToX(integer linkNum)
{
    integer result = ((linkNum - 1) % fwidth) * numfaces + (numfaces / 2);
    return result;
}

integer linkNumToY(integer linkNum)
{
    integer result = ((linkNum - 1) / fwidth);
    return result;
}

setpixel(integer x, integer y, vector colour)
{
    integer face = (y*xsize) + x;
    integer linknum = face/numfaces;
    integer primface = face - (linknum*5);
    llSetLinkColor(linknum + 1, colour, llList2Integer(faces,primface));
}

mandlebrot(float startx, float starty, float zoom, integer width)
{
    integer height = width;
    integer i;
    integer m = 60; // Max iterations.
    integer isOverLimit = FALSE;
    float Zr = 0.0;
    float Zi = 0.0;
    float Cr = 0.0;
    float Ci = 0.0;
    float Tr;
    float Ti;
    float limit2 = 4.0;

    integer y;
    for(y = 0; y < height; y++)
    {
        integer x;
         for(x = 0; x < width; x++)
         {
            Zr = 0.0; Zi = 0.0;
            Cr = (2.0 * (x + (startx / zoom)) / width - 1.5) * zoom;
            Ci = (2.0 * (y + (starty / zoom)) / height - 1.0) * zoom;

            // Evaluate sequence until either max iterations has been
            // reached or threshold is breached.
            i = 0;
            do {
               Tr = Zr*Zr - Zi*Zi + Cr;
               Ti = 2.0*Zr*Zi + Ci;
               Zr = Tr; Zi = Ti;
               isOverLimit = Zr*Zr + Zi*Zi > limit2;
            } while (!isOverLimit && (++i < m));

            // Generate colour for each possible iteration.
            // First fill r, then overflow in to g, then b.
            vector colour = <0,0,0>;
            if(i < m)
            {
                float step = m / 3.0;
                if(i > 0)
                {
                    colour.x = i / step;
                    i -= (integer)step;
                }
                if(i > 0)
                {
                    colour.y = i / step;
                    i -= (integer)step;
                }
                if(i > 0)
                {
                    colour.z = i / step;
                    i -= (integer)step;
                }
            }
            setpixel(x, y, colour);
        }
    }
}

float gZoom;
float gMinX;
float gMinY;

init()
{
    // Draw initial fractal image.
    gZoom = 1.0;
    gMinX = 0;
    gMinY = 0;
    mandlebrot(gMinX, gMinY, gZoom, 35);
}

default
{
    on_rez(integer param)
    {
        init();
    }

    state_entry()
    {
        init();
    }

    touch_start(integer num)
    {
        // Convert link number in to screen space.
        float dx = linkNumToX(llDetectedLinkNumber(0));
        float dy = linkNumToY(llDetectedLinkNumber(0));

        // Make dx and dy relative to centre.
        dx -= (xsize / 2);
        dy -= (ysize / 2);

        // Adjust gMinX and gMinY by x and y.
        gMinX += dx * gZoom;
        gMinY += dy * gZoom;

        // Calculate Mandelbrot and increase zoom.
        mandlebrot(gMinX, gMinY, gZoom, 35);
        gZoom *= 0.9;
    }
}
```