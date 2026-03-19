---
name: "Pseudo-randomly Generate Unique Indices"
category: "example"
type: "example"
language: "LSL"
description: "Ordinarily when a collection of data needs to be retrieved in a random order, it can simply be reshuffled by randomly swapping elements and then iterating through the resulting, shuffled, collection. However there are cases where this is infeasible, especially in LSL, and as such the following functions can be used to generate indices in a pseudo-random way that should be \"good enough\" for many purposes."
wiki_url: "https://wiki.secondlife.com/wiki/Pseudo-randomly_Generate_Unique_Indices"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

- 1 Pseudo-randomly Generate Unique Indices

  - 1.1 Examples

  - 1.1.1 List
  - 1.1.2 String
  - 1.1.3 Notecard
- 2 Multiple Number Generators

  - 2.1 Single Integer State

  - 2.1.1 Example
  - 2.2 List State

  - 2.2.1 Full Precision
  - 2.2.2 16-bit Precision
  - 2.2.3 Example

Pseudo-randomly Generate Unique Indices

Ordinarily when a collection of data needs to be retrieved in a random order, it can simply be reshuffled by randomly swapping elements and then iterating through the resulting, shuffled, collection. However there are cases where this is infeasible, especially in LSL, and as such the following functions can be used to generate indices in a pseudo-random way that should be "good enough" for many purposes.

```lsl
integer _prui_counter = 1;
integer _prui_limit = 0;

integer _prui_start = 0;
integer _prui_stride = 0;
integer _prui_next = 0;

// Configures the random number generator to generate values between 0 (inclusive) and limit (exclusive) and initialises
prui_init(integer limit) {
    _prui_limit = limit;
    _prui_start = (integer)llFrand((float)limit);
    _prui_stride = (integer)llFrand((float)limit - 1.0) + 1;
    _prui_next = _prui_start;
}

// Call this each time the next random value is required.
// When configured with a limit of N, every discreet batch of N calls to this function will return each possible index only once.
integer prui_next() {
    if (!_prui_counter) prui_init(_prui_limit);

    integer result = _prui_next;
    _prui_next = (_prui_next + _prui_stride) % _prui_limit;
    if (_prui_next == _prui_start) {
        _prui_start = (_prui_start + 1) % _prui_limit;
        _prui_next = _prui_start;
    }

    _prui_counter = (_prui_counter + 1) % _prui_limit;
    return result;
}
```

## Examples

### List

The following script will spit out a random entry from a list when touched. In this example the list contains letters of the alphabet and as such the first 26 touches will produce a unique letter, the following 26 touches will likewise produce no duplicates and so-on.

```lsl
// Add the above prui variables and functions here

list myList = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"];
integer myListLength;

default {
    state_entry() {
        prui_init(myListLength = llGetListLength(myList));
        llSetText("Touch me for a complimentary letter of the alphabet!", <1.0, 1.0, 1.0>, 1.0);
    }

    touch_start(integer x) { llRegionSayTo(llDetectedKey(0), PUBLIC_CHANNEL, llList2String(myList, prui_next())); }
}
```

### String

This is the same example rewritten to more efficiently use a string for storing the letters of the alphabet:

```lsl
// Add the above prui variables and functions here

string myString = "abcdefghijklmnopqrstuvwxyz";
integer myStringLength;

default {
    state_entry() {
        prui_init(myStringLength = llStringLength(myString));
        llSetText("Touch me for a complimentary letter of the alphabet!", <1.0, 1.0, 1.0>, 1.0);
    }

    touch_start(integer x) { llRegionSayTo(llDetectedKey(0), PUBLIC_CHANNEL, llGetSubString(myString, x = prui_next(), x)); }
}
```

### Notecard

Finally, this example performs the same incredible feat using lines in a notecard (one for each letter of the alphabet):

```lsl
// Add the above prui variables and functions here

key myNotecard = "a62213ba-381d-2347-7f7b-818f15f12d83";
integer myNotecardLength = -1;
key talkTo = NULL_KEY;

default {
    state_entry() { llGetNumberOfNotecardLines(myNotecard); }
    dataserver(key id, string data) {
        if (myNotecardLength > 0) llRegionSayTo(talkTo, PUBLIC_CHANNEL, data);
        else prui_init(myNotecardLength = (integer)data);
    }

    touch_start(integer x) {
        talkTo = llDetectedKey(0);
        llGetNotecardLine(myNotecard, prui_next());
    }
}
```

Multiple Number Generators

