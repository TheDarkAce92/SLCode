---
name: "2D Pseudo-Array"
category: "example"
type: "example"
language: "LSL"
description: "Many times it is useful to work with multi-dimensional arrays. While LSL does not provide us with this functionality directly, it is possible to obtain the same behavior using a set of very simple algorithms."
wiki_url: "https://wiki.secondlife.com/wiki/2D_Pseudo-Array"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Many times it is useful to work with multi-dimensional arrays.  While LSL does not provide us with this functionality directly, it is possible to obtain the same behavior using a set of very simple algorithms.

A list is defined as “a heterogeneous list of the other data types”.  It is linear by nature and can be thought of as a single column.

At the physical level, arrays are stored in contiguous sections of memory. (Another linear structure)  An algorithm is used to translate between the logical rows and columns and the physical level of addresses.

Consider a list with 24 elements.  Normally we visualize this as a vertical column.
In this case, it is convenient to think of them as 4 rows and 6 columns.

Notice we are starting with element 1.  Element zero is reserved for storing the size of the array.

     **0****1****2****3****4****5**
    **0** 1 2 3 4 5 6
    **1** 7 8 9101112
    **2**131415161718
    **3**192021222324

**Figure 1.**  Indexes of a list arranged in rows and columns.

**Our addressing algorithm can use the following formula: index = row * cols + col + 1 Where:**

- row is the row number of the element
- cols is the number of columns in the array
- col is the column number of the element

**Example:** Find the index for the data stored in row 3 and column 4.

- index = row * cols + col + 1
- index = 3 * 6 + 4 + 1
- index = 23



We will implement this in a set of functions.  These functions raise the level of abstraction and give us the ability to manipulate arrays referencing rows and columns.

Sandie



## LSL Implementation:

```lsl
//-----------------------------------------------------------------------------
// Script: IntegerArrayExample
// Description:
//      Example implementation of a 2-dimensional array of integers
//
// Written By: Sandie Harbour, July 2008
//-----------------------------------------------------------------------------

//------------------------------------------------------------------------------
// Function: initIntArray
// Descripton:
//      Given the number of rows and columns, create an list of integers
//      that will be used as an aarray.
//------------------------------------------------------------------------------
list makeArray ( integer rows, integer cols )
{
    integer i;
    list array = [];
    array += < rows, cols, 0 >;
    for (i=0; i < rows * cols; ++i)
    {
        array += 0;
    }
    return array;
}

//------------------------------------------------------------------------------
// Function: getElement
// Descripton:
//      Return the integer which is stored in the given array
//      at the given row and column numbers.
//------------------------------------------------------------------------------
integer getElement( list array, integer row, integer col )
{
    vector metadata = llList2Vector( array, 0);
    integer cols = (integer)metadata.y;
    integer index = row * cols + col + 1;
    return llList2Integer( array, index);
}

//------------------------------------------------------------------------------
// Function: setElement
// Descripton:
//      Set the value in the specified row and columnn and return
//      the array.
//------------------------------------------------------------------------------
list setElement( list array, integer row, integer col, integer value )
{
    vector metadata = llList2Vector( array, 0);
    integer cols = (integer)metadata.y;
    integer index = row * cols + col  + 1;
    return llListReplaceList(array, [value], index, index);
}

//------------------------------------------------------------------------------
//
//------------------------------------------------------------------------------
default
{
    state_entry()
    {

       integer rows = 4;
       integer cols = 6;
       integer row;
       integer col;
        integer index;
        // Build the array
        list elements= makeArray( 4, 6 );

        for (row=0; row < rows; ++row)
        {
            for ( col=0; col