---
name: "FURWARE_text"
category: "example"
type: "example"
language: "LSL"
description: "This page is also available in German. / Diese Seite ist auch auf deutsch verfügbar."
wiki_url: "https://wiki.secondlife.com/wiki/FURWARE_text"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

This page is also available in German. / Diese Seite ist auch auf deutsch verfügbar.

**- 1 Overview - 2 Features - 3 How to obtain the script - 4 Documentation - 5 Texture creator - 6 How to contribute - 7 Known issues ## Overview FURWARE text is a script for displaying text** on prims using textures. It is intended to be **integrated in your objects** in which it will be controlled by **your own scripts**.

FURWARE text **is not** a ready-made display board but is intented for **scripters** who wish to integrate it in their own creations.

The script was proprietary from 2010 to July 2013 until I (Ochi Wolfe) have decided to make it open source under the MIT license. It is my first attempt to make a fully open sourced product in Second Life.

## Features

- **Open source** (MIT license)
- **Only one script** for a whole group ("sets") of displays
- **Formatting** (color, alpha, alignment, wrapping, trimming, font, borders)
- **Mesh prims** with 1 to 8 chars, only occupying 0.5 prims each
- **Virtual text boxes** to position text arbitrarily
- **Style templates** for encapsulating multiple style settings

## How to obtain the script

