---
name: "LSL Recursion Benchmark"
category: "example"
type: "example"
language: "LSL"
description: "integer ack(integer x, integer y) { if(x == 0) { return y + 1; }"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Recursion_Benchmark"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
//
// The Computer Language Shootout
// http://shootout.alioth.debian.org/
//
// contributed by bearophile, Jan 24 2006
// modified by Babbage Linden, Oct 10 2007
//

integer ack(integer x, integer y)
{
  if(x == 0)
  {
    return y + 1;
  }

  if(y)
  {
    return ack(x - 1, ack(x, y - 1));
  }
  else
  {
    return ack(x - 1, 1);
  }
}

integer fib(integer n)
{
  if (n < 2)
  {
    return 1;
  }
  return fib(n - 2) + fib(n - 1);
}

float fibFP(float n)
{
  if (n < 2.0)
  {
    return 1.0;
  }
  return fibFP(n - 2.0) + fibFP(n - 1.0);
}

integer tak(integer x, integer y, integer z)
{
  if (y < x)
  {
    return tak(tak(x - 1, y, z), tak(y - 1, z, x), tak(z - 1, x, y));
  }
  return z;
}

float takFP(float x, float y, float z)
{
    if (y < x)
    {
        return takFP( takFP(x-1.0, y, z), takFP(y-1.0, z, x), takFP(z-1.0, x, y) );
    }
    return z;
}

test()
{
  integer n = 3;
  llSay(0, "Ack(3," + (string)(n+1) + "): " + (string)(ack(3, n+1)));
  //llSay(0, "Fib("+ (string)(28.0 + n) + "): " + (string)(fibFP(28.0+n)));

  llSay(0, "Tak(" + (string)(3 * n) + "," + (string)(2 * n) + "," + (string)n + "): " + (string)tak(3*n, 2*n, n));

  llSay(0, "Fib(3): " + (string)fib(3));
  llSay(0, "Tak(3.0,2.0,1.0): " + (string)takFP(3.0, 2.0, 1.0));
}

time()
{
    llResetTime();
    llSay(0, "Starting tests...");
    test();
    llSay(0, "Finished tests in " + (string)llGetTime() + "s");

}

default
{
    state_entry()
    {
        time();
    }

    touch_start(integer num)
    {
        time();
    }
}
```