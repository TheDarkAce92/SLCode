---
name: "Random Gaussian Number Generator"
category: "example"
type: "example"
language: "LSL"
description: "Port of the Random Gaussian algorithm found on http://www.taygeta.com/random/gaussian.html."
wiki_url: "https://wiki.secondlife.com/wiki/Random_Gaussian_Number_Generator"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Port of the Random Gaussian algorithm found on [http://www.taygeta.com/random/gaussian.html](http://www.taygeta.com/random/gaussian.html).

```lsl
float randGauss(float mean, float stdev){
    float x, y, r2;
    do{//Generate a point in a unit circle that is not zero.
        x = llFrand(2.) - 1;
        y = llFrand(2.) - 1;
        r2 = x * x + y * y;
    } while (r2 > 1.0 || r2 == 0);

    //Box-Muller transformation
    return mean + x * stdev * llSqrt( -2 * llLog(r2) / r2);
}
```

```lsl
vector randGaussPair(vector center, float stdev){//2D
    //returns a random point on the x/y plain with a specified standard deviation from center.
    float r2;
    vector p;
    do{//Generate a point in a unit circle that is not zero.
        p = ;
        r2 = p * p;//dot product
    } while (r2 > 1.0 || r2 == 0);

    //Box-Muller transformation
    return center + (p * (stdev * llSqrt( -2 * llLog(r2) / r2)));
}
```

## Box-Muller Transformation

The Box-Muller transformation is used to adjust the magnitude of the vector, remapping it to a standard deviation.

## 3D

Is this correct? Or does Box-Muller need to be adjusted?

```lsl
vector randGaussPoint(vector center, float stdev){//3D
    //returns a random point with a specified standard deviation from center?
    float r2;
    vector p;
    do{//Generate a point in a unit sphere that is not zero.
        p = ;
        r2 = p * p;//dot product
    } while (r2 > 1.0 || r2 == 0);

    //Box-Muller transformation
    return center + (p * (stdev * llSqrt( -2 * llLog(r2) / r2)));
}
```