---
name: "link_message"
category: "example"
type: "example"
language: "LSL"
description: "Triggered when the script receives a link message that was sent by a call to llMessageLinked. llMessageLinked is used to send messages from one script to another."
wiki_url: "https://wiki.secondlife.com/wiki/Link_message"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL


link_message

- 1 Description
- 2 Caveats
- 3 Examples
- 4 Useful Snippets

  - 4.1 Sending Lists
- 5 Notes
- 6 See Also

  - 6.1 Functions
- 7 Deep Notes

  - 7.1 Signature

## Description

 Event: link_message( integer sender_num, integer num, string str, key id ){ ; }


	29
	Event ID


	Delay


Triggered when the script receives a link message that was sent by a call to llMessageLinked. llMessageLinked is used to send messages from one script to another.• integer sender_num – The link number of the prim that contained the script that called llMessageLinked. • integer num – Second parameter of the llMessageLinked call. • string str – The message that was sent from the script that called llMessageLinked. • key id – Fourth parameter of the llMessageLinked call. id is often used as a second string field (in LSL the key type is implemented as a string with just custom operators). Typecasting between string and key types has no effect on the data contained. The sizes of str and id are only limited by available script memory. ## Caveats - 64 link_message events can queue, past that, they are silently dropped! Don't do too much in the event if they might be coming in fast. - sender_num does not reflect how a message was sent, there is no way to know if it was sent with a LINK_* flag or the specific link number. - If str and id are bigger than available memory the script will crash with a Stack-Heap Collision. ## Examples ```lsl // This is just an example script, you shouldn't handle touches within a single script this way. default { touch_start(integer num_detected) { llMessageLinked(LINK_THIS, 0, llDetectedName(0), llDetectedKey(0)); } link_message(integer source, integer num, string str, key id) { llWhisper(0, str + " (" + (string)id + ") touched me!"); } } ``` ## Useful Snippets ### Sending Lists ```lsl // This is just an example script, you shouldn't handle link messages within a single script this way. default { // To propagate an unlimited number of arguments of any type, as long as you don't run out of memory. // For low-latency operations, it is more efficient to concatenate the parameters into a string manually all at once, which avoids the comparatively slower llDumpList2String call but is not as flexible. // The separator string cannot be used in any source string, or the resulting list will be incorrectly parsed. // It is possible to design your own custom escape sequence for any instances of the separator string or use a rarer character, though that is outside the scope of this snippet. state_entry() { list my_list = [1, 2.0, "a string", , , llGetOwner()]; string list_parameter = llDumpList2String(my_list, "|"); // Produce a | delimited string from the list llMessageLinked(LINK_THIS, 0, list_parameter, NULL_KEY); } link_message(integer sender_num, integer num, string list_argument, key id) { if (list_argument != "") { list re_list = llParseStringKeepNulls(list_argument, ["|"], [""]); // Convert the string back to a list // llParseStringKeepNulls is used here in lieu of llParseString2List to accommodate any elements of my_list that were empty strings, which would otherwise be deleted. // Note that re_list will be a list of strings no matter what my_list contained, so only llList2String can be used on it, not llList2Integer, llList2Vector, etc. } else { // my_list was an empty list (or a list that contained only one empty string), so llParseStringKeepNulls is not necessary because it would potentially incorrectly return a list with a single blank string. // It is not possible to distinguish between the two, so it would be wise to check which is the case before sending if possible. } } } ``` ## Notes Important: A script can hear its own link messages.


- sender_num can be compared to llGetLinkNumber to determine whether the message was sent by the same prim, regardless of whether the prim is unlinked, a root, or a child.

## See Also

### Functions

•

llMessageLinked

## Deep Notes

#### Signature

```lsl
event void link_message( integer sender_num, integer num, string str, key id );
```