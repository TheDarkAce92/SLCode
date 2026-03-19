---
name: "Minesweeper"
category: "example"
type: "example"
language: "LSL"
description: "(http://www.gnu.org/copyleft/fdl.html) in the spirit of which this script is GPL'd. Copyright (C) 2008 Xaviar Czervik"
wiki_url: "https://wiki.secondlife.com/wiki/Minesweeper"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

([http://www.gnu.org/copyleft/fdl.html](http://www.gnu.org/copyleft/fdl.html)) in the spirit of which this script is GPL'd. Copyright (C) 2008 Xaviar Czervik

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.



This is an example of a very simple minesweeper game.



Create a controller object, and drop the following script into it.

```lsl
integer size = 6;     //Size of the game 3 is a 3x3, 5 is a 5x5.
float percent = .1;    //Percentage of squares that are mines.

list mat;
list mines;
integer found;
integer rand;

showhidden(integer i) {
    if ((i+1)%size != 0) {
        llShout(rand+i+1, (string)(i+1));
    }

    if (i-1 >= 0) {
        if (i%size != 0) {
            llShout(rand+i-1, (string)(i-1));
        }
    }

    llShout(rand+i+size, (string)(i+size));

    if (i-size >= 0) {
        llShout(rand+i-size, (string)(i-size));
    }

    if (i-size+1 >= 0) {
        if ((i+1)%size != 0) {
            llShout(rand+i-size+1, (string)(i-size+1));
        }
    }

    if ((i+1)%size != 0) {
        llShout(rand+i+size+1, (string)(i+size+1));
    }

    if (i%size != 0) {
        llShout(rand+i+size-1, (string)(i+size-1));
    }

    if (i-1-size >= 0) {
        if (i%size != 0) {
            llShout(rand+i-size-1, (string)(i-size-1));
        }
    }
}

display() {
    integer i = 0;
    while (i < llGetListLength(mat)) {
        i += size;
    }
}
init() {
    rand = (integer)llFrand(100000000) + 1000;
    integer i = 0;
    while (i < size*size) {
        if (llFrand(1) < percent) {
            mat += 9;
        } else {
            mat += 0;
        }
        i += 1;
    }
    i = 0;
    while (i < size*size) {
        if (llList2Integer(mat, i) == 0) {
            integer mines = 0;

            if ((i+1)%size != 0) {
                if (llList2Integer(mat, i+1) == 9) mines++;
            }

            if (i-1 >= 0) {
                if (i%size != 0) {
                    if (llList2Integer(mat, i-1) == 9) mines++;
                }
            }

            if (llList2Integer(mat, i+size) == 9) mines++;

            if (i-size >= 0) {
                if (llList2Integer(mat, i-size) == 9) mines++;
            }

            if (i-size+1 >= 0) {
                if ((i+1)%size != 0) {
                    if (llList2Integer(mat, i-size+1) == 9) mines++;
                }
            }

            if ((i+1)%size != 0) {
                if (llList2Integer(mat, i+size+1) == 9) mines++;
            }

            if (i%size != 0) {
                if (llList2Integer(mat, i+size-1) == 9) mines++;
            }

            if (i-1-size >= 0) {
                if (i%size != 0) {
                    if (llList2Integer(mat, i-size-1) == 9) mines++;
                }
            }
            mat = llListReplaceList(mat, [mines], i, i);
        }
        i += 1;
    }
    i = 0;
    while (i < size*size) {
        integer f = i + rand;
        llRezObject("Square", llGetPos() + <-(i%size)/2.0, 2, -llFloor(i/size)/2.0>, <0,0,0>, <0,0,0,0>, f);
        llSay(f, (string)size);
        llSay(f, (string)i);
        llSay(f, (string)llList2Integer(mat, i));
        i += 1;
    }
}

default {
    state_entry() {
        llShout(-121215, "Die");
        llOwnerSay("Touch me when you finish.");
        init();
        llListen(-12, "", "", "");
        llListen(-13, "", "", "");
    }
    touch_start(integer i) {
        integer lost;
        integer i = 0;
        while (i < size*size) {
            if (llList2Integer(mat, i) == 9) {
                if (llListFindList(mines, [i]) == -1) {
                    lost = 1;
                }
            }
            i++;
        }
        i = 0;
        while (i < llGetListLength(mines)) {
            if (llList2Integer(mat, llList2Integer(mines, i)) != 9) {
                lost = 1;
            }
            i++;
        }
        if (lost)
            llOwnerSay("You lose.");
        else
            llOwnerSay("You win.");
        llShout(-121215, "Die");
    }

    listen(integer ch, string n, key id, string m) {
        if (ch == -13) {
            mines += (integer)m;
        } else if (ch == -12) {
            integer i = (integer)m;
            integer num = llList2Integer(mat, i);
            if (llListFindList(mines, [i]) != -1) {
                mines = llListReplaceList(mines, [], llListFindList(mines, [i]), llListFindList(mines, [i]));
            }
            if (num == 0)
                showhidden(i);
        }
    }
}
```

Then create an object called Square, and drop the following script in it. Then put the Square into the Controller.

```lsl
integer size;
integer num;
integer value;
integer i;
integer a;

default {
    on_rez(integer ii) {
        llListen(ii, "","", "");
        llListen(-121215, "","", "");
    }
    state_entry() {
        llSetTexture("767c7cd0-9312-0f5b-caf1-18d1b9b4d66e", ALL_SIDES);
        llOffsetTexture((6)*.077, 0, ALL_SIDES);
    }

    listen(integer ch, string s, key id, string m) {
        if (ch == -121215) {
            llDie();
        } else {
            if (i == 0) {
                size = (integer)m;
                i = 1;
            } else if (i == 1) {
                num = (integer)m;
                i = 2;
            } else if (i == 2) {
                value = (integer)m;
                llOffsetTexture((6)*.077, 0, ALL_SIDES);
                i = 3;
            } else if (i == 3) {
                i = 4;
                a = 2;
                if (value == 0)
                    llShout(-12, (string)num);
                llOffsetTexture((value-6)*.077, 0, ALL_SIDES);
            } else {
                llOffsetTexture((value-6)*.077, 0, ALL_SIDES);
            }
        }

    }
    touch_start(integer i) {
        if (a == 0) {
            llSetColor(<0,0,1>, ALL_SIDES);
            a = 1;
            llOffsetTexture((4)*.077, 0, ALL_SIDES);
        } else if (a == 1) {
            llSetColor(<1,0,0>, ALL_SIDES);
            a = 2;
            llOffsetTexture((5)*.077, 0, ALL_SIDES);
            llShout(-13, (string)num);
        } else if (a == 2) {
            llSetColor(<1,1,1>, ALL_SIDES);
            llShout(-12, (string)num);
            if (value == 9)
                llSetColor(<1,0,0>, ALL_SIDES);
            llOffsetTexture((value-6)*.077, 0, ALL_SIDES);
        }
    }
}
```