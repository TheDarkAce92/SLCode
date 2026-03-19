---
name: "Matrix Functions"
category: "example"
type: "example"
language: "LSL"
description: "list MakeMatrix(float r1c1, float r1c2, float r1c3, float r2c1, float r2c2, float r2c3, float r3c1, float r3c2, float r3c3) { return [, , ]; }"
wiki_url: "https://wiki.secondlife.com/wiki/Matrix_Functions"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

```lsl
//
// *******************************************************************************
// *******************************************************************************
//
// Developed by KyleFlynn.
//
// This is free and open source code, protected by the GPLv3 license.
// http://www.gnu.org/licenses/gpl-3.0.html
// Accepting this code is conditioned upon accepting this license.
//
//
// The following are some core linear algebra functions.
// They are primarily used to develop and use 3D transformation matrices.
// Note that ALL matrices herein are assumed to be 3x3 matrices.
// And all of these 3x3 matrices are assumed to be stored as a 3 element list of vectors.
// In all cases, the vectors are assumed to be column (not row) vectors.
//
// For all purposes herein, rows are numbered 1,2,3 and columns are also numbered 1,2,3 (both 1 based).
//
// As a last note, there are certainly faster ways to perform these function.
// However, the following imposes an excellent organization when performing
// complex 3D transformations.
//
// The available functions are:
//
//      list    MakeMatrix(float r1c1, float r1c2, float r1c3, r2c1, ...
//      float   GetMatrixElement(list m, integer row, integer col)
//      list    SetMatrixElement(list m, integer row, integer col, float value) // Returns a new matrix with the new element set.
//      list    MultMatrices(list m1, list m2)
//      list    DivideMatrices(list m1, list m2)
//      list    BackDivideMatrices(list m1, list m2)
//      list    InvertMatrix(list m)
//      list    TransposeMatrix(list m)
//      integer MatrixIsZero(list m)
//      integer MatrixIsOrthogonal(list m)
//      integer MatrixIsNormal(list m)
//
//      vector  SetVectorElement(vector v, integer row, float value) // Returns a new vector with the new element set.
//      float   GetVectorElement(vector v, integer row)
//      list    MatrixFrom3ColVectors(vector v1, vector v2, vector v3)
//      list    ZeroMatrix()
//      list    UnitMatrix()
//      vector  MakeVector(float x, float y, float z)
//      string  VectorString(vector v)          // For debugging.
//      string  MatrixString(list m)            // For debugging.
//
// *******************************************************************************
// *******************************************************************************
//

list MakeMatrix(float r1c1, float r1c2, float r1c3,
                float r2c1, float r2c2, float r2c3,
                float r3c1, float r3c2, float r3c3)
{
    return [, , ];
}

float GetMatrixElement(list m, integer row, integer col)
{
    return GetVectorElement(llList2Vector(m, col - 1), row);
}

list SetMatrixElement(list m, integer row, integer col, float value) // Returns a new matrix with the new element set.
{
    return llListReplaceList(m, [SetVectorElement(llList2Vector(m, col - 1), row, value)], col - 1, col - 1);
}

float GetVectorElement(vector v, integer row)
{
         if (row == 1) return v.x;
    else if (row == 2) return v.y;
    else if (row == 3) return v.z;
    //
    return 0;
}

vector SetVectorElement(vector v, integer row, float value) // Returns a new vector with the new element set.
{
         if (row == 1) v.x = value;
    else if (row == 2) v.y = value;
    else if (row == 3) v.z = value;
    //
    return v;
}

list ZeroMatrix()
{
    return MakeMatrix(0, 0, 0,
                      0, 0, 0,
                      0, 0, 0);
}

list UnitMatrix()
{
    return MakeMatrix(1, 0, 0,
                      0, 1, 0,
                      0, 0, 1);
}

vector MakeVector(float x, float y, float z)
{
    return ;
}

list  MatrixFrom3ColVectors(vector v1, vector v2, vector v3)
{
    return [v1, v2, v3];
}

list DivideMatrices(list m1, list m2)
{
    // In Matlab, this is equivalent to:     X = m1 / m2;
    return MultMatrices(m1, InvertMatrix(m2));
}

list BackDivideMatrices(list m1, list m2)
{
    // In Matlab, this is equivalent to:     X = m1 \ m2;
    return MultMatrices(InvertMatrix(m1), m2);
}

list MultMatrices(list m1, list m2)
{
    // A matrix generalization of the vector dot product.
    // This procedure specifically multiplies 3x3 matrices, and returns a 3x3 matrix.
    integer r1Ptr;
    integer c1Ptr;
    integer c2Ptr;
    list m3 = ZeroMatrix();
    //
    for (r1Ptr = 1; r1Ptr <= 3; r1Ptr++)
    {
        for (c2Ptr = 1; c2Ptr <=3; c2Ptr++)
        {
            for (c1Ptr = 1; c1Ptr <=3; c1Ptr++)
            {
                // This uses column ptr for row, but that's okay.
                m3 = SetMatrixElement(m3, r1Ptr, c2Ptr, GetMatrixElement(m3, r1Ptr, c2Ptr) + GetMatrixElement(m1, r1Ptr, c1Ptr) * GetMatrixElement(m2, c1Ptr, c2Ptr));
            }
        }
    }
    //
    return m3;
}

list InvertMatrix(list m)
{
    // Don't forget that InvertMatrix(m)=TransposeMatrix(m) if m is orthonormal.
    // And TransposeMatrix(m) would be much faster.
    //
    // This ONLY works with 3x3 matrices.
    integer rPtr;
    integer cPtr;
    integer ptr;
    integer rPtr2;
    integer cPtr2;
    float PivotMax;
    float dNorm;
    float dSwap;
    integer swpCnt;
    //
    for (ptr = 1; ptr <= 3; ptr++)
    {
        // Search max pivot.
        rPtr2 = ptr;
        cPtr2 = ptr;
        PivotMax = 0;
        for (rPtr = ptr; rPtr <= 3; rPtr++)
        {
            for (cPtr = ptr; cPtr <= 3; cPtr++)
            {
                if (llFabs(GetMatrixElement(m, rPtr, cPtr)) > PivotMax)
                {
                    rPtr2 = rPtr;
                    cPtr2 = cPtr;
                    PivotMax = llFabs(GetMatrixElement(m, rPtr, cPtr));
                }
            }
        }
        // Swap rows and columns.
        if (rPtr2 > ptr)
        {
            // Swap row.
            for (cPtr = 1; cPtr <= 3; cPtr++)
            {
                dSwap = GetMatrixElement(m, rPtr2, cPtr);
                m = SetMatrixElement(m, rPtr2, cPtr, GetMatrixElement(m, ptr, cPtr));
                m = SetMatrixElement(m, ptr, cPtr, dSwap);
            }
            swpCnt++;
            SetSwapDiag(swpCnt, 1, ptr);
            SetSwapDiag(swpCnt, 2, rPtr2);
            SetSwapDiag(swpCnt, 3, 1);
        }
        if (cPtr2 > ptr)
        {
            // Swap column.
            for (rPtr = 1; rPtr <= 3; rPtr++)
            {
                dSwap = GetMatrixElement(m, rPtr, cPtr2);
                m = SetMatrixElement(m, rPtr, cPtr2, GetMatrixElement(m, rPtr, ptr));
                m = SetMatrixElement(m, rPtr, ptr, dSwap);
            }
            swpCnt++;
            SetSwapDiag(swpCnt, 1, ptr);
            SetSwapDiag(swpCnt, 2, cPtr2);
            SetSwapDiag(swpCnt, 3, 2);
        }
        //
        // Check pivot 0.
        if (llFabs(GetMatrixElement(m, ptr, ptr)) <= 0)
        {
            llSay(DEBUG_CHANNEL, "Matrix inversion error, script is stopped.");
            rPtr = 1 / 0; // Crash the script.
        }
        //
        // Normalization.
        dNorm = GetMatrixElement(m, ptr, ptr);
        m = SetMatrixElement(m, ptr, ptr, 1);
        for (cPtr = 1; cPtr <= 3; cPtr++)
        {
            m = SetMatrixElement(m, ptr, cPtr, GetMatrixElement(m, ptr, cPtr) / dNorm);
        }
        // Linear reduction.
        for (rPtr = 1; rPtr <= 3; rPtr++)
        {
            if (rPtr != ptr && GetMatrixElement(m, rPtr, ptr) != 0)
            {
                dNorm = GetMatrixElement(m, rPtr, ptr);
                m = SetMatrixElement(m, rPtr, ptr, 0);
                for (cPtr = 1; cPtr <= 3; cPtr++)
                {
                    m = SetMatrixElement(m, rPtr, cPtr, GetMatrixElement(m, rPtr, cPtr) - dNorm * GetMatrixElement(m, ptr, cPtr));
                }
            }
        }
    }
    //
    // Un-Scramble rows.
    for (ptr = swpCnt; ptr >= 1; ptr--)
    {
        if (GetSwapDiag(ptr, 3) == 1)
        {
            // Swap column.
            for (rPtr = 1; rPtr <=3; rPtr++)
            {
                dSwap = GetMatrixElement(m, rPtr, GetSwapDiag(ptr, 2));
                m = SetMatrixElement(m, rPtr, GetSwapDiag(ptr, 2), GetMatrixElement(m, rPtr, GetSwapDiag(ptr, 1)));
                m = SetMatrixElement(m, rPtr, GetSwapDiag(ptr, 1), dSwap);
            }
        }
        else if (GetSwapDiag(ptr, 3) == 2)
        {
            // Swap row.
            for (cPtr = 1; cPtr <= 3; cPtr++)
            {
                dSwap = GetMatrixElement(m, GetSwapDiag(ptr, 2), cPtr);
                m = SetMatrixElement(m, GetSwapDiag(ptr, 2), cPtr, GetMatrixElement(m, GetSwapDiag(ptr, 1), cPtr));
                m = SetMatrixElement(m, GetSwapDiag(ptr, 1), cPtr, dSwap);
            }
        }
    }
    //
    return m;
}

list TransposeMatrix(list m)
{
    list m2 = ZeroMatrix();
    //
    m2 = SetMatrixElement(m2, 1, 2, GetMatrixElement(m, 2, 1));
    m2 = SetMatrixElement(m2, 1, 3, GetMatrixElement(m, 3, 1));
    m2 = SetMatrixElement(m2, 2, 1, GetMatrixElement(m, 1, 2));
    m2 = SetMatrixElement(m2, 2, 3, GetMatrixElement(m, 3, 2));
    m2 = SetMatrixElement(m2, 3, 1, GetMatrixElement(m, 1, 3));
    m2 = SetMatrixElement(m2, 3, 2, GetMatrixElement(m, 2, 3));
    //
    // Don't need to transpose the diagonal elements.
    m2 = SetMatrixElement(m2, 1, 1, GetMatrixElement(m, 1, 1));
    m2 = SetMatrixElement(m2, 2, 2, GetMatrixElement(m, 2, 2));
    m2 = SetMatrixElement(m2, 3, 3, GetMatrixElement(m, 3, 3));
    //
    return m2;
}

integer MatrixIsZero(list m)
{
    return (GetMatrixElement(m, 1, 1) == 0 && GetMatrixElement(m, 2, 1) == 0 && GetMatrixElement(m, 3, 1) == 0 &&
            GetMatrixElement(m, 1, 2) == 0 && GetMatrixElement(m, 2, 2) == 0 && GetMatrixElement(m, 3, 2) == 0 &&
            GetMatrixElement(m, 1, 3) == 0 && GetMatrixElement(m, 2, 3) == 0 && GetMatrixElement(m, 3, 3) == 0);
}

integer MatrixIsOrthogonal(list m)
{
    float epsilon = .00002; // Our allowed tolerance.
    //
    vector v1 = llList2Vector(m, 0);
    vector v2 = llList2Vector(m, 1);
    vector v3 = llList2Vector(m, 2);
    //
    return llFabs(llFabs(llRot2Angle(llRotBetween(v1, v2))) - 90) < epsilon &&
           llFabs(llFabs(llRot2Angle(llRotBetween(v1, v3))) - 90) < epsilon &&
           llFabs(llFabs(llRot2Angle(llRotBetween(v2, v3))) - 90) < epsilon;
}

integer MatrixIsNormal(list m)
{
    float epsilon = .00002; // Our allowed tolerance.
    //
    vector v1 = llList2Vector(m, 0);
    vector v2 = llList2Vector(m, 1);
    vector v3 = llList2Vector(m, 2);
    //
    return llFabs(v1.x * v1.x + v1.y * v1.y + v1.z * v1.z - 1) < epsilon &&
           llFabs(v2.x * v2.x + v2.y * v2.y + v2.z * v2.z - 1) < epsilon &&
           llFabs(v3.x * v3.x + v3.y * v3.y + v3.z * v3.z - 1) < epsilon;
}

string VectorString(vector v)
// Primarily used for debugging purposes.
{
    return "[ " + Float2StringFormat(v.x, 5, TRUE) + ", " + Float2StringFormat(v.y, 5, TRUE) + ", " + Float2StringFormat(v.z, 5, TRUE) + " ]";
}

string MatrixString(list m)
// Primarily used for debugging purposes.
{
    return "\n[ " + Float2StringFormat(GetMatrixElement(m, 1, 1), 5, TRUE) + ", " + Float2StringFormat(GetMatrixElement(m, 1, 2), 5, TRUE) + ", " + Float2StringFormat(GetMatrixElement(m, 1, 3), 5, TRUE) + " ;" + "\n" +
             "  " + Float2StringFormat(GetMatrixElement(m, 2, 1), 5, TRUE) + ", " + Float2StringFormat(GetMatrixElement(m, 2, 2), 5, TRUE) + ", " + Float2StringFormat(GetMatrixElement(m, 2, 3), 5, TRUE) + " ;" + "\n" +
             "  " + Float2StringFormat(GetMatrixElement(m, 3, 1), 5, TRUE) + ", " + Float2StringFormat(GetMatrixElement(m, 3, 2), 5, TRUE) + ", " + Float2StringFormat(GetMatrixElement(m, 3, 3), 5, TRUE) + " ]";
}

string Float2StringFormat(float num, integer places, integer rnd)
// Allows string output of a float in a tidy text format.
// rnd (rounding) should be set to TRUE for rounding, FALSE for no rounding
{
    if (rnd)
    {
        float f = llPow(10.0, places);
        integer i = llRound(llFabs(num) * f);
        string s = "00000" + (string)i; // Number of 0s is (value of max places - 1).
        if (num < 0.0) return "-" + (string)( (integer)(i / f) ) + "." + llGetSubString(s, -places, -1);
        return (string)((integer)(i / f)) + "." + llGetSubString(s, -places, -1);
    }
    if (!places) return (string)((integer)num );
    if ((places = (places - 7 - (places < 1))) & 0x80000000) return llGetSubString((string)num, 0, places);
    return (string)num;
}

// These globals are just used in SetSwapDiag & GetSwapDiag, which are used only in InvertMatrix.
// They emulate a 6x3 array of integers.
integer iSwapDiag11;
integer iSwapDiag21;
integer iSwapDiag31;
integer iSwapDiag41;
integer iSwapDiag51;
integer iSwapDiag61;
integer iSwapDiag12;
integer iSwapDiag22;
integer iSwapDiag32;
integer iSwapDiag42;
integer iSwapDiag52;
integer iSwapDiag62;
integer iSwapDiag13;
integer iSwapDiag23;
integer iSwapDiag33;
integer iSwapDiag43;
integer iSwapDiag53;
integer iSwapDiag63;
//

SetSwapDiag(integer i, integer j, integer value)
// Just used for the InvertMatrix function.
{
         if (i == 1)
    {
             if (j == 1) iSwapDiag11 = value;
        else if (j == 2) iSwapDiag12 = value;
        else if (j == 3) iSwapDiag13 = value;
    }
    else if (i == 2)
    {
             if (j == 1) iSwapDiag21 = value;
        else if (j == 2) iSwapDiag22 = value;
        else if (j == 3) iSwapDiag23 = value;
    }
    else if (i == 3)
    {
             if (j == 1) iSwapDiag31 = value;
        else if (j == 2) iSwapDiag32 = value;
        else if (j == 3) iSwapDiag33 = value;
    }
    else if (i == 4)
    {
             if (j == 1) iSwapDiag41 = value;
        else if (j == 2) iSwapDiag42 = value;
        else if (j == 3) iSwapDiag43 = value;
    }
    else if (i == 5)
    {
             if (j == 1) iSwapDiag51 = value;
        else if (j == 2) iSwapDiag52 = value;
        else if (j == 3) iSwapDiag53 = value;
    }
    else if (i == 6)
    {
             if (j == 1) iSwapDiag61 = value;
        else if (j == 2) iSwapDiag62 = value;
        else if (j == 3) iSwapDiag63 = value;
    }
}

integer GetSwapDiag(integer i, integer j)
// Just used for the InvertMatrix function.
{
    integer i1;
    integer i2;
    integer i3;
    //
         if (i == 1) { i1 = iSwapDiag11; i2 = iSwapDiag12; i3 = iSwapDiag13; }
    else if (i == 2) { i1 = iSwapDiag21; i2 = iSwapDiag22; i3 = iSwapDiag23; }
    else if (i == 3) { i1 = iSwapDiag31; i2 = iSwapDiag32; i3 = iSwapDiag33; }
    else if (i == 4) { i1 = iSwapDiag41; i2 = iSwapDiag42; i3 = iSwapDiag43; }
    else if (i == 5) { i1 = iSwapDiag51; i2 = iSwapDiag52; i3 = iSwapDiag53; }
    else if (i == 6) { i1 = iSwapDiag61; i2 = iSwapDiag62; i3 = iSwapDiag63; }
    //
         if (j == 1) return i1;
    else if (j == 2) return i2;
    else if (j == 3) return i3;
    return 0; // Needed for compiler.
}

default
{
    on_rez(integer iStartParam)
    {
        llResetScript();
    }
    state_entry()
    {

        list m1;
        list m2;
        list m3;
        list m4;
        //
        m1 = MakeMatrix(1,2,3,4,5,6,7,8,9);
        m2 = MakeMatrix(2.2, 3.3, 4.4,
                        5.5, 6.6, 5.5,
                        4.4, 3.2, 2.1);
        m3 = MultMatrices(m1, m2);
        llSay(0, MatrixString(m3));

        m4 = DivideMatrices(m3, m2);
        llSay(0, MatrixString(m4)); // m4 should take us back to m1.

        // With the above, the MultMatrices and DivideMatrices functions are tested,
        // along with InvertMatrix via divide.  This is the core of these procedures.




    }
    touch_start(integer iNumDetected)
    {
    }
    timer()
    {
    }
}
```