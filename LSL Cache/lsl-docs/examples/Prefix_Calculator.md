---
name: "Prefix Calculator"
category: "example"
type: "example"
language: "LSL"
description: "Created by Xaviar Czervik. Do whatever you wish with this function: Sell it (good luck), use it, or modify it."
wiki_url: "https://wiki.secondlife.com/wiki/Prefix_Calculator"
author: "Xaviar Czervik"
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Prefix Calculator

Created by Xaviar Czervik. Do whatever you wish with this function: Sell it (good luck), use it, or modify it.

Evaluates an expression in prefix notation. I will give a few examples, and let you figure it out yourself. You have a brain: use it.

+ 1 2 = 3

+ - 1 2 3 = 2

/ + 3 2 - +1 2 3 = 1.25



For more information visit [http://en.wikipedia.org/wiki/Prefix_notation](http://en.wikipedia.org/wiki/Prefix_notation).

Another prefix calculator script is the Chatbot sample. That script is much less simple, because it handles many more varieties of input, but that script exhibits essentially this same control flow.



```lsl
list stack;

push(float i) { // Float To Integer - Not good to use for large values, but it works. Sue me...

    stack += (integer)(i*10000000);
}

float pop() {
    float i = peek();
    stack = llList2List(stack, 0, -2);
    return i;
}

float peek() { // Float To Integer - Not good to use for large values, but it works. Sue me...

    return ((float)llList2Integer(stack, -1))/10000000;
}

default {
    state_entry() {
        llListen(0, "", llGetOwner(), "");
    }
    listen(integer i, string n, key id, string m) {
        string data = m;

        list parsed = llParseString2List(data, [" "], []);

        integer i = llGetListLength(parsed);
        while (i--) {
            string data = llList2String(parsed, i);
            string check = (string)((float)data);
            while (llGetSubString(check, -1, -1) == "0") {
                check = llGetSubString(check, 0, -2);
            }
            if (llGetSubString(check, -1, -1) == ".")
                check = llGetSubString(check, 0, -2);
            if (check == data) { // Is it a number?
                push((float)data);
            } else {
                if (llStringLength(data) == 1) {
                    float first = pop();
                    float second = pop();
                    if (data == "+") {
                        push(first + second);
                    }
                    if (data == "-") {
                        push(first - second);
                    }
                    if (data == "*") {
                        push(first * second);
                    }
                    if (data == "/") {
                        push((float)first / (float)second);
                    }
                } else {
                    float first = pop();
                    if (data == "sin") {
                        push(llSin(first));
                    }
                    if (data == "cos") {
                        push(llCos(first));
                    }
                    if (data == "tan") {
                        push(llTan(first));
                    }
                    if (data == "sqrt") {
                        push(llSqrt(first));
                    }
                }
            }
        }
        llOwnerSay((string)pop());
    }
}
```