---
name: "Rainbow_palette"
category: "example"
type: "example"
language: "LSL"
description: "// Rainbow Palette by Rui Clary // This script will only run in Mono enabled, Second Life Viewer 1.21 or above. // // Interactive Rainbow Palette // // Add this script to a cube prim and add \"Listen Palete\" script to another Object. // You can resize and stretch the cube, the way you want, to make it look like a color palette. // Touch face 1 of \"Rainbow Palette\" to change \"Listen Object\" color. // // Modified by Rui Clary on 2011.06.20 - some corrections // Available under the Creative Commons Attribution-ShareAlike 3.0 license // http://creativecommons.org/licenses/by-sa/3.0/ default { state_entry() { llSetObjectName(\"pal\"); llSetTexture (\"5748decc-f629-461c-9a36-a35a221fe21f\",ALL_SIDES); llSetTexture(\"5543eaa7-4283-8383-eef9-945c0b3f25c7\",1); } touch(integer num_detected) { float x; float r; float g; float b; vector touchedpos = llDetectedTouchST(0); if (llDetectedTouchFace(0)==1) { x=360*touchedpos.x; r=0; g=0; b=0; if (x>=0&&x<=60){ r=255; g=x*255/60; } if (x>60&&x<=120){ r=255-(x-60)*255/60; g=255; } if (x>120&&x<=180){ g=255; b=(x-120)*255/60; } if (x>180&&x<240){ g=255-(x-180)*255/60; b=255; } if (x>240&&x<300){ r=(x-240)*255/60; b=255; } if (x>300&&x<=360){ r=255; b=255-(x-300)*255/60; } llSay(4,\"<\"+(string)(r/255)+\",\"+(string)(g/255)+\",\"+(string)(b/255)+\">\"); } } } // Rainbow Palette Listen Script by Rui Clary // // Second component of Rainbow Palette // // Add this script to \"Listen Object\". default { state_entry() { llSetTexture (\"5748decc-f629-461c-9a36-a35a221fe21f\",ALL_SIDES); llListen( 4, \"pal\", NULL_KEY, \"\" ); } listen( integer channel, string name, key id, string message ) { llSetColor((vector)message,0); } } Modified version with fixed floats and \"organized\" :)"
wiki_url: "https://wiki.secondlife.com/wiki/Rainbow_palette"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
// Rainbow Palette by Rui Clary
// This script will only run in Mono enabled, Second Life  Viewer 1.21 or above.
//
// Interactive Rainbow Palette
//
// Add this script to a cube prim and add "Listen Palete" script to another Object.
// You can resize and stretch the cube, the way you want, to make it look like a color palette.
// Touch face 1 of "Rainbow Palette" to change "Listen Object" color.
//
// Modified by Rui Clary on 2011.06.20 - some corrections
// Available under the Creative Commons Attribution-ShareAlike 3.0 license
// http://creativecommons.org/licenses/by-sa/3.0/

default
{
    state_entry()
    {
        llSetObjectName("pal");
        llSetTexture ("5748decc-f629-461c-9a36-a35a221fe21f",ALL_SIDES);
        llSetTexture("5543eaa7-4283-8383-eef9-945c0b3f25c7",1);
    }
    touch(integer num_detected)
    {
         float x;
         float r;
         float g;
         float b;
         vector touchedpos = llDetectedTouchST(0);
         if (llDetectedTouchFace(0)==1)
         {
            x=360*touchedpos.x;
            r=0;
            g=0;
            b=0;
            if (x>=0&&x<=60){
                r=255;
		g=x*255/60;
            }
            if (x>60&&x<=120){
                r=255-(x-60)*255/60;
                g=255;
            }
            if (x>120&&x<=180){
                g=255;
                b=(x-120)*255/60;
            }
            if (x>180&&x<240){
                g=255-(x-180)*255/60;
                b=255;
            }
            if (x>240&&x<300){
                r=(x-240)*255/60;
                b=255;
            }
            if (x>300&&x<=360){
                r=255;
		b=255-(x-300)*255/60;
            }
                llSay(4,"<"+(string)(r/255)+","+(string)(g/255)+","+(string)(b/255)+">");
        }
    }

}
```

```lsl
// Rainbow Palette Listen Script by Rui Clary
//
// Second component of Rainbow Palette
//
// Add this script to  "Listen Object".

