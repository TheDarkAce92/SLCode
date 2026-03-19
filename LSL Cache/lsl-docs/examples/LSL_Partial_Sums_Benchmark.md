---
name: "LSL Partial Sums Benchmark"
category: "example"
type: "example"
language: "LSL"
description: "test() { integer n = 250;"
wiki_url: "https://wiki.secondlife.com/wiki/LSL_Partial_Sums_Benchmark"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
//
//   The Computer Language Shootout
//   http://shootout.alioth.debian.org/
//
//   contributed by Isaac Gouy
//   modified by Babbage Linden
//

test()
{
  integer n = 250;

  float twothirds = 2.0/3.0;

  float a1 = 0.0;
  float a2 = 0.0;
  float a3 = 0.0;
  float a4 = 0.0;
  float a5 = 0.0;
  float a6 = 0.0;
  float a7 = 0.0;
  float a8 = 0.0;
  float a9 = 0.0;
  float alt = -1.0;

  integer k=0;
  while (n >= (++k))
  {
     float k2 = llPow(k,2);
     float k3 = k2*k;
     float sk = llSin(k);
     float ck = llCos(k);
     alt = -alt;

     a1 += llPow(twothirds,k-1);
     a2 += llPow(k,-0.5);
     a3 += 1.0/(k*(k+1.0));
     a4 += 1.0/(k3 * sk*sk);
     a5 += 1.0/(k3 * ck*ck);
     a6 += 1.0/k;
     a7 += 1.0/k2;
     a8 += alt/k;
     a9 += alt/(2.0*k -1.0);
  }

  llSay(0, (string)a1 + " (2/3)^k");
  llSay(0, (string)a2 + " k^-0.5");
  llSay(0, (string)a3 + " 1/k(k+1)");
  llSay(0, (string)a4 + " Flint Hills");
  llSay(0, (string)a5 + " Cookson Hills");
  llSay(0, (string)a6 + " Harmonic");
  llSay(0, (string)a7 + " Riemann Zeta");
  llSay(0, (string)a8 + " Alternating Harmonic");
  llSay(0, (string)a9 + " Gregory");
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