You can obtain a complete package containing the script, the display creator, display meshes and font textures at [the Marketplace](http://marketplace.secondlife.com/p/FURWARE-text/141379).

For developers and interested users, I have also set up a [GitHub](http://github.com/furware/text) account for the core scripts.

## Documentation

Please see the following subpages for the user's manual and developer documentation:

First steps & extensive tutorial

Short reference & version history

Helper functions for more convenient usage

Developer documentation

## Texture creator

Please see this page for information about the texture creator tool for making your own font textures.

## How to contribute

**For users:** A very important part of contribution to the development of this script is to report any problems you experience while using it as well as suggestions how to make using it even more awesome. For the time being, feel free to write a notecard to Ochi Wolfe or add your comments to the discussion of this wiki-page.

**For developers:** If you have any suggestions for improvements to the script itself, you can either post them in the same way or you can branch the project on [GitHub](http://github.com/furware/text) and send your pull requests. Just make sure that they are, of course, of awesome quality and that they don't bloat the script more than it already is bloated. In fact, any suggestions to improve performance and decrease memory consumption are **very** welcome.

## Known issues

No issues are known for the current release, but please report any problems you find.

---

## Subpage: de

/de
/LSL

Diese Seite ist auch auf englisch verfügbar. / This page is also available in English.

**- 1 Übersicht - 2 Merkmale - 3 Wo du das Skript bekommst - 4 Dokumentation - 5 Texture creator - 6 Wie du helfen kannst - 7 Bekannte Probleme ## Übersicht FURWARE text ist ein Skript zur Darstellung von Text** mittels Texturen auf Prims. Es ist zum **Einbau in deine Objekte** gedacht in denen es von **deinen eigenen Skripten** gesteuert wird.

FURWARE text **ist keine** vorgefertigte Anzeigetafel sondern ist für **Skripter** gedacht, die es in ihre eigene Kreationen integrieren.

Das Skript war von 2010 bis Juli 2013 proprietär bis ich (Ochi Wolfe) mich dazu entschieden habe, es Open Source unter der MIT-Lizenz zu machen. Dies ist mein erster Versuch eines vollständig offenen Produkts in Second Life.

## Merkmale

- **Open source** (MIT license)
- **Nur ein Skript** für eine ganze Gruppe ("sets") von Anzeigetafeln
- **Formatierung** (Farbe, Alpha, Ausrichtung, Umbruch, Trimming, Font, Rahmen)
- **Mesh prims** mit 1-8 Zeichen, die je nur 0.5 Prims belegen
- **Virtuelle Text-Boxen** um Text beliebig zu Positionieren
- **Style templates** um mehrere Stileinstellungen zusammenzufassen

## Wo du das Skript bekommst

Du kannst dir ein komplettes Paket inklusive dem Display Creator, Meshes und Schrift-Texturen auf [dem Marketplace](http://marketplace.secondlife.com/p/FURWARE-text/141379) holen.

Für Entwickler und interessierte Benutzer habe ich für die Skripte außerdem einen Account auf [GitHub](http://github.com/furware/text) erstellt.

## Dokumentation

Unter den folgenden Unterseiten findest du eine Bedienungsanleitung sowie Dokumentation für Entwickler:

Erste Schritte & ausführliches Tutorial

Kurzreferenz & Versionsgeschichte

Hilfsfunktionen für einfachere Verwendung

Dokumentation für Entwickler

## Texture creator

Auf dieser Seite findest du mehr Informationen zum "texture creator", mit dem du deine eigenen Schrifttexturen erstellen kannst.

## Wie du helfen kannst

**Für Anwender:** Eine wichtige Hilfe bei der Entwicklung dieses Skripts ist das Berichten von Problemen bei seiner Verwendung sowie Vorschläge, wie man die Benutzung noch besser machen kann. Momentan sind die wahrscheinlich besten Möglichkeiten hierfür Ochi Wolfe eine Notecard zu schreiben oder deine Kommentare zur Diskussion dieser Wiki-Seite hinzuzufügen.

**Für Entwickler:** Wenn du Vorschläge für die Verbesserung des Skripts hast kannst du diese gerne auf dieselbe Weise kundtun. Alternativ kannst du aber auch gerne einen Branch des Projekts auf [GitHub](http://github.com/furware/text) erstellen und Pull-Requests senden. Bitte stelle sicher, dass die Änderungen von sehr guter Qualität sind und sie das Skript nicht weiter aufblähen als es sowieso schon ist. Genauergesagt sind Vorschläge zur Verbesserung der Performance und Senkung des Speicherverbrauchs **äußerst** gern gesehen.

## Bekannte Probleme

Für die aktuelle Version sind keine Probleme bekannt. Falls welche auftreten, melde dies bitte.

---

## Subpage: Tutorial

- 1 First steps - 1.1 Creating displays - 1.2 Setup and initialization - 2 Tutorial - 2.1 Preparations - 2.2 Single display set - 2.3 Multiple display sets - 2.4 Virtual text boxes - 2.4.1 A more concise version - 2.4.2 Box borders - 2.4.3 Deleting boxes - 2.5 Touch queries - 2.5.1 Performing a query - 2.5.2 Parsing the reply - 2.6 Style templates - 2.7 Configuring multiple boxes at once - 2.8 Global style settings - 2.9 Inline styles - 2.9.1 Selectively disabling inline styles ## First steps ### Creating displays You may (and should) use the included "FURWARE display creator" to have a perfectly aligned grid of display prims automatically created for you. Every prim will be automatically assigned a special object name that is used internally by the text script so that it knows how to order them correctly, independently of the link order.

Creating a display is simple:

- Rez the display creator on a parcel where you have sufficient permissions.
- Touch the creator object. A dialog appears where you can set some parameters of the new display:

  - A **name** for the display. You will use this name to identify which display you wish to manipulate when using multiple displays within one linkset.
  - The number of **rows and columns** of the display (the columns are counted in prims here, not in characters).
  - The number of **faces per prim**. There are mesh prims from 1 to 8 faces available. Generally speaking, using more faces per prim is more efficient.
- When you're happy with the settings, click "Create" to start rezzing the prims. Link them to your creation as appropriate.

### Setup and initialization

When you have created your display(s) and linked them together in your creation, simply put **a single copy** of the FURWARE text script into the linkset. Only a single copy of the text script is required for handling multiple display sets within a linkset. The script does **not** have to be in the root prim.

**Important hint:**

You may wish to send some initial commands to the text script as soon as its initialization is done. A reset of the text script may happen in a number of cases:

- The script was just put into the object.
- The object in which the script resides was shift-copied.
- The linkset has changed (then the script needs to search for display prims again).
- The script was reset manually (for instance using the "fw_reset" command).

In order to know when exactly the script is ready to take commands, it sends a link message to the whole set with the "id" parameter set to "fw_ready". It is **good practice** to watch for these messages and send your initialization commands when receiving this message. Your code could look something like this:

```lsl link_message(integer sender, integer num, string str, key id) { if (id == "fw_ready") { llOwnerSay("FW text is up and running!"); // Start sending some initialization stuff. llMessageLinked(sender, 0, "c=red", "fw_conf"); llMessageLinked(sender, 0, "Default text", "fw_data"); // ... } } ``` ## Tutorial ### Preparations Let's first prepare a small framework that you can use to try out the examples in this tutorial. It may be convenient to reset the FURWARE text script each time you make changes to the controller script to start with a freshly initialized script so that settings made in previous runs won't interfere. You can use the following snippet as a starting point: ```lsl default { state_entry() { // Reset the FURWARE text script. llMessageLinked(LINK_SET, 0, "", "fw_reset"); } link_message(integer sender, integer num, string str, key id) { // The text script sends "fw_ready" when it has initialized itself. if (id == "fw_ready") { // Here you can try out your commands. } } } ``` Tip: For the sake of simplicity, all commands shown in this tutorial will be sent to LINK_SET. You can of course use more specific/optimized receivers in your own objects.


**Important:** It is usually **not** considered good practice to reset the script each time you wish to change something. Once you get more familiar with the concepts of FURWARE text you will see that you can do almost anything without ever having to fully reset the script. It is just more convenient for your first experiments.


### Single display set Let's first consider the simplest case. As a concrete example, let's assume that we have created a display consisting of 3 by 4 prims, each of them having 8 faces. Here's a schematic representation of our display: We first take look at the two most important commands of FURWARE text, namely "fw_data" for setting text and "fw_conf" to control style preferences (text color, alignment, font, etc.). Setting the text is done like so: ```lsl llMessageLinked(LINK_SET, 0, "This is some example text", "fw_data"); ``` This will yield: Similarly, setting the text color to blue and the **alignment** to centered is done using the following call:

**```lsl llMessageLinked(LINK_SET, 0, "c=blue; a=center", "fw_conf"); ``` Combined with the previous "fw_data" call, the display now looks like this: Tip:** You do not have to send both style and text data each time you wish to change one or the other. When setting the style, the currently set text is re-used and rendered with the new style. Likewise, when setting text, the currently set style will be used.


**### Multiple display sets A single FURWARE text script can handle multiple display sets within a linkset. Let's consider the following example consisting of three sets named "Alpha", "Beta" and "Gamma": Tip:** The sets do not have to use the same prim type (i.e. number of faces per prim) but **within** a particular set, the prim type and the number of columns in each row need to be the same.


**If we use the same two lines of code for setting the text and style as in the single-set case, all sets** will use the **same** settings. So using the code

**```lsl llMessageLinked(LINK_SET, 0, "This is some example text", "fw_data"); llMessageLinked(LINK_SET, 0, "c=blue; a=center", "fw_conf"); ``` will yield Now the question arises how to set text and styles for the individual** sets independently. This is where the **names** of the display sets that we have specified when we created the displays come into play. The last parameter of the llMessageLinked()-call needs to be modified. For instance, for setting the text and style of the set "Beta", instead of writing "fw_data" and "fw_conf" we specify the set name by writing "**fw_data : Beta**" and "**fw_conf : Beta**":

```lsl llMessageLinked(LINK_SET, 0, "Only for set Beta", "fw_data : Beta"); llMessageLinked(LINK_SET, 0, "c=red", "fw_conf : Beta"); ``` Again combining these lines with the previous code, this will yield: ### Virtual text boxes In addition to using multiple sets, we can also define multiple virtual text boxes within a display set. This can be used to easily position text on a display, for example for displaying **tables**, **dialog boxes** and much more.

In the following example we have two sets called "Dialog" and "Table". Let's assume that we wish to use the set "Dialog" as a simple dialog with two buttons and the set "Table" as a small table having three rows, three columns and an additional column that will be used for "up" and "down" buttons.

The small overlap between the column boxes will be useful later when adding borders to our boxes.

**The first task is to add** the text boxes to the sets. This is done using the "fw_addbox" command. The syntax of the command is:

*fw_addbox : boxName : parentName : dx, dy, sx, sy : stylePrefs*

The meaning of the individual parameters is as follows:

- **boxName**: A user-specified name for the new box. Must be **unique** among all box and set names.
- **parentName**: The name of the **set or box** that the new box should be aligned relatively to.
- **dx, dy, sx, sy**: Four integers specifying the **position** relative to the parent set or box (dx, dy) and the **size** of the box (sx, sy).
- **stylePrefs**: A style string (for example "c=red; a=center") that the box should use as its default; may be omitted.

Let us write down the code for adding the boxes in our example. We will first make it rather **verbose** and take a look at a shorter version later.

```lsl // Add the boxes. llMessageLinked(LINK_SET, 0, "", "fw_addbox : ButtonOK : Dialog : 1, 2, 10, 1"); llMessageLinked(LINK_SET, 0, "", "fw_addbox : ButtonCancel : Dialog : 13, 2, 10, 1"); llMessageLinked(LINK_SET, 0, "", "fw_addbox : Column0 : Table : 0, 1, 8, 3"); llMessageLinked(LINK_SET, 0, "", "fw_addbox : Column1 : Column0 : 7, 0, 8, 3"); llMessageLinked(LINK_SET, 0, "", "fw_addbox : Column2 : Column1 : 7, 0, 8, 3"); llMessageLinked(LINK_SET, 0, "", "fw_addbox : UpDown : Column2 : 9, 0, 1, 3"); // Set the boxes' style. llMessageLinked(LINK_SET, 0, "a=center", "fw_conf : ButtonOK"); llMessageLinked(LINK_SET, 0, "a=center", "fw_conf : ButtonCancel"); llMessageLinked(LINK_SET, 0, "w=none", "fw_conf : Column0"); llMessageLinked(LINK_SET, 0, "w=none", "fw_conf : Column1"); llMessageLinked(LINK_SET, 0, "w=none", "fw_conf : Column2"); // Set some text for the boxes. llMessageLinked(LINK_SET, 0, "Some dialog", "fw_data : Dialog"); llMessageLinked(LINK_SET, 0, "OK", "fw_data : ButtonOK"); llMessageLinked(LINK_SET, 0, "Cancel", "fw_data : ButtonCancel"); llMessageLinked(LINK_SET, 0, "One\nTwo\nThree", "fw_data : Column0"); llMessageLinked(LINK_SET, 0, "123\n456\n789", "fw_data : Column1"); llMessageLinked(LINK_SET, 0, "1.2\n2.3\n3.4", "fw_data : Column2"); llMessageLinked(LINK_SET, 0, "▲\n\n▼", "fw_data : UpDown"); ``` This will yield a constellation as depicted below. Please take a moment to understand all parts of the commands. The first two boxes were added to the parent "Dialog" which is the name of the left set, hence the "Dialog" as the third parameter to "fw_addbox". You may also specify the name of another box as the parent, then the coordinates of the new box will be **relative** to the upper-left corner of that (already added) box. For instance, for box "Column1" we have used "Column0" as the parent box and then specified the coordinates relative to the upper-left corner of that box. The same was done for the boxes "Column2" and "UpDown".

After the boxes have been created, we have set some style preferences for them. For instance, we have set the **alignment** of the dialog buttons to center ("a=center") and **disabled wrapping** ("w=none") for the table's columns so that even overlong lines will always stay within one row of our table.

Lastly, we have set some text for each of the boxes.

#### A more concise version

As mentioned before, we can write the above example in a more concise way by directly specifying style and text data **when creating the boxes**. The following code results in the same constellation as in the last example:

```lsl llMessageLinked(LINK_SET, 0, "OK", "fw_addbox : ButtonOK : Dialog : 1, 2, 10, 1 : a=center"); llMessageLinked(LINK_SET, 0, "Cancel", "fw_addbox : ButtonCancel : Dialog : 13, 2, 10, 1 : a=center"); llMessageLinked(LINK_SET, 0, "One\nTwo\nThree", "fw_addbox : Column0 : Table : 0, 1, 8, 3 : w=none"); llMessageLinked(LINK_SET, 0, "123\n456\n789", "fw_addbox : Column1 : Column0 : 7, 0, 8, 3 : w=none"); llMessageLinked(LINK_SET, 0, "1.2\n2.3\n3.4", "fw_addbox : Column2 : Column1 : 7, 0, 8, 3 : w=none"); llMessageLinked(LINK_SET, 0, "▲\n\n▼", "fw_addbox : UpDown : Column2 : 9, 0, 1, 3"); llMessageLinked(LINK_SET, 0, "Some dialog", "fw_data : Dialog"); ``` #### Box borders FURWARE text offers a special style option that comes in especially handy when dealing with boxes: The border style option. Because an example probably says more than words here, consider the following modification of the previous example:

```lsl llMessageLinked(LINK_SET, 0, "OK", "fw_addbox : ButtonOK : Dialog : 1, 2, 10, 1 : a=center; border=lr"); llMessageLinked(LINK_SET, 0, "Cancel", "fw_addbox : ButtonCancel : Dialog : 13, 2, 10, 1 : a=center; border=lr"); llMessageLinked(LINK_SET, 0, "One\nTwo\nThree", "fw_addbox : Column0 : Table : 0, 1, 8, 3 : w=none; border=lr"); llMessageLinked(LINK_SET, 0, "123\n456\n789", "fw_addbox : Column1 : Column0 : 7, 0, 8, 3 : w=none; border=lr"); llMessageLinked(LINK_SET, 0, "1.2\n2.3\n3.4", "fw_addbox : Column2 : Column1 : 7, 0, 8, 3 : w=none; border=lr"); llMessageLinked(LINK_SET, 0, "▲\n\n▼", "fw_addbox : UpDown : Column2 : 9, 0, 1, 3"); llMessageLinked(LINK_SET, 0, "Some dialog", "fw_data : Dialog"); llMessageLinked(LINK_SET, 0, "border=lrtb", "fw_conf : Dialog"); ``` In the following picture, the separating lines between the prims and faces were omitted so you can get a better view on the borders introduced by the above commands. Note how FURWARE text automatically adjusts the text positions according to the borders. The "border" style setting takes any (meaningful) combination of the letters **tblrTBLR12** (order does not matter). The lowercase letters t, b, l, r introduce borders at the top, bottom, left or right side. The uppercase letters T, B, L, R additionally introduce special characters at the corners of boxes to connect them with other boxes (see also the next picture). The numbers "1" or "2" yield different border styles. Here are a few examples:

**Now it should become clear why the previously mentioned overlap of the table's columns is useful: This way we could simply set the borders of all** table columns to left and right without having to distinguish between them.

**Tip:** The additional space that is needed to draw the borders must be manually added to the respective box sizes.


#### Deleting boxes Deleting boxes is done using the "fw_delbox" command followed by the box's name. For instance, the following code would remove the dialog's buttons: ```lsl llMessageLinked(LINK_SET, 0, "", "fw_delbox : ButtonOK"); llMessageLinked(LINK_SET, 0, "", "fw_delbox : ButtonCancel"); ``` You can also delete multiple boxes at once. The following code yields the same result: ```lsl llMessageLinked(LINK_SET, 0, "", "fw_delbox : ButtonOK : ButtonCancel"); ``` Important: You cannot delete the "root" boxes of the display sets ("Dialog" and "Table" in this example).


**### Touch queries The example we used in the last chapter contains parts of the text that the user should be able to touch on the object and get some response, namely the buttons of the "dialog" and the up/down buttons right of our table. The FURWARE text script can be queried about which box** has been touched and at **what coordinates**, given the prim and face number that has been touched. The script will automatically take into account the correct translation into coordinates relative to the box, the correct ordering and any overlap between boxes.

#### Performing a query

Let's take a look at the touch_start()-handler in our script and how it can send a "fw_touchquery" to the FURWARE text script:

```lsl touch_start(integer numDetected) { string link = (string)llDetectedLinkNumber(0); string face = (string)llDetectedTouchFace(0); llMessageLinked(LINK_SET, 0, "Some user data", "fw_touchquery:" + link + ":" + face); } ``` As you can see, the last parameter of llMessageLinked() contains the "fw_touchquery" command, the touched link number and face number, all separated by ":". In addition, you may pass an arbitrary string as the third parameter to llMessageLinked(); "Some user data" in this example. This data will be sent back unmodified in the response message. This way you can associate queries with respones.

#### Parsing the reply

The FURWARE text script will **always** reply to such a query, even if something went wrong and it could not make sense of the parameters given in the query (for instance when a prim was touched that is not a display prim).

The "id" parameter of the "link_message()" handler always contains the string "fw_touchreply" so you can quickly distinguish the reply messages from other link messages.

The "str" parameter contains ":"-separated data about the result of the query in the form

*boxName:dx:dy:rootName:x:y:userData*

where

- **boxName** is the name of the box that has been touched.
- **dx** is the column (in characters) of the touch relative to the box's left side.
- **dy** is the row of the touch relative to the box's top side.
- **rootName** is the name of the base box of the display set in which the box resides.
- **x** is the column (in characters) of the touch relative to the display set's left side.
- **y** is the row of the touch relative to the display set's top side.
- **userData** is the string that has been passed as third parameter of "llMessageLinked()" in the touch query.

**Tip:** All fields except for "userData" will be empty if the touch query was invalid (e.g. a prim was touched that is not part of a display).


Here is an example how we could parse a reply in our example: ```lsl link_message(integer sender, integer num, string str, key id) { if (id == "fw_touchreply") { list tokens = llParseStringKeepNulls(str, [":"], []); string boxName = llList2String(tokens, 0); integer dx = llList2Integer(tokens, 1); integer dy = llList2Integer(tokens, 2); string rootName = llList2String(tokens, 3); integer x = llList2Integer(tokens, 4); integer y = llList2Integer(tokens, 5); string userData = llList2String(tokens, 6); if (boxName == "ButtonOK") { llOwnerSay("OK button was clicked."); } else if (boxName == "ButtonCancel") { llOwnerSay("Cancel button was clicked."); } else if (boxName == "UpDown") { // We use the Y coordinate to determine whether "up" or "down" was touched. if (dy == 0) { llOwnerSay("Up button was clicked."); } else if (dy == 2) { llOwnerSay("Down button was clicked."); } } } } ``` ### Style templates Let's say we wish to make the buttons of our dialog a bit more fancy. For instance, we might wish to give them another font and color (in addition to their left and right borders and the centered alignment). We could of course write something like this:

```lsl llMessageLinked(LINK_SET, 0, "border=lr; a=center; c=darkgreen; f=5054fec3-1465-af8f-2fe5-e9507795c82a", "fw_conf : ButtonOK"); llMessageLinked(LINK_SET, 0, "border=lr; a=center; c=darkgreen; f=5054fec3-1465-af8f-2fe5-e9507795c82a", "fw_conf : ButtonCancel"); ``` Although it might not be that bad in this small example, it seems to be a little redundant. If you have more boxes or text passages with styles that you wish to share among boxes, using templates is probably more efficient.

FURWARE text allows you to store string "variables" that you can assign a name. Currently, these variables are only used for style templates. Let's put the above shared style commands into such a variable using the "fw_var" command and give it the name "button":

**```lsl llMessageLinked(LINK_SET, 0, "border=lr; a=center; c=darkgreen; f=5054fec3-1465-af8f-2fe5-e9507795c82a", "fw_var : button"); ``` We may now use this variable in style specifications using the style=...** syntax. Let's rewrite the two "fw_conf" lines from before:

```lsl llMessageLinked(LINK_SET, 0, "style=button", "fw_conf : ButtonOK"); llMessageLinked(LINK_SET, 0, "style=button", "fw_conf : ButtonCancel"); ``` Our dialog then looks like this: You may even mix templates with other style settings (even other templates). For instance, we might want to make the "Cancel" button dark red but keep the other style attributes of the "button" template: ```lsl llMessageLinked(LINK_SET, 0, "style=button; c=darkred", "fw_conf : ButtonCancel"); ``` Tip: You can also use "fw_var" to **change** the contents of an existing variable. Passing the empty string as the variable's contents **deletes** the variable. Note that changing an existing variable will trigger a **complete refresh** of the display because it doesn't know where the variables might be currently in use.


**Important:** Style templates allow recursion (i.e. calling a style template from within another style template). The text script does **not** check for infinite recursion!


### Configuring multiple boxes at once Sometimes you may wish to set the same style or text data for multiple boxes at once. As an example, let us consider the following "game board" that has 9 separate boxes for the "X" and "O" cells: Now let's say that we wish to highlight the middle row like this: To achieve this, we could of course write:

```lsl llMessageLinked(LINK_SET, 0, "c=red", "fw_conf : Cell3"); llMessageLinked(LINK_SET, 0, "c=red", "fw_conf : Cell4"); llMessageLinked(LINK_SET, 0, "c=red", "fw_conf : Cell5"); ``` But this obviously requires three link messages. FURWARE text offers a special syntax that can be used for the "fw_data" and "fw_conf" commands to set text or style data for multiple boxes at once. One possibilty for our example is to specify the names of all boxes that should be configured like so:

**```lsl llMessageLinked(LINK_SET, 0, "c=red", "fw_conf : Cell3 : Cell4 : Cell5"); ``` If we assume that the boxes were added to the display in the order "Cell0", "Cell1", and so on, we can shorten the code even more. We may specify intervals** of boxes that we wish to set using the following syntax (note the semicolon (";") between the box names!):

```lsl llMessageLinked(LINK_SET, 0, "c=red", "fw_conf : Cell3 ; Cell5"); ``` Let's say that we wish to "reset" the game so that all fields to show the "?" symbol like this: To achieve this, we need to reset the color and the text for all fields. We can use the interval notation for both "fw_conf" and "fw_data": ```lsl llMessageLinked(LINK_SET, 0, "", "fw_conf : Cell0 ; Cell8"); llMessageLinked(LINK_SET, 0, "?", "fw_data : Cell0 ; Cell8"); ``` In this concrete example we can even omit one end of the interval: Because "Cell8" is the last box in the display set, we may omit its name and write: ```lsl llMessageLinked(LINK_SET, 0, "", "fw_conf : Cell0 ;"); llMessageLinked(LINK_SET, 0, "?", "fw_data : Cell0 ;"); ``` This means "apply to Cell0 and all following boxes in the same display set".

It is even possible to mix interval- and single-box-notation. Consider the following code (the additional whitespace is just inserted for clarity, you may of course omit it):

**```lsl llMessageLinked(LINK_SET, 0, "!", "fw_data : Cell1;Cell3 : Cell5 : Cell7; "); ``` Applied to the above example board, this yields: Tip:** Please see the reference for a complete overview of all possible parameter notations.


**### Global style settings Some of the style settings of your board may have a "global" nature. For instance, you might wish to always use a certain font for all** boxes and be able to change that setting quickly.

Using the style templates from the last section, we already have a way to give multiple boxes a style that we can later on change centrally (by changing the respective variable using "fw_var"). The **drawback** of this method is that we still need to specify the "style=..." for each box separately and remember to include it again when changing some other style settings specific to a box using "fw_conf".

For such cases, the script offers the "**fw_defaultconf**" command. Using this command, you may set global defaults for **all boxes**, **all root boxes** (i.e. the "base" boxes of each display set) and **all non-root boxes**.

There currently are three variants of the command that can be sent for setting the defaults as mentioned above. Here are examples showing their usage (note the different arguments for "fw_defaultconf:..." command):

```lsl // Sets the default style for all boxes to red, centered. llMessageLinked(LINK_SET, 0, "c=red; a=center", "fw_defaultconf"); // Sets the default style for all ROOT boxes to green, no wrapping. llMessageLinked(LINK_SET, 0, "c=green; w=none", "fw_defaultconf : root"); // Sets the default style for all NON-ROOT boxes to "no trimming". llMessageLinked(LINK_SET, 0, "t=off", "fw_defaultconf : nonroot"); ``` ### Inline styles By now we have used global and per-box style configuration. FURWARE text supports yet another level which is the most fine-grained: Style commands that are placed directly within the text. This allows you to override parts of the current style settings for only parts of your text, for instance to highlight words or align individual lines of text differently.

Such a style command is started by "<!" (note the exclamation mark) and ended by ">". In between those tags, you may specify style commands. As an example, let's make the heading text of our dialog centered, one word within the text randomly colored and make it use a different font:

**```lsl llMessageLinked(LINK_SET, 0, "Some fancy dialog", "fw_data : Dialog"); ``` The result may look something like this (of course, here the color is random each time the dialog is rendered): Take a close look at the result and at the code: We have used a special setting "c=def**" to **restore the normal color** of the text after the word "fancy" but **we have not reset the font** and thus it will stay active for the rest of the text. You may use the special setting "**def**" for any setting (color, font, alignment, etc.) to restore the box's default.

**Tip:** You may also use style templates using the inline formatting command "style".


**Important:** Using "border" settings as an inline style does not have any effect.


**Important:** Alignment, trimming or wrapping settings may only be used immediately at the beginning of a new line (also immediately after each "\n") and will then affect that line and following lines.


#### Selectively disabling inline styles You might want to disable inline styles for parts of your display, for instance when displaying user input where you do not want the "<!" to be interpreted as the start of style data. Curiously enough, the command for doing this is a style setting itself, namely "tags=off". After it has been parsed, further "<!" tags will be ignored. As an example, the following command disables inline styles for the contents of our "Dialog":

**```lsl llMessageLinked(LINK_SET, 0, "border=tblr; tags=off", "fw_conf : Dialog"); ``` You can even use this setting in an inline fashion, but only at the beginning of new lines (similar to alignment, etc.). Then this line and all** following lines will ignore inline styles (indeed there is no way to enable them again using an inline command).

---

## Subpage: Reference

- 1 Reference manual - 1.1 Commands - 1.1.1 fw_data & fw_conf - 1.1.2 fw_defaultconf - 1.1.3 fw_var - 1.1.4 fw_addbox - 1.1.5 fw_delbox - 1.1.6 fw_touchquery - 1.1.7 fw_notify - 1.1.8 fw_memory - 1.1.9 fw_reset - 1.2 Style settings - 1.3 Predefined colors - 1.4 Fonts - 2 Version history ## Reference manual This chapter is meant to be a quick overview of pretty much everything necessary to use FURWARE text, especially which names and parameters go where. It is not meant to replace the tutorial in any way.

### Commands

#### fw_data & fw_conf

Per-box settings for text (fw_data) and style (fw_conf)

```lsl
llMessageLinked(LINK_SET, 0, "Some new text",   "fw_data : BoxSpec : BoxSpec : BoxSpec : ...");
llMessageLinked(LINK_SET, 0, "c=red; a=center", "fw_conf : BoxSpec : BoxSpec : BoxSpec : ...");
```

Each "**BoxSpec**" can have different forms to select different boxes. In the following table, let "BoxOne" and "BoxTwo" be two valid box names in the same display set:

BoxSpec

Meaning

(empty)

All boxes in all sets.

BoxOne

Only the box "BoxOne".

BoxOne ; BoxTwo

All Boxes between* (and including) "BoxOne" and "BoxTwo".

BoxOne ;

"BoxOne" and all following* boxes in the same display set.

; BoxTwo

"BoxTwo" and all preceding* boxes in the same display set.

(*) Depending on the order in which the boxes were added.

#### fw_defaultconf

Sets global style preferences

```lsl
llMessageLinked(LINK_SET, 0, "c=red; a=center", "fw_defaultconf");
llMessageLinked(LINK_SET, 0, "c=red; a=center", "fw_defaultconf : root");
llMessageLinked(LINK_SET, 0, "c=red; a=center", "fw_defaultconf : nonroot");
```

The three variants set the global style preferences for all boxes, all root-boxes and all non-root boxes.

#### fw_var

Store some string data in a "variable" name. Currently only used for style templates.

```lsl
llMessageLinked(LINK_SET, 0, "Some string", "fw_var : varName");
```

Sets the contents of variable "varName" to "Some string". You can delete variables by passing the empty string as data.

#### fw_addbox

Adds a new virtual text box. There can be at most 16 boxes per set (including the root box).

```lsl
llMessageLinked(LINK_SET, 0, "Some initial text", "fw_addbox : boxName : parentName : dx, dy, sx, sy : stylePrefs");
```

Please see the tutorial for details.

#### fw_delbox

Deletes one or more text boxes.

```lsl
llMessageLinked(LINK_SET, 0, "", "fw_delbox : boxOne : boxTwo : ...");
```

Deletes the boxes named "boxOne", "boxTwo", etc.

#### fw_touchquery

Performs a query which box has been touched where.

```lsl
llMessageLinked(LINK_SET, 0, "userData", "fw_touchquery : linkNumber : faceNumber");
```

The reply has the form (pseudo code):

```lsl
link_message(..., ..., "boxName:dx:dy:rootName:x:y:userData", "fw_touchreply") {
    ...
}
```

Please see the tutorial for details.

#### fw_notify

Enable or disable link message notifications when the script has done rendering. Off by default.

```lsl
llMessageLinked(LINK_SET, 0, "on", "fw_notify");
llMessageLinked(LINK_SET, 0, "off", "fw_notify");
```

When notifications are enabled, the text script will send a link message with "id" set to "fw_done" to the whole linkset to let you know when all pending rendering actions have been completed.

#### fw_memory

Tells the owner how much memory is available.

```lsl
llMessageLinked(LINK_SET, 0, "", "fw_memory");
```

#### fw_reset

Performs a full reset on the text script.

```lsl
llMessageLinked(LINK_SET, 0, "", "fw_reset");
```


      **Tip:** When the reset has completed, the script sends a link message with "id" set to "fw_ready" to all prims in the linkset. This tells you when the script is ready to take further commands. **Important:** Only reset the text script if necessary. Initialization is a quite expensive operation and the script will not be available to take commands for a few seconds. ### Style settings Text styles and format settings are specified using special strings. They are used for global and per-box settings ("fw_conf") as well as for specifying styles directly within the text (inline styles). A single setting is given as a **key=value** pair, for example **c=red**. Multiple settings are separated by "**;**", for example **c=red; a=center; w=none**. In the following table: Italic = Default

Setting

Key

Values

Description

Font color

c

R,G,B

Font color as red, green, blue (each in range 0.0-1.0)

R,G,B,A

Font color as red, green, blue, alpha (each in range 0.0-1.0)

rand

Random color (with alpha = 1)

(predefined)

Predefined color, see table below

Alignment

a

*left*

Alignment left

center

Alignment centered

right

Alignment right

Wrapping

w

*word*

Wrap after words, if possible

char

Wrap at any position

none

No wrapping; cuts overlong lines

Trimming

t

*on*

Trims whitespace from beginning and end of lines

off

Keeps whitespace (except with wrap=word)

Font

f

(UUID/name)

Sets the font texture to UUID or name

Borders

border

{trblTRBL12}

Specifies the style of box borders

Style template

style

(Style name)

Uses a style defined using fw_var

Inline styles

tags

*on*

Enables usage of inline styles

off

Disables usage of inline styles

Force refresh

force

on

Enables forced refresh of all faces (disables optimizations!)

*off*

Disables forced refresh of all faces (enables optimizations)

### Predefined colors

You may use the following names in place of color vectors in styles.

**### Fonts You can use the fonts listed here with the "f=...**" style setting either by using their UUID or by putting the corresponding texture item (included in the FURWARE text package) into your object and then use the texture's name.

**## Version history 2.0.1**

- Fixed an issue where characters that are not part of the font texture specification would cause unexpected behavior.
- A box's set pointer is now stored bit-packed together with the rest of its status. This decreases the length of a stride in boxDataList by 1.
- Removed message about free memory on script startup.
- Removed getNumberOfPrims()-function.
- Moved the check if we have any sets at all to the beginning of the link_message()-handler.

**2.0**

- Made the script open source under the MIT license.

**2.0-Beta1**

- The functionality of "fw_data" and "fw_conf" has been reworked to (hopefully) make it more intuitive.
- The commands "fw_data", "fw_conf", and "fw_delbox" are now able to modify multiple boxes at once.
- Added "fw_defaultconf" command. Currently used to configure global style settings.
- Touch replies now also contain the name of the root box and the absolute coordinates.
- Added "force" style attribute to force refresh of all faces (useful for fonts where whitespace is not completely transparent).
- Optimized handling when multiple "similar" commands (e.g. "fw_delbox") come in quickly.

**2.0-Beta0**

- Mesh prims with up to 8 characters per prim, each occupying 0.5 prims
- Virtual text boxes for aligning text arbitrarily
- Style templates for saving format settings

**1.1**

- The developer version now allows distribution of the script as +copy/-trans or -copy/+trans

**1.0.1**

- Improved speed

**1.0**

- First released version

---

## Subpage: Snippets

This page contains several useful code snippets (functions, constants) that can make the usage of FURWARE_text a lot more convenient. - 1 Basic convenience functions - 1.1 Examples - 2 Additional awesomeness - 2.1 Examples ## Basic convenience functions The functions in this section are wrappers around each of the FURWARE text commands. They were designed to follow these rules: - The functions shall be *self-contained*. That is, you may copy any subset of the functions that you need and they will work. - The functions (and their parameters) shall be *self-explanatory*. That is, they also serve as a quick reference guide to the parameters of the commands they execute. The fact that the functions are self-contained also means that each of them contains a llMessageLinked(...)-call. The target of this call is set to LINK_SET (the whole linkset). Please change this target accordingly in your scripts, if needed. ```lsl fwSetText(string text) { llMessageLinked(LINK_SET, 0, text, "fw_data"); } fwSetBoxText(string box, string text) { llMessageLinked(LINK_SET, 0, text, "fw_data:" + box); } fwSetStyle(string style) { llMessageLinked(LINK_SET, 0, style, "fw_conf"); } fwSetBoxStyle(string box, string style) { llMessageLinked(LINK_SET, 0, style, "fw_conf:" + box); } fwSetDefaultStyle(string target, string style) { // "target" may be empty, "root" or "nonroot". llMessageLinked(LINK_SET, 0, style, "fw_defaultconf:" + target); } fwSetVariable(string name, string value) { llMessageLinked(LINK_SET, 0, value, "fw_var:" + name); } fwAddBox(string name, string parent, integer x, integer y, integer w, integer h, string text, string style) { llMessageLinked(LINK_SET, 0, text, "fw_addbox: " +name + ":" + parent + ":"+ (string)x + "," + (string)y + "," + (string)w + "," + (string)h + ":" + style); } fwDelBox(string name) { llMessageLinked(LINK_SET, 0, "", "fw_delbox:" + name); } fwTouchQuery(integer linkNumber, integer faceNumber, string userData) { llMessageLinked(LINK_SET, 0, userData, "fw_touchquery:" + (string)linkNumber + ":" + (string)faceNumber); } list fwTouchReply(string replyString) { list tokens = llParseStringKeepNulls(replyString, [":"], []); return [ llList2String(tokens, 0), llList2Integer(tokens, 1), llList2Integer(tokens, 2), llList2String(tokens, 3), llList2Integer(tokens, 4), llList2Integer(tokens, 5), llDumpList2String(llDeleteSubList(tokens, 0, 5), ":") ]; } fwSetNotify(integer enabled) { string s = "off"; if (enabled) s = "on"; llMessageLinked(LINK_SET, 0, s, "fw_notify"); } fwMemory() { llMessageLinked(LINK_SET, 0, "", "fw_memory"); } fwReset() { llMessageLinked(LINK_SET, 0, "", "fw_reset"); } ``` ### Examples The above snippets allow you to use the basic commands more easily, but you may still need to do some manual work, for example when specifying style configuration strings. The following lines give a few assorted examples of calls using the functions. ```lsl // Set the text of all boxes in all sets. fwSetText("Hello world!"); // Set the text of the box "SomeBox". fwSetBoxText("SomeBox", "This is some box!"); // Set the default style of all boxes to color=red, align=center (see the next section how to make this much nicer). fwSetDefaultStyle("", "c=red;a=center"); // Add a box "NewBox" using "ExistingBox" as its parent. fwAddBox("NewBox", "ExistingBox", 2, 2, 10, 5, "Some initial text", ""); // Delete a box. fwDelBox("NewBox"); // Send a touch query from the touch_start(...)-event. touch_start(integer num) { fwTouchQuery(llDetectedLinkNumber(0), llDetectedTouchFace(0), "Arbitrary user data goes here"); } // Parse a touch reply in the link_message(...)-event. link_message(integer sender, integer num, string str, key id) { if (id == "fw_touchreply") { list result = fwTouchReply(str); // The list "result" now contains the reply as [boxName, boxRelativeX, boxRelativeY, rootName, absoluteX, absoluteY, userData]. // "boxName" is empty if the touch query was invalid. } } ``` ## Additional awesomeness The functions in the previous section are wrappers around the FURWARE_text commands, but you still need to write, for instance, style configuration strings yourself and remember the style options and values. The following set of constants and functions help you with that (again, you don't have to copy all of them but just the ones you need to save script memory!). Tip: Note that these constants complement the functions defined above, so make sure to copy the functions you need as well.


```lsl
// === Colors ===

string COLOR_DEFAULT            = "c=def;";

// Grayscales.
string COLOR_WHITE              = "c=white;";
string COLOR_SILVER             = "c=silver;";
string COLOR_GRAY               = "c=gray;";
string COLOR_BLACK              = "c=black;";

// Standard colors.
string COLOR_RED                = "c=red;";
string COLOR_GREEN              = "c=green;";
string COLOR_BLUE               = "c=blue;";
string COLOR_CYAN               = "c=cyan;";
string COLOR_MAGENTA            = "c=magenta;";
string COLOR_YELLOW             = "c=yellow;";

// Dark colors.
string COLOR_DARKRED            = "c=darkred;";
string COLOR_DARKGREEN          = "c=darkgreen;";
string COLOR_DARKBLUE           = "c=darkblue;";
string COLOR_DARKCYAN           = "c=darkcyan;";
string COLOR_DARKMAGENTA        = "c=darkmagenta;";
string COLOR_DARKYELLOW         = "c=darkyellow;";

// Arbitrary RGB (red, green, blue) color.
string fwColorRGB(float red, float green, float blue) {
    return "c=" + (string)red + "," + (string)green + "," + (string)blue + ",1" + ";";
}

// Arbitrary RGBA (red, green, blue, alpha/opacity) color.
string fwColorRGBA(float red, float green, float blue, float alpha) {
    return "c=" + (string)red + "," + (string)green + "," + (string)blue + "," + (string)alpha + ";";
}

// === Alignment ===

string ALIGN_DEFAULT            = "a=def;";
string ALIGN_LEFT               = "a=left;";
string ALIGN_CENTER             = "a=center;";
string ALIGN_RIGHT              = "a=right;";

// === Wrapping ===

string WRAP_DEFAULT             = "w=def;";
string WRAP_WORD                = "w=word;";
string WRAP_CHAR                = "w=char;";
string WRAP_NONE                = "w=none;";

// === Trimming ===

string TRIM_DEFAULT             = "t=def;";
string TRIM_ON                  = "t=on;";
string TRIM_OFF                 = "t=off;";

// === Fonts ===

string FONT_DEFAULT             = "f=def;";
string FONT_ANDALE              = "f=e31ce6e8-4117-7073-6aac-e6503034b4c5;";
string FONT_ANONYMOUS_PRO       = "f=24c4ead5-04cd-1831-5fd9-ec48882e00b1;";
string FONT_ANONYMOUS_PRO_BOLD  = "f=82c4fcac-3990-223c-286d-5bc92a258fbc;";
string FONT_DEJAVU              = "f=f974fdfc-8fbd-2f29-2b38-3c34411c1fcc;";
string FONT_DEJAVU_BOLD         = "f=5054fec3-1465-af8f-2fe5-e9507795c82a;";
string FONT_ENVYCODER           = "f=a2ec2cf0-b207-db51-d4a1-f3f8d6684c07;";
string FONT_FREEFONT            = "f=05f6f69e-8bdf-a824-a2cf-d91c9e371c23;";
string FONT_INCONSOLATA         = "f=867288f9-940e-a7cf-ac7d-5596ea7fb2c5;";
string FONT_LIBERATION          = "f=c992dfc4-0aca-02c8-bc01-8330e6db6f87;";
string FONT_LIBERATION_BOLD     = "f=1494337d-5296-3c43-8f7c-45617448ec9a;";
string FONT_LUXI                = "f=2d8f52d7-2220-2d7a-15b5-e685a9449e5c;";
string FONT_LUXI_BOLD           = "f=03812794-535b-f546-6171-6bec5bf399be;";
string FONT_MONOFUR             = "f=8fc63e35-a18f-e335-3936-e2ca196a944d;";
string FONT_NOVA                = "f=2df8e09d-e1bd-d17f-6bec-b8d713790380;";
string FONT_PROFONT             = "f=45a8e6f6-90e4-299d-d3bc-0bf4dbf170db;";

// === Borders ===

string BORDER_DEFAULT           = "border=def;";

// These are just some examples for common border styles.
string BORDER_ALL_SIDES         = "border=tblr;";
string BORDER_ALL_SIDES_THICK   = "border=tblr1;";
string BORDER_ALL_SIDES_DOUBLE  = "border=tblr2;";
string BORDER_BOTTOM            = "border=b;";
string BORDER_LEFT_RIGHT        = "border=lr;";

// A more general helper function for borders. The side parameters are ordered clockwise, starting on top.
string fwBorder(integer top, integer right, integer bottom, integer left, integer style) {
    string result = "border=";
    if (top)    result += "t"; if (right)  result += "r";
    if (bottom) result += "b"; if (left)   result += "l";
    if (style)  result += (string)style;
    return result + ";";
}

// === Style variables ===

// Loads a style stored in a fw_var(iable).
string fwStyle(string styleVariableName) {
    return "style=" + styleVariableName + ";";
}
```

### Examples

Note that the value of each constant ends with ";". This allows you to simply "+" them together and you still get valid style strings which you may then use wherever you need a style config string. This allows you to write things like this:

```lsl
// Set the color, wrapping and font of all boxes.
fwSetStyle(COLOR_YELLOW + WRAP_NONE + FONT_MONOFUR);

// Set the default style for all boxes.
fwSetDefaultStyle("", COLOR_RED + ALIGN_CENTER);

// Add a box with some style config. We will use a custom RGB color here.
fwAddBox("SomeBox", "ParentBox", 2, 2, 10, 5, "Some initial text", FONT_LUXI + fwColorRGB(0.5, 0.75, 0.0) + BORDER_ALL_SIDES);

// Store a style string in a variable and use it.
fwSetVariable("MyStyle", FONT_MONOFUR + ALIGN_CENTER + BORDER_ALL_SIDES);
fwSetBoxStyle("BoxA", fwStyle("MyStyle"));
fwSetBoxStyle("BoxB", fwStyle("MyStyle"));
```

---

## Subpage: Developers

**This page contains technical information about FURWARE_text and is intended for developers and interested users. Tip:** If you would like to get more info on specific topics, please leave a note on the discussion page. :)


- 1 Terminology and hierarchy of entities - 2 The main data structure for box, set and prim data - 2.1 Box data - 2.2 Set data - 2.3 Prim data - 3 Basic flow of events - 4 The initialization routine - 5 The link_message(...)-handler - 6 The setDirty(...)-function - 6.1 *integer* action - 6.2 *integer* first / last - 6.3 *integer* isConf - 6.4 *integer* newLayerOverrideBits - 6.5 *integer* setIndex - 6.6 *integer* withData - 6.7 *string* data - 7 The refresh()-function - 8 Caching strategies ## Terminology and hierarchy of entities A "set" is a part of a text display consisting of display prims arranged in rows and columns. Each set has a name, usually assigned using the display creator tool. A linkset may contain multiple sets.

A "**box**" is a virtual text box within a set. Each set always has a (root) box of the size of the set. Each box has a name which is assigned via a parameter to the *fw_addbox* command. Additional boxes may be added to a set which are then stacked in layers, depending on the order in which the boxes were added.

**This yields the following relations: - A box is always part of (and fully contained within) a set. - A set consists of one or more prims. - A prim may have multiple faces. - Each face shows one character of text. The textual content of a box is often referred to as the box's "data**" (note that "data" is sometimes also used with a more general meaning).

The text style configuration of a box (or parts of text) is often referred to as (the box's) "**conf**".

## The main data structure for box, set and prim data Most of the information about the geometry and contents of the displays is stored in a few lists. Some lists contain indices ("pointers") to data in other lists. ### Box data - "boxNameList" is a list containing the names of the boxes one after another. The reason for having the box names in a separate list (i.e. not part of "boxDataList", see below) is that the names shall be quickly searchable. For instance, when new text is received, the index of a box given its name must be retrieved. - "boxDataList" is a strided list containing more information about each box. One stride contains: - The box's text content (string). - The box's style configuration (string). - A bit-packed integer containing the box's layer (4 bits), the index of the set the box is part of (8 bits), dirty flags (2 bits), two reserved bits and the layer override bits (16 bits). - The box's geometry (column offset, row offset, width, height) (rotation). ### Set data - "setDataList" is a strided list containing information about each set. One stride contains: - The set's geometry (number of prim columns and rows, face count) (vector). - A pointer to the start of the prim data stored in the "prim*List"-lists (integer). ### Prim data - "primLinkList" contains the link numbers of the prims, ordered by sets, rows and columns. The link numbers are not bit-packed because they shall be quickly searchable, e.g. when performing touch queries. - "primFillList" contains bit-packed integers storing the state of each face on the respective prim. "The state" of a face means whether it is currently known to be showing whitespace or non-whitespace. This information is used as a cache to avoid SetPrimitiveParams-calls when not necessary. - "primLayerList" contains bit-packed integers that store the assignment of faces to layers. The 32 bits of the integer are split into 4 bits for each face and thus each face may be assigned one of 16 different layer IDs. This information is used during rendering to quickly determine which layer a given face of a given prim belongs to. ## Basic flow of events This images is an attempt to visualize the basic flow of events and functions inside FURWARE text when a command that modifies the layout or contents of the display is received. ## The initialization routine To do ## The link_message(...)-handler To do ## The setDirty(...)-function This functions stands between the parsing of commands in link_message(...) and the actual rendering in refresh(...). The parameters are as follows: ### integer action One of the integer constants ACTION_CONTENT, ACTION_ADD_BOX or ACTION_DEL_BOX. This tells us what basic type of action shall be performed (for instance, setting new text is of type ACTION_CONTENT). This type is stored in a global variable and is reset in a call to refresh(...). The reason for storing this information is the delayed refresh mechanism (which is in turn one of the reasons why setDirty(...) was introduced as a buffer between parsing and refreshing in the first place). At the end of setDirty(...), a timer is started with a quite short interval. The timer()-event merely calls refresh() once it fires. However, until then, more link_message(...)-events may be received and parsed which basically allows us to aggregate multiple commands (for instance, setting text for different boxes) before starting an actual refresh. This can yield a huge performance gain in some situations. Note that the timer is not restarted if the last action is already set to something else than 0 which "guarantees" that the timer will fire at some point, even if a constant stream of commands is received. However, there's a catch. If we would just go and postpone all kinds of actions like setting text, styles, variables, adding and deleting boxes, we would end up with a mess and destroyed data structures (think about the details if you like, but it will make your head hurt). This is where the distinction between the different types of operations comes into play. Operations that merely modify the contents of boxes are in some sense compatible to each other and allow us to aggregate them because the indices of the box data lists and layers remain constant during any content modifications and refreshes. Operations that add boxes may also be aggregated, broadly speaking because data will only be appended to some data lists and we can then refresh a batch of newly added boxes at once. Operations that delete boxes may be aggregated and we basically remember which layers have been freed during these operations. After that, we can just sweep through the remaining boxes and refresh the display accordingly. Because mixing these types operations is a bad thing, each time a command is received, the handler checks whether the new operation is compatible with the last type of operation (that is, "last action type == new action type") and if it is not, an immediate refresh is forced before handling the command. Note that only the type of operation needs to be the same, not the exact command; for instance, fw_data and a fw_conf commands are compatible because they are both of type ACTION_CONTENT. Note that the kind of action may also change the operation of the refresh()-function; please see the according section for details. ### integer first / last The interval of box indices to work on. This way we can operate on a whole range of boxes at once. ### integer isConf May be either 0 or 1. Used for determining whether to store given data (if any) as the data or conf of the box(es). Also, if isConf is true, drawing of the border of the box(es) is forced on next refresh because the border style may have changed. ### integer newLayerOverrideBits This is where it gets a little tricky. :) Before we talk about how this value is used, a few facts: This parameter shall only be non-zero when adding or deleting boxes. It is stored bit-packed as part of the status of the box(es) in the boxDataList and is cleared after a refresh() is completed. The value itself is 16 bits long and each bit stands for one of the 16 layers available within a set. A value of 0xFFFF (binary 1111111111111111) thus means "all layers" and a value of 0x4 (binary 0000000000000100) means "layer 2" (counted from 0). The value is used in the draw(...)-function which is called at several places in refresh() to draw a character to a face. Normally, draw(...) fetches the index of the layer that is currently in the foreground at the specified face as well as the layer of the box whose contents shall be drawn. If these two values are not equal, it will reject to update that face because the box to be drawn is not in the foreground. Now if we added or removed a box, the stored information about which layers are in the foreground may change for some faces. This is just what the value of the newLayerOverrideBits tells us. For instance, when a box was added, the bits are set to 0xFFFF. Now when the newly added box is being drawn, the draw(...)-function will see that it is supposed to override any other layer and draw the new box on top. When deleting a box, the logic is similar, however only specific bits will be set and the order of the refresh routine is reversed; also see the section about the refresh()-function. ### integer setIndex Allows us to restrict writing data to boxes that are part of a certain set. A value of -1 means to operate on boxes belonging to any set. ### integer withData Tells us whether the data-parameter (see below) contains data to be stored. This allows us to differentiate between the empty string and "no data given". ### string data Contains either new text content or a new style config string that is to be stored in the boxDataList. ## The refresh()-function The refresh()-function may be seen as the "heart" of the text script. It is either called after some changes have been aggregated or when a refresh needs to be forced during command handling. It basically consists of a loop that iterates through all boxes and checks their "dirty" bit. If a box is marked dirty, its current data (text, style, geometry) is loaded and prepared for drawing. A word on the order of iteration of this outer loop: Normally, the boxes are iterated in the *reverse* order in which they have been added. That means that boxes will be refreshed "top-to-bottom" (with respect to the layers). However, there is an exception: When the type of the last command(s) was ACTION_ADD_BOX (see the "action" parameter of setDirty(...)), the boxes are iterated *in* the order in which they were added to the board (bottom-to-top). This is necessary to correctly update the information which faces currently show what layer (also see the "newLayerOverrideBits" parameter of setDirty(...)).

Back to the main loop and the dirty bit. There are actually two dirty bits: One telling us that the box needs to be refreshed at all and one that the border of the box also needs to be refreshed. For instance, if only the text content of the box was changed – but not its style settings – then there is no need to bother with re-drawing the border.

The text of the box is split into parts (at whitespaces, newlines, style markup tags) and an inner loop iterates through these tokens which prepares lists of character indices and style information given right within the text as markup. Once a row worth of data has been prepared (row = a row of primitives), another small loop renders the text to the faces before data preparation for the next row begins.

After a box has been refreshed, its dirty bits are reset. When all boxes are done, the last action is also reset and (if the notification option is enabled) a "fw_done" message is emitted to the linkset.



## Caching strategies

*To do*

---

## Subpage: TextureCreator

/LSL

## Overview

FURWARE texture creator is a tool for creating font textures for the FURWARE text script from TrueType/OpenType font files. It offers quite flexible configuration options for tweaking per-font and per-symbol options like offsets and scaling. This enables you to create configuration files for specific fonts to fit perfectly for usage with FURWARE text without any additional, manual tweaking of the resulting textures.

The tool is available as a Python 2 script and a pre-compiled package for Windows; see below.

## Documentation

Please see the following subpages for documentation:

Quick start and overview

Script commands and font configuration reference

Download links for the standard FURWARE text fonts

## How to obtain the tool

The Python 2 code is available at [GitHub](http://github.com/furware/text/tree/master/TextureCreator).

Also, there is a pre-compiled package for Windows available from the [FURWARE website](http://www.furware.de/products/text/TextureCreator.zip).