The above code is fine for uses where only a single number generator is required, for example when communicating with a single avatar. However, when working with multiple random tasks it is not possible for a single number generator to produce values for different limits without completing the tasks sequentially (or aborting one), and in cases where the limit is the same, sharing a single number generator between multiple tasks will cause it to produce duplicates faster. For example, if a script is sending one of 100 possible messages randomly to four different avatars, then it will only have an effective entropy of around 25 messages (though for random messages this doesn't necessarily mean noticeably more duplicates).

For such cases, the following alternative functions enable the use of multiple number generators by producing and updating a state, by giving each task/avatar their own state value, it is possible to generate the full range of indices for each task/avatar.

## Single Integer State

The fastest and most memory efficient implementation uses four 8-bit values packed into a single 32-bit integer for its state, however this produces the following caveats:

- This implementation can only handle limits of up to 256.
- This implementation does not call mprui_init() after exactly N iterations, which means that it cannot guarantee a full N iterations without duplicates, however for most purposes this should still be adequate.

```lsl
// Configures the random number generator to generate values between 0 (inclusive) and limit (exclusive, max 256) and initialises
// Returns an mprui state that can then be passed into mprui_next()
integer mprui_init(integer limit) {
    integer start = (integer)llFrand((float)limit);
    integer stride = (integer)llFrand((float)limit - 1.0) + 1;

    return ((limit - 1) << 24) | (start << 16) | (stride << 8) | start;
}

// Call this each time the next random value is required.
// When configured with a limit of N, every discreet batch of *around* N calls to this function will return each possible index only once.
// This function should be passed an mprui_state generated using mprui_init, and will return an updated state in response. Mask with 0xFF to get the index like so:
// mprui_state = prui_next(mprui_state);
// integer next_index = mprui_state & 0xFF;
integer mprui_next(integer mprui_state) {
    integer limit = ((mprui_state >> 24) & 0xFF) + 1;
    integer start = (mprui_state >> 16) & 0xFF;
    integer stride = (mprui_state >> 8) & 0xFF;
    integer next = mprui_state & 0xFF;

    next = (next + stride) % limit;
    if (next == start) { // We're about to repeat
        // This is a hack that can result in fewer or greater than limit
        // repetitions, but is fine in the spirit of "good enough"
        if (next >= (limit - 1)) return mprui_init(limit);

        // Move the start and insert into new state
        next = (start + 1) % limit;
        mprui_state = (mprui_state & 0xFF00FFFF) | (next << 16);
    }

    // Insert next value into state
    return (mprui_state & 0xFFFFFF00) | next;
}
```

### Example

The following example takes the same string-based alphabet spewing device and adapts it to support multiple avatars, which will each get their own unique range of random letters no matter how many are also using the device.

```lsl
// Insert the single-integer mprui functions here

string myString = "abcdefghijklmnopqrstuvwxyz";
integer myStringLength;

list avatars = []; integer avatar_limit = 8; // Maximum number of avatars to keep track of (list is pruned from longest ago touch)
integer avatar_stride = 2; // Key + mprui state

default {
    state_entry() { llSetText("Touch me for a complimentary letter of the alphabet!", <1.0, 1.0, 1.0>, 1.0); }

    touch_start(integer x) {
        key id = llDetectedKey(0); integer mprui_state;

        integer index = llListFindList(avatars, [id]);
        if (~index) {
            mprui_state = mprui_next(llList2Integer(avatars, index + 1));

            // Remove our old state
            avatars = llDeleteSubList(avatars, index, index + 1);
        } else {
            mprui_state = mprui_init(llStringLength(myString));

            // Make room if the list is full
            integer prune = ((llGetListLength(avatars) / avatar_stride) + 1) - avatar_limit;
            if (prune > 0) avatars = llDeleteSubList(avatars, 0, (prune * avatar_stride) - 1);
        }

        integer next = mprui_state & 0xFF;
        llRegionSayTo(id, PUBLIC_CHANNEL, llGetSubString(myString, next, next));

        // Add the new state to the end of the list
        avatars += [id, mprui_state];
    }
}
```

## List State

For greater precision a list-based state must be used, which naturally carries with it the overhead of list manipulation. This comes in two varieties, a 16-bit precision which uses a list that is three elements long, and a full (32-bit) precision variation that uses a five element list. In both cases the next value is stored in the first element of the list, as such the implementations can actually be used interchangeably.

### Full Precision

```lsl
// Configures the random number generator to generate values between 0 (inclusive) and limit (exclusive) and initialises
// Returns an mprui state that can then be passed into mprui_next()
list mprui_init(integer limit) {
    integer start = (integer)llFrand((float)limit);
    integer stride = (integer)llFrand((float)limit - 1.0) + 1;

    return [start, 1, start, stride, limit];
}

// Call this each time the next random value is required.
// When configured with a limit of N, every discreet batch of N calls to this function will return each possible index only once.
// This function should be passed an mprui_state generated using mprui_init, and will return an updated state in response. Retrieve the first element to get the next index like so:
// mprui_state = prui_next(mprui_state);
// integer next_index = llList2Integer(mprui_state, 0);
list mprui_next(list mprui_state) {
    integer next    = llList2Integer(mprui_state, 0);
    integer counter = llList2Integer(mprui_state, 1);
    integer start   = llList2Integer(mprui_state, 2);
    integer stride  = llList2Integer(mprui_state, 3);
    integer limit   = llList2Integer(mprui_state, 4);

    if (!counter) return mprui_init(limit);

    next = (next + stride) % limit;
    if (next == start) {
        start = (start + 1) % limit;
        next = start;

        return llListReplaceList(mprui_state, [next, (counter + 1) % limit, start], 0, 2);
    }

    return llListReplaceList(mprui_state, [next, (counter + 1) % limit], 0, 1);
}
```

### 16-bit Precision

The following list-state implementation restricts precision to 16-bits (max limit of 65536) but uses a smaller list for its state (3 elements vs 5):

```lsl
// Configures the random number generator to generate values between 0 (inclusive) and limit (exclusive) and initialises
// Returns an mprui state that can then be passed into mprui_next()
list mprui_init(integer limit) {
    integer start = (integer)llFrand((float)limit);
    integer stride = (integer)llFrand((float)limit - 1.0) + 1;

    return [start, 0x10000 | start, (stride << 16) | limit];
}

// Call this each time the next random value is required.
// When configured with a limit of N, every discreet batch of N calls to this function will return each possible index only once.
// This function should be passed an mprui_state generated using mprui_init, and will return an updated state in response. Retrieve the first element to get the next index like so:
// mprui_state = prui_next(mprui_state);
// integer next_index = llList2Integer(mprui_state, 0);
list mprui_next(list mprui_state) {
    integer next    = llList2Integer(mprui_state, 0);
    integer counter = llList2Integer(mprui_state, 1);
    integer start   = counter & 0xFFFF; counter = (counter >> 16) & 0xFFFF;
    integer stride  = llList2Integer(mprui_state, 2);
    integer limit   = stride & 0xFFFF; stride = (stride >> 16) & 0xFFFF;

    if (!counter) return mprui_init(limit);

    next = (next + stride) % limit;
    if (next == start) {
        start = (start + 1) % limit;
        next = start;
    }

    return llListReplaceList(mprui_state, [next, ((counter + 1) % limit) << 16 | start], 0, 1);
}
```

### Example

Once again we grant the gift of the alphabet upon avatars, this time using either of the above list-state implementations:

```lsl
// Insert the mprui functions from either of the list-state options here

string myString = "abcdefghijklmnopqrstuvwxyz";
integer myStringLength;

list avatars = []; integer avatar_limit = 8; // Maximum number of avatars to keep track of (list is pruned from longest ago touch)
integer avatar_stride;

default {
    state_entry() {
        // Get the stride width for avatar entries
        avatar_stride = llGetListLength(mprui_init(llStringLength(myString))) + 1;
        llSetText("Touch me for a complimentary letter of the alphabet!", <1.0, 1.0, 1.0>, 1.0);
    }

    touch_start(integer x) {
        key id = llDetectedKey(0); list mprui_state;

        integer index = llListFindList(avatars, [id]);
        if (~index) {
            mprui_state = mprui_next(llList2List(avatars, index + 1, index + (avatar_stride - 1)));

            // Remove our old state
            avatars = llDeleteSubList(avatars, index, index + 5);
        } else {
            mprui_state = mprui_init(llStringLength(myString));

            // Make room if the list is full
            integer prune = ((llGetListLength(avatars) / avatar_stride) + 1) - avatar_limit;
            if (prune > 0) avatars = llDeleteSubList(avatars, 0, (prune * avatar_stride) - 1);
        }

        integer next = llList2Integer(mprui_state, 0);
        llRegionSayTo(id, PUBLIC_CHANNEL, llGetSubString(myString, next, next));

        // Add the new state to the end of the list
        avatars += [id] + mprui_state;
    }
}
```