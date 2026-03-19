---
name: "3D Pseudo-Array"
category: "example"
type: "example"
language: "LSL"
description: "In my previous article 2D_Pseudo-Array, I discussed how to acheive 2 dimensional array behavior in LSL. In this article, we will look at doing the same for a 3 dimensional array."
wiki_url: "https://wiki.secondlife.com/wiki/3D_Pseudo-Array"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

In my previous article 2D_Pseudo-Array, I discussed how to acheive 2 dimensional array behavior in LSL.  In this article, we will look at doing the same for a 3 dimensional array.

A list is defined as “a heterogeneous list of the other data types”.  It is linear by nature and can be thought of as a single column.  At the physical level, arrays are stored in contiguous sections of memory. (Another linear structure)  An algorithm is used to translate between the logical rows and columns and the physical level of addresses.

**Consider a list with 48 elements. Normally we visualize this as a vertical column. In this case, it is convenient to think of them as 2 tables of 4 rows and 6 columns. Notice we are starting with element 1. Element zero is reserved for metadata about the size of the array. Layer 0**

     **0****1****2****3****4****5**
    **0** 1 2 3 4 5 6
    **1** 7 8 9101112
    **2**131415161718
    **3**192021222324

**Layer 1**

     **0****1****2****3****4****5**
    **0**252627282930
    **1**313233343536
    **2**373839404142
    **3**434445464748

**Figure 1.**  Indexes of a list arranged in rows and columns.

**Our addressing algorithm can use the following formula: index = (rows * cols * layer) + row * cols + col + 1 Where:**

- row is the row number of the element
- cols is the number of columns in the array
- col is the column number of the element

**Example:** Find the index for the data stored in layer 1, row 3 and column 4.

8index = (rows * cols * layer) + row * cols + col + 1
8index = (4 * 6 * 1) + (3 * 6 + 4) + 1
8index = 47



We will implement this in a set of functions.  These functions raise the level of abstraction and give us the ability to manipulate arrays referencing rows and columns.





## LSL Implementation:

```lsl
//------------------------------------------------------------------------------
// Function: initIntArray
// Descripton:
//      Given the number of rows, columns and layers, create an list of integers
//      that will be used as an array.
//------------------------------------------------------------------------------
list makeArray ( integer rows, integer cols, integer layers )
{
    integer i;
    list array = [];
    array += < rows, cols, layers >;
    for (i=0; i < rows * cols * layers; ++i)
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
integer getElement( list array, integer row, integer col, integer layer )
{
    vector metadata = llList2Vector( array, 0);
    integer rows = (integer)metadata.x;
    integer cols = (integer)metadata.y;
    integer index = (rows * cols * layer) + (row * cols + col + 1);
    return llList2Integer( array, index);
}

//------------------------------------------------------------------------------
// Function: setElement
// Descripton:
//      Set the value in the specified row and columnn and return
//      the array.
//------------------------------------------------------------------------------
list setElement( list array, integer row, integer col, integer layer, integer value )
{
    vector metadata = llList2Vector( array, 0);
    integer rows = (integer)metadata.x;
    integer cols = (integer)metadata.y;
    integer index = (rows * cols * layer) + (row * cols + col + 1);
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
       integer cols = 4;
       integer layers = 2;
       integer row;
       integer col;
       integer layer;
       integer index;

        // Build the array
        list elements= makeArray( rows, cols, layers );
        for (layer = 0; layer < layers; ++layer)
        {
            for (col=0; col < cols; ++col)
            {
                for ( row=0; row < rows; ++row)
                {
                    index = (rows * cols * layer) + (row * cols + col + 1);
                    elements = setElement(elements, row, col,layer, index) ;
                }
            }
        }

        for (layer = 0; layer < layers; ++layer)
        {
            for (row=0; row < rows; ++row)
            {
                for ( col=0; col < cols; ++col)
                {
                    // Report the value at (3,4)
                    integer element = getElement( elements,row,col,layer);
                    llOwnerSay(  "layer=" + (string)layer
                               + ", row=" + (string)row
                               + ", col=" + (string)col
                               + ", index=" + (string)element);
                }
            }
        }
    }//end state entry
}//end default
```