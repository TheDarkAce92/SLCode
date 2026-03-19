---
name: "LibObj"
category: "example"
type: "example"
language: "LSL"
description: "LibObj is a collection of functions that are designed to simplify data management of multiple, (pseudo-)parallel threads in LSL scripts. Examples include the communication with multiple avatars (e.g. through dialogs) or objects (e.g. through listens or HTTP) where the states of the communication threads are usually independent from one another."
wiki_url: "https://wiki.secondlife.com/wiki/LibObj"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

- 1 Introduction
- 2 Documentation
- 3 License
- 4 How to obtain

## Introduction

LibObj is a collection of functions that are designed to simplify data management of multiple, (pseudo-)parallel threads in LSL scripts. Examples include the communication with multiple avatars (e.g. through dialogs) or objects (e.g. through listens or HTTP) where the states of the communication threads are usually independent from one another.

To this end, the library implements a rudimentary concept of object-oriented data management. The concept should be relatively easy to grasp and use for programmers and offers versatile means to data management which is not resticted to its originally intended use case.

Management of "objects" is based on two functions, `objNew` and `objDelete`, which merely manage unique, light-weight object handles. Functionality is extended by various functions which operate on these handles. The library is modular in that only the subset of functions which is actually used by a particular script needs to be included.

## Documentation

Reference

For complete examples, please see the "Examples" subdirectory in the GitHub repo linked below.

## License

The library is open source under the MIT license.

## How to obtain

