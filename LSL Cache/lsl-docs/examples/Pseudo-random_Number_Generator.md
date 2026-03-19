---
name: "Pseudo-random Number Generator"
category: "example"
type: "example"
language: "LSL"
description: "See also: llFrand, llListRandomize, Seedable_PRNG"
wiki_url: "https://wiki.secondlife.com/wiki/Pseudo-random_Number_Generator"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

See also: llFrand, llListRandomize, Seedable_PRNG

- 1 Seedable PRNG Based On Multiply/ Add/ Overflow
- 2 Conventional Linear Congruential Seedable PRNG Based On Multiply/ Add/ Overflow
- 3 Seedable PRNG Based On MD5 Hashing
- 4 Minimal XORshift PRNG

## Seedable PRNG Based On Multiply/ Add/ Overflow

Here's a Pseudo-random Number Generator - I (Xaviar Czervik) just made it up off the top of my head - so it has no mathematical research behind it to prove it's random... I've tested it for a while and it looks random to me, about the same as llFrand(). But what ever. Sue me. The main reason that I use it so that I can test scripts, and then when it blows up because of a math error, I can just run the script again an it will use the same numbers, in the same order.

I use this for determining a random channel for two (or more) objects to talk on. This allows the scripts to talk without users being able to intercept the messages - and even if they do - then the channel will change in a minute or two - so no harm done.



```lsl
// IMPORTANT: Change the following numbers before using!
integer seed1 = 0x053FA20C;
integer seed2 = 0x3B1264D5;
integer seed1Mod = 0x71B5F252;
integer seed2Mod = 0x56A0E61D;

integer rand(integer spread) {
    	seed1 = (seed1 * seed1Mod + 0xB);
    	seed2 = (seed2 * seed2Mod + 0xB);
        seed2Mod = seed1Mod;
        seed1Mod = seed1 * seed2;
	return seed1Mod % spread;
}
```

The below code is exactly the same as the above, only it is much faster. Thanks to Strife Onizuka.

```lsl
integer rand(integer spread) {
    	seed2 = (seed2 * seed2Mod + 0xB);
	return (seed1Mod = ((seed1 = (seed1 * (seed2Mod = seed1Mod) + 0xB)) * seed2)) % spread;
}
```

Example code to test the randomness (Is that a word?) of the generator.

```lsl
default {
	state_entry() {
		integer i = 0;
		integer min = 0x7FFFFFFF;
		integer max = -0x7FFFFFFF;
		integer total = 0;
		while (i < 100000000) {
			integer r = rand(0x7FFFFFFF);
			if (r < min) {
				min = r;
			}
			if (r > max) {
				max = r;
			}
			total += r;
			i++;
		}
		llOwnerSay("Min: " + (string)min);
		llOwnerSay("Max: " + (string)max);
		llOwnerSay("Average: " + (string)(total/100000000));

	}
}
```

Note: A pattern of digits like yyyymmddnn often works as a seed that changes often enough, *e.g.*, test with 2007090103 == 2,007,090,103 as the 3rd try of the 1st day of the 9th month of the 2007th year, except you must take care to avoid confusing yourself with integers larger than the 2,147,483,647 limit of 32-bit signed arithmetic.

## Conventional Linear Congruential Seedable PRNG Based On Multiply/ Add/ Overflow

Note: Google Groups sci.math cites Knuth & Lewis suggesting the following linear congruential generator for 32-bit arithmetic processors. Someone skilled in the relevant mathematics should be able to prove that these choices of multiplier and addend provides results that feel more random. Someone skilled in Google might find yet more popular choices than these. People say the choose function returning the quotient rather than the remainder matters: try counting odd results and even results from the pseudorandom() routine to see why.

```lsl
integer seed = 2007090103;

integer pseudorandom()
{
    seed = 1664525 * seed + 1013904223;
    return seed;
}

integer choose(integer count)
{
    integer nonnegative = 0x7fffFFFF;
    integer choice = pseudorandom() & nonnegative;
    return ((choice / (nonnegative / count)) % count);
}

default
{
    state_entry()
    {
        string line;
        integer index;

        line = "";
        for (index = 0; index < 9; ++index)
        {
           line += " " + (string) pseudorandom();
        }
        llOwnerSay(line);

        line = "";
        for (index = 0; index < 30; ++index)
        {
           line += " " + (string) (1 + choose(6));
        }
        llOwnerSay(line);

        llOwnerSay("OK");
    }
}
```

## Seedable PRNG Based On MD5 Hashing

I haven't noticed any irregular behavior in this one, i would love to know what you guys think - Kyrah Abattoir

```lsl
string seed = "";//Any String you want as your initial seed.

//this version will pull a random int from 0 to max int
integer NextInt()
{
	seed = llMD5String(seed,0);
	integer value = (integer)("0x"+llGetSubString(seed,0,6));
	return value;
}

//This one will limit the result from 0 to the range indicated
integer NextIntClamped(integer max)
{
	max++;
	seed = llMD5String(seed,0);
	integer value = (integer)("0x"+llGetSubString(seed,0,6))%max;
	return value;
}

//0 to 1 duh.
integer NextBool()
{
	return NextIntClamped(1);
}
```

I think MD5 random is just fine. I did some testing with ent and dieharder (random number test suites) based on recursed md5 'random' and it seems to have superior pseudo-random-number charactaristics. The only drawback is the decreased performance, which is usually (for games etc) not an issue at all.
My version (below) added a little extra entropy using timestamps. You could inject other sources of entropy as well. Tano Toll Tano Toll

```lsl
string md5="seed";
integer rnd() {
    //add in more entropy if you like, like touch position (detectedtouchST etc).
    //however, seeding the md5 with itself is already quite sufficient
    md5=llMD5String(md5+(string)llGetUnixTime()+(string)llGetTime(), 0x5EED);
    return (integer)("0x"+llGetSubString(md5,0,7));
}

float frnd (float max) {
    //this suffers a few bit rounding errors
    return llFabs(max * rnd()/0x80000000);
}
```

```lsl
$ ent random.outmd5
Entropy = 7.999961 bits per byte.

Optimum compression would reduce the size
of this 4222048 byte file by 0 percent.

Chi square distribution for 4222048 samples is 231.03, and randomly
would exceed this value 75.00 percent of the times.

Arithmetic mean value of data bytes is 127.4654 (127.5 = random).
Monte Carlo value for Pi is 3.140641831 (error 0.03 percent).
Serial correlation coefficient is 0.000047 (totally uncorrelated = 0.0).
```

## Minimal XORshift PRNG

XOR and bit shifts are highly efficient in LSL, so a XORshift generator is very simple and offers high performance, though is not very random as it simply cycles through all integers in a random-seeming order.

```lsl
// Minimal 32-bit XORshift PRNG, with a period of 2^32-1, i.e. cycles through every integer value except 0
// Usage:
// - Set xs_rnd to a desired start value
// - Call xorshift() to advance the PRNG and get current value
// Source: https://www.jstatsoft.org/article/view/v008i14

// Must not be 0
integer xs_rnd = 0x1673eec0;

integer xorshift() {
    integer t = xs_rnd; t = t ^ (t<<13); t = t ^ (t>>17); t = t ^ (t<<5); xs_rnd = t;
    return xs_rnd;
}

default
{
    state_entry() {
        xs_rnd = 0xaaaaaaaa;
        llOwnerSay((string)xorshift()); // 180213
        llOwnerSay((string)xorshift()); // -1468353173
        llOwnerSay((string)xorshift()); // 606956032
    }
}
```