default
{
    state_entry()
    {
        llSetTexture ("5748decc-f629-461c-9a36-a35a221fe21f",ALL_SIDES);
        llListen( 4, "pal", NULL_KEY, "" );
    }
   listen( integer channel, string name, key id, string message )
    {
        llSetColor((vector)message,0);
    }
}
```

Modified version with fixed floats and "organized" :)

```lsl
// Bsed on Rainbow Palette by Rui Clary
//
// Modified by Jor3l Boa. Better interface and more readable :P
//
// Modified by Rui Clary on 2011.06.20 - some corrections
//
// Available under the Creative Commons Attribution-ShareAlike 3.0 license
// http://creativecommons.org/licenses/by-sa/3.0/

// devolverString -> Convert and return a vector without .0000 and other
// float things :)
devolverString(float r, float g, float b) {
    string _vector = "<";
    if(r <= 0)  {
        _vector += "0,";
    }
    else if(r == 1) {
        _vector += "1,";
    }
    else    {
        string temp = (string)r;
        while(llGetSubString(temp,llStringLength(temp)-1,-1) == "0")    {
            temp = llDeleteSubString(temp,llStringLength(temp)-1,-1);
        }
        _vector += temp+",";
    }
    //----------------
    if(g <= 0)  {
        _vector += "0,";
    }
    else if(g == 1) {
        _vector += "1,";
    }
    else    {
        string temp = (string)g;
        while(llGetSubString(temp,llStringLength(temp)-1,-1) == "0")    {
            temp = llDeleteSubString(temp,llStringLength(temp)-1,-1);
        }
        _vector += temp+",";
    }
    //----------------
    if(b <= 0)  {
        _vector += "0>";
    }
    else if(b == 1) {
        _vector += "1>";
    }
    else    {
        string temp = (string)b;
        while(llGetSubString(temp,llStringLength(temp)-1,-1) == "0")    {
            temp = llDeleteSubString(temp,llStringLength(temp)-1,-1);
        }
        _vector += temp+">";
    }
    //----------------
    llSay(0,"Color: "+_vector);
}

default
{
    state_entry()
    {
        llSetObjectName("pal");
        llSetTexture ("5748decc-f629-461c-9a36-a35a221fe21f",ALL_SIDES);
        llSetTexture("5543eaa7-4283-8383-eef9-945c0b3f25c7",1);
    }
    touch_start(integer num_detected)
    {
        float x;float r;float g;float b;
        vector touchedpos = llDetectedTouchST(0);

        if(llDetectedTouchFace(0) != 1) { return;   }
        x=360*touchedpos.x;
        r=0;
        g=0;
        b=0;
        if (x>=0&&x<=60){
            r=255;
            g=x*255/60;
        }
        if (x>60&&x<=120){
            r=255-(x-60)*255/60;
            g=255;
        }
        if (x>120&&x<=180){
            g=255;
            b=(x-120)*255/60;
        }
        if (x>180&&x<240){
            g=255-(x-180)*255/60;
            b=255;
        }
        if (x>240&&x<300){
            r=(x-240)*255/60;
            b=255;
        }
        if (x>300&&x<=360){
            r=255;
            b=255-(x-300)*255/60;
        }
        r = (r/255);
        g = (g/255);
        b = (b/255);
        //CONVERSION
        devolverString(r,g,b);
    }

}
```

In order for the above script to work as the original some corrections should be added.

Replace:

```lsl
llSay(0,"Color: "+_vector);
```

with:

```lsl
llSay(4,_vector);
```

Replace:

```lsl
touch_start
```

with:

```lsl
touch
```