The latest version is available on [GitHub](https://github.com/furware/libobj).

---

## Subpage: Reference

- 1 LibObj Base - Object Handles
- 2 "Names" Extension
- 3 "Paths" Extension
- 4 "Data" Extension
- 5 "Properties" Extension
- 6 "Hierarchy" Extension
- 7 Object Timeouts

## LibObj Base - Object Handles

**Interface**

```lsl
integer objNew()
objDelete(integer id)
```

**Guarantees**

- The handle returned by `objNew` is positive (> 0).
- The handle returned by `objNew` is unique among all handles existing at the moment the function is called.
- `objDelete` does nothing if the given handle id does not exist.

**Assumptions**

- The implementation of `objDelete` should include calls to suitable functions of any used extensions to delete data associated with the given object.

**Description**

LibObj has a simple representation of "objects" as handles which are of type `integer`. Objects may be created and deleted using the "Object Base" module consisting of the functions `objNew` and `objDelete`. All handles returned by `objNew()` are unique within the script at any given point in time and positive (> 0). By themself, handles have little use but are instead intended to be used in combination with any of the extensions described below to associate additional data with the objects.

**Important:** In addition to deleting the object handle, the `objDelete` function also needs to call additional functions to delete any data associated with the object managed by the used extensions. Keep this in mind and make sure that all deletion function calls corresponding to the extensions you're using are included in the implementation of `objDelete`.

**Example**

```lsl
integer a = objNew(); // Create a new object.
objDelete(a); // Delete it again.
```

## "Names" Extension

**Interface**

```lsl
integer objSetName(integer id, string name)
string  objGetName(integer id)
integer objByName(string name)
```

**Guarantees**

- `objSetName` returns the given object handle, even if invalid.
- `objSetName` removes the name if `name == ""`.
- If a name for the given object already exists, `objSetName` replaces that name.
- `objByName` returns 0 if an object with the given name does not exist.

**Assumptions**

- No particular assumptions.

**Description**

The purpose of this extension is to address objects by name. Using the `objSetName` function of the names extension you can assign a name to an object. The main use of this extension is to look up objects by name using `objByName`. Once an object handle is retrieved, further operations may be performed on it. The `objByName` function returns 0 if an object with the given name is not found. Note that arbitrary data should generally not be stored as an object name; use the "data" or "properties" extensions for that purpose.

**Example**

```lsl
integer a = objNew(); // Create a new object.
objSetName(a, "A"); // Assign name to object.
llOwnerSay(objGetName(a)); // Says "A".
integer b = objByName("A"); // b == a.
objDelete(b); // Deletes the object.
```

## "Paths" Extension

**Interface**

```lsl
integer objSetPath(integer id, list path)
list    objGetPath(integer id)
string  objGetPathItem(integer id, integer item)
integer objByPath(list path)
```

**Guarantees**

- `objSetPath` returns the given object handle, even if invalid.
- `objSetPath` removes the path if `path == []`.
- If a path for the given object already exists, `objSetPath` replaces it.
- `objByPath` returns 0 if the given path does not match any object.

**Assumptions**

- All elements of paths are automatically converted to the string data type.
- No element of valid paths should contain the newline character ("\n").

**Description**

The purpose of this extension is to address objects in a hierarchical (tree-like) manner. It is a generalization of the "names" extensions with more possibilities. Instead of assigning an object a single string as name, a multi-element list ("path") of names may be given. This principle may be used to group objects of a specific "type" by giving them a common prefix (for instance the first item in the path list). The `objByPath` function to retrieve an object handle by path does **not** require the whole path to match but instead returns the first object whose path **prefix** matches the given list.

**Note:** All elements of a given path are converted to strings and **no** path element shall contain a **newline** ("\n") character.

**Example**

```lsl
integer a = objNew(); // Create a new object.
integer b = objNew(); // Create another object.
objSetPath(a, ["X"]); // Assigns path to object a.
objSetPath(b, ["X", "Y"]); // Assigns path to object b.
integer x = objByPath(["X"]); // x == a.
integer y = objByPath(["X", "Y"]); // y == b.
llOwnerSay(objGetPathItem(x, 0)); // Says "X".
llOwnerSay(objGetPathItem(y, 1)); // Says "Y".
objDelete(x); // Deletes x (and a).
objDelete(y); // Deletes y (and b).
```

## "Data" Extension

**Interface**

```lsl
integer objSetData(integer id, string data)
string  objGetData(integer id)
```

**Guarantees**

- `objSetData` returns the given object handle, even if invalid.
- `objSetData` removes any existing data for the given object if `data == ""`.
- `objGetData` returns the empty string ("") if no data is associated with the given object.

**Assumptions**

- No particular assumptions.

**Description**

The purpose of this extension is to assign a (string) payload to an object. It is similar to the "names" extension but does not include the capability to retrieve objects given a string. It is suitable to store possibly unsafe user data related to an object.

**Example**

```lsl
integer a = objNew(); // Create a new object.
objSetData(a, "Payload"); // Assign string data to object.
llOwnerSay(objGetData(a)); // Says "Payload".
objDelete(a); // Deletes the object.
```

## "Properties" Extension

**Interface**

```lsl
integer objSetProp(integer id, string prop, string data)
string  objGetProp(integer id, string prop)
```

**Guarantees**

- `objSetProp` returns the given object handle, even if invalid.
- `objSetProp` removes **all** properties of the given object if `prop == ""`.
- `objSetProp` removes a given property "X" if `prop == "X"` and `data == ""`.
- `objGetProp` returns the empty string ("") if the given object or property does not exist.

**Assumptions**

- No particular assumptions.

**Description**

The purpose of this extension is to assign **named** properties to an object. It is a generalization of the "data" extension in that it allows to assign **multiple** separate string payloads to a single object. The idea is to simulate the concept of e.g. "structs" or "dictionaries" in other languages.

**Example**

```lsl
integer a = objNew(); // Creates a new object.
objSetProp(a, "A", "X"); // Add property "A" with content "X".
objSetProp(a, "B", "Y"); // Add property "B" with content "Y".
objSetProp(a, "A", "Z"); // Replace content of property "A" with "Z".
llOwnerSay(objGetProp(a, "A")); // Says "Z".
objDelete(a); // Delete the object.
```

## "Hierarchy" Extension

**Interface**

```lsl
integer objSetParent(integer id, integer parent)
integer objGetParent(integer id)
integer objGetChild(integer id)
list    objGetChildren(integer id)
```

**Guarantees**

- `objSetParent` returns the given object handle, even if invalid.
- `objSetParent` removes the parent relation for the given object if `parent == 0`.
- `objGetChild` returns 0 if the given object has no children.
- `objGetChildren` returns the empty list ([]) if the given object has no children.

**Assumptions**

- If non-zero, the parent object given to `objSetParent` shall be a handle to an existing object.
- The `objDelete` function should take care of setting the parent of children of the object being deleted to 0.

**Description**

The purpose of this extension is to define "child-parent" relationships between objects which allows to build object hierarchies (without common, redundant name prefixes as with the "path" extension). An object may have one parent object specified using the `objSetParent` function. Conversely, an object `obj` may have multiple (implicitly defined) children which is the set of objects whose parent is `obj`. The function `objGetChild` returns the first child for a given object; the function `objGetChildren` may be used to get a list of all children of an object (a list of object handles).

**Example**

```lsl
integer a = objNew(); // Create object a.
integer b = objNew(); // Create object b.
integer c = objNew(); // Create object c.
objSetParent(b, a); // Set parent of object b to a.
objSetParent(c, a); // Set parent of object c to a.
list children = objGetChildren(a); // children == [b, c].
integer child = objGetChild(a); // x == b or x == c, implementation dependent.
while (child = objGetChild(a)) {objDelete(child);} // Delete children (b, c).
objDelete(a); // Delete remaining object.
```

## Object Timeouts

**Interface**

```lsl
integer objSetTimeout(integer id, integer time)
integer objCheckTimeout()

// Minimal timer event for handling timeouts:
timer() {
    integer obj;
    while (obj = objCheckTimeout()) {
        // Do something with obj.

        // Finally, you should either disable the timeout for the object
        // by calling objSetTimeout(obj, 0) or delete the object.
        objDelete(obj);
    }
}
```

**Guarantees**

- `objSetTimeout` returns the given object handle, even if invalid.
- Timeout is removed by `objSetTimeout` if `time <= 0`

**Assumptions**

- The temporal resolution of timeouts are relatively coarse (seconds).
- The timeout mechanism should not be used for high frequency timers.

**Description**

The purpose of this extension is to set independent timeouts for objects which are handled asynchronously by a timer event at a later point in time.

**Example**

```lsl
integer a = objNew(); // Create a new object.
objSetTimeout(a, 5); // Timeout handle will trigger in approximately 5 seconds in timer event.
```