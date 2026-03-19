---
name: "Pseudo Random Number Generator"
category: "example"
type: "example"
language: "LSL"
description: "Generating random values can be useful in many applications, however all we are supplied with in LSL is a relatively inflexible floating-point number generator."
wiki_url: "https://wiki.secondlife.com/wiki/Pseudo_Random_Number_Generator"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Description

Generating random values can be useful in many applications, however all we are supplied with in LSL is a relatively inflexible floating-point number generator.

To this end I set-out to create a more useful random number generator based on a [Mersenne Twister](http://en.wikipedia.org/wiki/Mersenne_Twister) [Pseudo Random Number Generator](http://en.wikipedia.org/wiki/Pseudorandom_number_generator) (PRNG). The implementation in LSL uses a much smaller state of only four values, however it gives much the same distribution as the standard implementation which uses an array of some 624 values as its state, which of course is unfeasible to implement in LSL.

Usage

Usage is relatively simple, and this library comes with some helper methods so that you can quickly generate random LSL integer, float, and key values, providing a seed to help generate them even more randomly. If you use this PRNG to aid in communications between objects, then you must ensure they use the same seed value(s), thus an algorithm for determining these will be required, but could be as simple as a counter for each message sent/received.

The only methods you are ever likely to use are:

`integer lslPRNGRandomInteger(integer seed)`

Generates a pseudo-random integer using the given `seed`.

`float lslPRNGRandomFloat(integer seed)`

Generates a pseudo-random float with range [0.0, 1.0) using the given `seed`.

`key lslPRNGRandomKey(integer seed)`

Generates a pseudo-random key using the given `seed`.

`string lslIntegerToHex(integer i)`

Allows you to output an integer value as hex, useful for Cryptography.

Script

```lsl
integer lslPRNGState0       = 0;
integer lslPRNGState1       = 0;
integer lslPRNGState2       = 0;
integer lslPRNGState3       = 0;

integer lslPRNGPosition     = 0;
integer lslPRNGSeed         = 0;

integer lslPRNGTwiddle(integer a, integer b) {
    integer c = (((a & 0x80000000) | (b & 0x7FFFFFFF)) >> 1);
    if (b & 1) c = c ^ 0x9908B0DF;
    return c;
}

lslPRNGGenState() {
    lslPRNGState0 = lslPRNGState2 ^
        lslPRNGTwiddle(lslPRNGState0, lslPRNGState1);
    lslPRNGState1 = lslPRNGState1 ^
        lslPRNGTwiddle(lslPRNGState1, lslPRNGState2);
    lslPRNGState2 = lslPRNGState0 ^
        lslPRNGTwiddle(lslPRNGState2, lslPRNGState3);
    lslPRNGState3 = lslPRNGState3 ^
        lslPRNGTwiddle(lslPRNGState3, lslPRNGState0);
    lslPRNGPosition = 0;
}

lslPRNGGenStateSeed(integer seed) {
    lslPRNGState0 = seed;
    lslPRNGState1 = 1812433253 *
        (lslPRNGState0 ^ (lslPRNGState0 >> 30)) + 1;
    lslPRNGState2 = 1812433253 *
        (lslPRNGState1 ^ (lslPRNGState1 >> 30)) + 2;
    lslPRNGState3 = 1812433253 *
        (lslPRNGState2 ^ (lslPRNGState2 >> 30)) + 3;
    lslPRNGPosition = 4;
}

integer lslPRNGRandomInteger(integer seed) {
    if (seed != lslPRNGSeed) {
        lslPRNGGenStateSeed(seed);
        lslPRNGSeed = seed;

        lslPRNGGenState();
    } else if (lslPRNGPosition >= 4) lslPRNGGenState();

    integer x;
    if (lslPRNGPosition == 0)      x = lslPRNGState0;
    else if (lslPRNGPosition == 1) x = lslPRNGState1;
    else if (lslPRNGPosition == 2) x = lslPRNGState2;
    else if (lslPRNGPosition == 3) x = lslPRNGState3;
    ++lslPRNGPosition;

    x = x ^ ((x >> 11) & 0x001FFFFF);
    x = x ^ ((x << 7) & 0x9D2C5680);
    x = x ^ ((x << 15) & 0xEFC60000);
    return x ^ ((x >> 18) & 0x00002FFF);
}

// Returns a random float between 0.0 (inclusive) and 1.0 (exclusive)
float lslPRNGRandomFloat(integer seed) {
    integer t = lslPRNGRandomInteger(seed);
    if (t < 0) t = -t;
    integer b = lslPRNGRandomInteger(seed);
    if (b < 0) b = -b;
    else if (b == 0) return 0.0;

    t %= b;
    return (float)t / (float)b;
}

// Returns a completely random key
key lslPRNGRandomKey(integer seed) {
    string k = lslIntegerToHexFast(lslPRNGRandomInteger(seed)) +
        lslIntegerToHexFast(lslPRNGRandomInteger(seed)) +
        lslIntegerToHexFast(lslPRNGRandomInteger(seed)) +
        lslIntegerToHexFast(lslPRNGRandomInteger(seed));

    return (key)llInsertString(
        llInsertString(
            llInsertString(
                llInsertString((k = "") + k, 8,"-"),
                13,
                "-"
            ),
            18,
            "-"
        ),
        23,
        "-"
    );
}

string lslIntegerToHexFast(integer int) {
	string hex = "";
	{
		integer shift = 32; integer nybble; string char = "";
		while (shift >= 4) {
			nybble = (int >> (shift -= 4)) & 0xF;
			if (nybble > 7) {
				if (nybble > 11) {
					if (nybble > 13) {
						if (nybble > 14) char = "f";	// 15
						else char = "e";				// 14
					} else {
						if (nybble > 12) char = "d";	// 13
						else char = "c";				// 12
					}
				} else {
					if (nybble > 9) {
						if (nybble > 10) char = "b";	// 11
						else char = "a";				// 10
					} else {
						if (nybble > 8) char = "9";		// 9
						else char = "8";				// 8
					}
				}
			} else {
				if (nybble > 3) {
					if (nybble > 5) {
						if (nybble > 6) char = "7";		// 7
						else char = "6";				// 6
					} else {
						if (nybble > 4) char = "5";		// 5
						else char = "4";				// 4
					}
				} else {
					if (nybble > 1) {
						if (nybble > 2) char = "3";		// 3
						else char = "2";				// 2
					} else {
						if (nybble > 0) char = "1";		// 1
						else char = "0"; // 0
					}
				}
			}

			if (char != "") hex += char;
		}
	}
	if (hex == "") hex = "0";
	return (hex = "") + hex;
}

default {
    state_entry() {
        integer seed = llGetUnixTime();
        llOwnerSay("Seed = "+(string)seed);
        llOwnerSay("Random integer = "+(string)lslPRNGRandomInteger(seed));
        llOwnerSay("Random float = "+(string)lslPRNGRandomFloat(seed));
        llOwnerSay("Random key = "+(string)lslPRNGRandomKey(seed));
    }
}
```