---
name: "How To Show Video in SL"
category: "example"
type: "example"
language: "LSL"
description: "Avatar | Bug Fixes | Communication | Community | Glossary | Land & Sim | Multimedia | Navigation | Object | Video Tutorials | Viewer | Wiki | Misc"
wiki_url: "https://wiki.secondlife.com/wiki/How_To_Show_Video_in_SL"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Help Portal:

Avatar
| Bug Fixes
| Communication
| Community
| Glossary
| Land & Sim
| Multimedia
| Navigation
| Object
| Video Tutorials
| Viewer
| Wiki
| Misc

- 1 Encoding a Video File

  - 1.1 Quicktime Pro Settings
- 2 Web Server Configurations
- 3 Parcel Settings
- 4 Scripting a Display

  - 4.1 Basic Video Display Script

**How to set up and play streaming video in Second Life.**

This article covers each of the steps from encoding video content to displaying it in Second Life.



      **Tip:** **See "Playing media"** for a less technical, beginner's guide with video tutorials.


## Encoding a Video File

The video from any source must first be converted to a computer file form from whatever source it is in. There are variety of programs and devices that can do this step. Once the video is on the computer it must be encoded in a format that Quicktime can play. These are the settings used in Quicktime Pro to create a movie that Second Life can read. There may be other combinations that can work but these were what worked for this example.

### Quicktime Pro Settings

**Standard Video Compression Settings**

```lsl
 Compression Type: MPEG-4 Video
 Frame Rate: 30 fps
 Key Frames: Every 24 frames

 Data Rate: Restrict to 436 kbits/sec
 Optimized for: Download
 Compressor Quality: Best
```

**Sound Settings**

```lsl
 Format: AAC
 Channels: Stereo (L R)
 Rate: 44.100 kHz
Render Settings:
 Quality: Best
AAC Encoder Settings:
 Target Bit Rate: 64 kbps
```

**Movie Settings**

```lsl
 Video
  Compression: MPEG-4 Video
  Quality: Best
  Bitrate: 436 kbits / sec
  Dimensions: 320 x 240

 Sound
  Format: AAC
  Sample Rate: 44.100 kHz
  Channels: Stereo (L R)
  Bit Rate: 64 kbps
```

**Prepare for Internet Streaming**

```lsl
  Fast Start
```

At this point the program will start encoding the video and will produce an .MOV file. It is now ready to place on your web server.

## Web Server Configurations

You will need to have access to a web server, either a normal website or a specialized streaming server that is configured to support http access. Once the file is in place determine the URL address to access the file. If you can play the video in Quicktime on your computer using the URL address, chances are good it will also play in SL.

## Parcel Settings

To set up land parcel for video requires that you either be a land owner or member of a group that has the privileges to set the Media for streaming video. This option can be accessed by right clicking on the ground in the parcel and selecting the About Land menu. Open the Media Tab.

There are two items to set here for video. A texture that will be replaced by the video when it plays and the URL address for the video file. The texture can be any picture texture, but I find it useful to set a texture that indicates what video is available. It is my opinion that the texture should advertise the video as well as provide some instruction on how to start the program. Once the texture and URL are in place you are ready to start the show.

All devices that can play a video can only display the URL set in the Land Media settings. If any change is made to that URL all playing devices in that parcel are immediately changed. Each visitor does not see the same portion of the video that anyone else may be seeing. This is the result of each client independently connecting to the URL. If the video is started using the display device, all present and equipped to see it will all start seeing it at the same time. Confused? I certainly was at first! See article [Streaming Media](http://secondlife.com/app/help/guides/streamingmedia.php) for more information on how video is implemented in SL.

## Scripting a Display

There are a number of free, and paid, "TV" (or video display) devices available in SL, but if you wanted to create your own display device here are some tips in getting it done!

The size (width and height dimensions not file size) of the video does not control how big you can make your display unit in SL, it establishes a standard ratio between width and height. Any multiple of those numbers will have the correct aspect ratio and will display undistorted video. Anything not matching that ratio will cause the video to display stretched or squished. A convenient size can be made by making your display prim from a cube set to X=2.0, Y=1.5 (This is four 0.5m units by three 0.5m units!) The z value can be set to whatever your device will need for depth. This resulting arrangement has the display facing up. The display surface just happens to be face 0 (zero) of the cube. This is important in having a correct orientation so your picture is not showing sideways! Remove any texture on face zero and set to a dark gray or black color. This will be the "off" setting for the TV. Now you are ready for a bit of simple scripting to start showing the movie!

### Basic Video Display Script

The following script will run but you will soon find it inconvenient to use. It is to illustrate these commands:

llParcelMediaQuery()

Get Land parcel media settings for video

llSetPrimitiveParams()

To display the video on a surface making the device appear to turn on and off.

llParcelMediaCommandList()

To control activating the media stream through the device.

**Code:** Basic video display script

```lsl
// This script would be used in the prim that will show the video on surface zero.
// Touching the prim will start or stop the video display set in Land Media: Video.

// Global Variable declarations
key DefTexture;
vector DefColor;
list data;
key texture;
integer IsPlaying;

default {
    state_entry() {
        DefTexture = llGetTexture(0);                   // Save default texture set on prim surface zero.
        DefColor = llGetColor(0);                       // Save default color of prim surface zero
        IsPlaying = FALSE;                              // Set playing flag to FALSE.
    }

    touch_start(integer total_number) {
        // Read land parcel media settings
        data = llParcelMediaQuery([PARCEL_MEDIA_COMMAND_TEXTURE, PARCEL_MEDIA_COMMAND_URL]);
        texture = (key) llList2String(data, 0);         // Get texture for parcel to display
        if (IsPlaying) {                                // Player has video active
            llParcelMediaCommandList([PARCEL_MEDIA_COMMAND_STOP]);     // Stop streaming to the device.
            llSetPrimitiveParams([PRIM_TEXTURE,0,DefTexture,<1,1,0>,ZERO_VECTOR,0.0,PRIM_COLOR,0,DefColor,1.0,PRIM_FULLBRIGHT,0,TRUE]);
            IsPlaying = FALSE;
        }
        else {                                          // Check if Parcel Video is available
            if (llList2String(data, 0) == "") {         // Not a landowner or land group member error display
                key ErrTexture = llGetInventoryKey("ErrMsg");         // Get texture by name from inventory
                llSetPrimitiveParams([PRIM_TEXTURE,0,ErrTexture,<1,1,0>,ZERO_VECTOR,0.0,PRIM_COLOR,0,<1,1,1>,1.0,PRIM_FULLBRIGHT,0,TRUE]);
            }
            else {                                      // Set texture
                llSetPrimitiveParams([PRIM_TEXTURE,0,texture,<1,1,0>,ZERO_VECTOR,0.0,PRIM_COLOR,0,<1,1,1>,1.0,PRIM_FULLBRIGHT,0,TRUE]);
                llParcelMediaCommandList([PARCEL_MEDIA_COMMAND_PLAY]); // Start media playing to this device
                IsPlaying = TRUE;
            }
        }
    }
}
```

**NOTE:** The use of the ErrMsg texture is is a useful reminder if the device cannot function due to permissions not available to the owner. This is the text I used in white on blue:

```lsl
  You are not a land owner or land group member; or parcel does not have media set. Cannot connect to parcel media.
```

It gives the basic idea as to why the video is not playing.