---
name: "Tic Tac Toe"
category: "example"
type: "example"
language: "LSL"
description: "This example will demonstrate how to execute a larger project. Some of the techniques on display here are a little overkill for just coding Tic Tac Toe, but should provide a nice framework for more complex projects."
wiki_url: "https://wiki.secondlife.com/wiki/Tic_Tac_Toe"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

Tic Tac Toe Steps

1. Leaf Objects
1. Root Objects
1. Game Logic part one
1. Version Control
1. Game Logic part two
1. All Scripts on a Single Page

This example will demonstrate how to execute a larger project. Some of the techniques on display here are a little overkill for just coding Tic Tac Toe, but should provide a nice framework for more complex projects.

The game code is expressed in 6 steps.



A working version of this game can found at: [http://slurl.com/secondlife/Longfellow/193/60/25](http://slurl.com/secondlife/Longfellow/193/60/25)

---

## Subpage: Leaf_Objects

Tic Tac Toe Steps

1. Leaf Objects
1. Root Objects
1. Game Logic part one
1. Version Control
1. Game Logic part two
1. All Scripts on a Single Page

It all begins with a cube...

I'm basically a bottom up guy, so I tend to start with the user interface elements first. Of course you need a general idea of what your project is gonna look like when it's done, but it is not worthwhile to spend too much time beyond the general idea. The logic of the project will guide you along, and investing too much time on the grand plan will make you reluctant to change your mind if the evolution of the project seems to indicate a problem.

So, for tic tac toe, it seems like a 3x3 array of cubes mounted on a backboard is a good general idea, so let's start with the cube.

Obviously, we want to be able to display three states: empty, X and O. We could use three textures, but that would be quite wasteful - besides costing L$30, they would all rez separately and make the game slow at the beginning until all the textures are cached.

A much better technique is to use a single texture, displaying only a small part of it at a time using llOffsetTexture. Not only do we save L$20, but the whole texture rezzes once and we only have to go through the fuzzies once.

This is an approximate look of the texture I used:

```lsl
 +--------------------+
 | @@   @@    @@@@@   |
 |  @@ @@    @@   @@  |
 |   @@@     @@   @@  |
 |  @@ @@    @@   @@  |
 | @@   @@    @@@@@   |
 |                    |
 |                    |
 |                    |
 |                    |
 |                    |
 +--------------------+
```

In this example, I chose to use states to represent the three possible - well - states of the cube. The question on when to use states and when to represent state in data can be difficult, but I found the following guidelines to work pretty well:

- Use states when the *event-processing* in each state differs significantly **and** there is not much data to be shared among the states.

- Use data to store the state when event processing remains essentially the same or you need to share data between states anyway.

The reason why event processing matters is because every state gets to have its own event handlers. This is both good and bad. It means you can efficiently ignore events irrelevant to the state by simply not providing a handler, but it also means that if you do provide  a handler, you need to do all the setup work for it - hence the recommendations above.

In practice, the use cases for states are mostly two:

- "leaf" objects with no dependents, so no worries about other objects having to know about your state
- "boot" sequences where you expect to end up in a final, semi-permanent single state.

In our case here, we fall squarely into the first, and since we are definitively a leaf object *and* we do wish to modify our event processing behaviour depending on the state, states are the way to go.

And here's the code going into the cube:

```lsl
// Cached texture positions

float e_pos_s = 0.75;
float e_pos_t = 0.75;

float x_pos_s = 0.75;
float x_pos_t = 0.25;

float o_pos_s = 0.25;
float o_pos_t = 0.25;

integer display_face = 4;

default
{
    state_entry()
    {
        llOffsetTexture(e_pos_s, e_pos_t, display_face);
    }

    touch_start(integer total_number)
    {
        state x;
    }
}

state x
{
    state_entry()
    {
        llOffsetTexture(x_pos_s, x_pos_t, display_face);
    }

    touch_start(integer total_number)
    {
        state o;
    }
}

state o
{
    state_entry()
    {
        llOffsetTexture(o_pos_s, o_pos_t, display_face);
    }

    touch_start(integer total_number)
    {
        state default;
    }
}
```

At this point we're just playing around, and the code doesn't do anything immediately useful, it just cycles through the states on touch.

---

## Subpage: Root_Objects

Tic Tac Toe Steps

1. Leaf Objects
1. Root Objects
1. Game Logic part one
1. Version Control
1. Game Logic part two
1. All Scripts on a Single Page

I know that distributed logic is all the rage, but for a simple project like this, centralized is good. We're going to keep the user interface bits as dumb as possible and have the central controller script decide what happens.

Before we go even further, we need to think a little how the players are going to interact with this game. How are we going to know who is playing and whose turn it is?

When designing these things, try to make things as simple and automatic as possible. Don't make the users go through a sign-in process or other complicated sit-ups. In this game I decided to use the following process:

- a game is *idle* if it hasn't been played in a while or has ended. It can then be reset by clicking on any cube.
- the first player to make a move on a reset game is X
- the second player to make a move is O
- play continues until game ends or times out, after which it becomes idle.

One thing that isn't immediately obvious is that we can't have the X/O cubes make the decision on whether to change state, since they don't have the full information. Only the central controller script can change the states of the X/O cubes. So we need to split off the state change from the touch event handlers and use a message handler to change the states.

So let's talk about messages. This game is going to be one linkset, so we will use link messages. They are actually quite nice as long as you keep good message discipline. In this case we will decide to use the following convention:

```lsl
  llMessageLinked(, , , );
```

Message ids will be constants defined at the beginning of every script we use. We never overload the meaning of a message id - we have more than enough integers to not make this necessary. We avoid encoding data into the message id. The string arg and the key arg provide more than enough space for codes.

Note: Constants are expensive - unfortunately.  Seems like 20 bytes per integer constant, and as the project gets larger it puts you into an unfortunate vicious circle - so *magic numbers* will have to do - but use them only if really needed, and make sure you put a comment next to them.

Let's look at the X/O cube's script. Note the proper way to code a touch event handler. That integer argument getting passed in //is// important, even if in 99% of the cases it will be "1".  It does happen that multiple touch events get packed into one, especially in a competitive game, and ignoring a user action is just about the worst insult you can inflict. So do make the effort of writing that silly while loop.

```lsl
// Locations of various bits on the texture
float e_pos_s = 0.75;
float e_pos_t = 0.75;
float x_pos_s = 0.75;
float x_pos_t = 0.25;
float o_pos_s = 0.25;
float o_pos_t = 0.25;

// Face on which the texture lives
integer display_face = 4;

// Message constants
integer MSG_RESET      = 0;
integer MSG_TOUCH      = 1;
integer MSG_SET_X      = 2;
integer MSG_SET_O      = 3;
integer MSG_IDLE       = 4;
integer MSG_IDLE_TOUCH = 5;

default
{
    state_entry()
    {
        llOffsetTexture(e_pos_s, e_pos_t, display_face);
    }

    touch_start(integer touching_agents)
    {
        while (touching_agents--)
        {
            llMessageLinked(LINK_ROOT, MSG_TOUCH, "", llDetectedKey(touching_agents));
        }
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_SET_X) state x;
        if (msg_id == MSG_SET_O) state o;
        if (msg_id == MSG_IDLE) state idle;
    }
}

state x
{
    state_entry()
    {
        llOffsetTexture(x_pos_s, x_pos_t, display_face);
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_RESET) state default;
        if (msg_id == MSG_IDLE) state idle;
    }
}

state o
{
    state_entry()
    {
        llOffsetTexture(o_pos_s, o_pos_t, display_face);
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_RESET) state default;
        if (msg_id == MSG_IDLE) state idle;
    }
}

state idle
{
    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_RESET) state default;
    }

    touch_start(integer touching_agents)
    {
        llMessageLinked(LINK_ROOT, MSG_IDLE_TOUCH, "", NULL_KEY);
    }
}
```

Note that as long as the game is in progress, there //is// no touch event for the x and o states, thereby trivially avoiding bad touches.

As promised, state changes happen only when the central controller says so...

Another detail: the message sent on an idle touch is different that the touch message in the default state. Since at that point we really do not care who clicked, we omit the while loop.

And now let's look at the central controller script:

```lsl
// Message constants
integer MSG_RESET      = 0;
integer MSG_TOUCH      = 1;
integer MSG_SET_X      = 2;
integer MSG_SET_O      = 3;
integer MSG_IDLE       = 4;
integer MSG_IDLE_TOUCH = 5;

// Game timeout
integer GAME_TIMEOUT = 20;

// Game state
key player_x;
key player_o;

default
{
    state_entry()
    {
        llSay(0, "state default");
        player_x = NULL_KEY;
        player_o = NULL_KEY;
        llMessageLinked(LINK_ALL_CHILDREN, MSG_RESET, "", NULL_KEY);
        state playing;
    }
}

state playing
{
    state_entry()
    {
        llSay(0, "state playing");
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        llSay(0, "from = "+(string)from+" msg_id = "+(string)msg_id);
        if (msg_id == MSG_TOUCH)
        {
            llSay(0, "touch from "+(string)from);
            if (NULL_KEY == player_x)
            {
                player_x = id;
                llSetTimerEvent(GAME_TIMEOUT);
                llMessageLinked(from, MSG_SET_X, "", NULL_KEY);
            }
            else if (NULL_KEY == player_o)
            {
                player_o = id;
                llSetTimerEvent(GAME_TIMEOUT);
                llMessageLinked(from, MSG_SET_O, "", NULL_KEY);
            }
            else if (id == player_x)
            {
                llSetTimerEvent(GAME_TIMEOUT);
                llMessageLinked(from, MSG_SET_X, "", NULL_KEY);
            }
            else if (id == player_o)
            {
                llSetTimerEvent(GAME_TIMEOUT);
                llMessageLinked(from, MSG_SET_O, "", NULL_KEY);
            }
        }
    }

    timer()
    {
        llSetTimerEvent(0);
        state idle;
    }
}

state idle
{
    state_entry()
    {
        llSay(0, "state idle");
        llMessageLinked(LINK_ALL_CHILDREN, MSG_IDLE, "", NULL_KEY);
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_IDLE_TOUCH) state default;
    }
}
```

That one starts with a cut & paste job to import the message constants. Now wouldn't #include be nice here - but hence the rule about these being constants - if later other scripts need more, you only add those you need.

In the previous section we talked about states and when to use them, and here is an example of the other use case for states: a bootstrapping process. Note that during an actual game, we stay in a single state. We only change state when the event behaviour is changing.

Note how we pass along the id of the touchers from the X/O Cube script.

Note how we keep resetting the timeout. In particular, it is necessary to explicitly disable the timer event when leaving a state, since for some reason the timer setting persists and will come and cause trouble when re-entering that state.

No actual game logic is implemented yet, but it should be easy to see where this is going...

At this point, we can simply copy the X/O Cubes to make 9. The script's message will be identifiable by the link number. It is important to remember how those numbers get assigned when you build the object. Essentially, every new object you add to your selection prior to linking will be number one, shifting everyone else up one number. You then select your intended root prim *last*, then execute the link command (ctrl-l).

As your project grows, you may find that link numbers are too fragile, especially if you keep refining the shape of your object. An alternative solution would be to use llGetObjectName() or llGetObjectDesc() to store a symbolic link name and pass it along in your llMessageLinked() calls.

---

## Subpage: Game_Logic_One

Tic Tac Toe Steps

1. Leaf Objects
1. Root Objects
1. Game Logic part one
1. Version Control
1. Game Logic part two
1. All Scripts on a Single Page

Now we're ready to flesh out the game. We get a little stricter in our if else cascade and keep track of who's turn it is. We also record the game state.

```lsl
// Message constants
integer MSG_RESET      = 0;
integer MSG_TOUCH      = 1;
integer MSG_SET_X      = 2;
integer MSG_SET_O      = 3;
integer MSG_IDLE       = 4;
integer MSG_IDLE_TOUCH = 5;

// Game timeout
integer GAME_TIMEOUT = 20;

// Game state
key player_x;
key player_o;
string turn;
string game;

update_game(string player, integer move)
{
    game = llInsertString(llDeleteSubString(game, move, move), move, player);
    llSay(0, "game = "+game);
}

default
{
    state_entry()
    {
        player_x = NULL_KEY;
        player_o = NULL_KEY;
        game = "---------";
        turn = "x";

        llMessageLinked(LINK_ALL_CHILDREN, MSG_RESET, "", NULL_KEY);
        state playing;
    }
}

state playing
{
    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_TOUCH)
        {
            llSay(0, "touch from "+(string)from);
            if (turn == "x" && NULL_KEY == player_x)
            {
                player_x = id;
                update_game(turn, from-2);
                turn = "o";
                llSetTimerEvent(GAME_TIMEOUT);
                llMessageLinked(from, MSG_SET_X, "", NULL_KEY);
            }
            else if (turn == "o" && NULL_KEY == player_o)
            {
                player_o = id;
                update_game(turn, from-2);
                turn = "x";
                llSetTimerEvent(GAME_TIMEOUT);
                llMessageLinked(from, MSG_SET_O, "", NULL_KEY);
            }
            else if (turn == "x" && id == player_x)
            {
                update_game(turn, from-2);
                turn = "o";
                llSetTimerEvent(GAME_TIMEOUT);
                llMessageLinked(from, MSG_SET_X, "", NULL_KEY);
            }
            else if (turn == "o" && id == player_o)
            {
                update_game(turn, from-2);
                turn = "x";
                llSetTimerEvent(GAME_TIMEOUT);
                llMessageLinked(from, MSG_SET_O, "", NULL_KEY);
            }
        }
    }

    timer()
    {
        llSetTimerEvent(0);
        state idle;
    }
}

state idle
{
    state_entry()
    {
        llSay(0, "state idle");
        llMessageLinked(LINK_ALL_CHILDREN, MSG_IDLE, "", NULL_KEY);
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_IDLE_TOUCH) state default;
    }
}
```

A note about data structures... as you know, lsl doesn't have any. All it has is lists and strings. Use strings. Lists are worthless unless you have *wildly* heterogenous data, a need for a little extra speed and not much data:

- Strings are slower, but use memory more efficiently
- Lists are faster, but gobble up memory at an alarming rate

Store constant width fields in constant length records - your strings can be as long as can fit into whatever remains of the 16k allocated to your script.

If you run out of memory, a common technique is to write *data server scripts* with just a tiny query API via linked messages.

Everything is there except for the game end checker. If the game ends by winning, we'd like to highlight the winning squares, which would require adding a message and code to the 9 scripts in the X/O boxes. I guess 9 isn't too bad, but still annoying to have to open 9 inventories, delete and drag in a new verion of the script. It's easy to misclick, and becomes old pretty quick - and there is a better way...

---

## Subpage: Version_Control

Tic Tac Toe Steps

1. Leaf Objects
1. Root Objects
1. Game Logic part one
1. Version Control
1. Game Logic part two
1. All Scripts on a Single Page

So, let's interrupt our quest for the tic tac toe game and build a little infrastructure.

Here, I've added two scripts: RootNanny and LinkNanny. The RootNanny listens for a /1 update and starts a remote upload of a predetermined list of scripts onto the linked prims.

```lsl
// Message constants
integer MSG_RESET = 0;
integer MSG_LINK_QUERY = 10;
integer MSG_LINK_REPLY = 11;

// Globals to propagate
string version = "1.4";
integer pin = 321;

// State
integer current_link_nr;

// Stuff to send out
list remote_scripts = [ "TouchDisplay", "LinkNanny" ];

request_next_object_id(integer link_nr)
{
    // Send message, transmitting pin, hoping to get back objectid
    llMessageLinked(link_nr, MSG_LINK_QUERY, (string)pin, NULL_KEY);

    // Set timer in case link isn't replying
    llSetTimerEvent(2); // 2 secs seems generous
}

default
{
    state_entry()
    {
        string name = llGetObjectName();
        integer space = llSubStringIndex(name, " v");
        if (space < 0) llSetObjectName(name + " v" + version);
        else llSetObjectName(llDeleteSubString(name, space+2, -1) + version);
        llListen(1, "", llGetOwner(), "update");
    }

    listen(integer channel, string name, key id, string message)
    {
        state uploading;
    }
}

state uploading
{
    state_entry()
    {
        current_link_nr = llGetNumberOfPrims();
        // Check if it's more than one
        if (1 < current_link_nr)
        {
            // avatars sitting on us get added at the end, so subtract...
            while (llGetAgentSize(llGetLinkKey(current_link_nr)))
                --current_link_nr;
            request_next_object_id(current_link_nr);
        }
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (from == current_link_nr && msg_id == MSG_LINK_REPLY)
        {
            llSetTimerEvent(0); // Cancel timeout
            integer i;
            for (i = 0; i < llGetListLength(remote_scripts); ++i)
            {
                string script = llList2String(remote_scripts, i);
                llSay(0, "Uploading '"+script+"' to link nr "+(string)current_link_nr);
                llRemoteLoadScriptPin(id, script, pin, TRUE, 0);
            }
            current_link_nr--;
            if (1 < current_link_nr)
            {
                request_next_object_id(current_link_nr);
            }
            else
            {
                llSay(0, "Done uploading remote scripts.");
                state default;
            }
        }
    }

    timer()
    {
        llSay(0, "Failed to receive reply from link nr "+(string)current_link_nr);
        current_link_nr--;
        if (1 < current_link_nr)
        {
            request_next_object_id(current_link_nr);
        }
        else
        {
            llSay(0, "Done uploading remote scripts.");
            state default;
        }
    }
}
```

The LinkNannys are there to set the remote upload pin and to reply with their object id:

```lsl
// Message constants
integer MSG_RESET = 0;
integer MSG_LINK_QUERY = 10;
integer MSG_LINK_REPLY = 11;

default
{
    state_entry()
    {
        // If we are in the the root prim...
        if (llGetLinkNumber() < 2)
        {
            // ... disable ourselves
            llSetScriptState(llGetScriptName(), FALSE);
            llSleep(2);
        }
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_LINK_QUERY)
        {
            // Set pin given
            llSetRemoteScriptAccessPin((integer)str);
            // Tell caller who we are
            llMessageLinked(from, MSG_LINK_REPLY, "", llGetKey());
        }
    }
}
```

With this structure, we can keep all scripts in the root prim, and the appropriate ones will be replicated to all the remaining prims, greatly simplifying the task of developing those scripts.

For this specific project, this is almost overkill, and could have been done simpler - for example, we don't really need to ask every prim what their object id is, because we can use llGetLinkKey(). But for larger projects, you can use the LinkNannys to return the list of scripts in that prim, and thereby remove the need to keep a mapping of which scripts go where - in this project we just happen to luck out simply because all the linked prims are identical. In most real projects, this is not the case. Also, if you are really paranoid, you would negotiate a separate pin for every upload.

This implementation also illustrates some common idioms and ways to avoid scaling pitfalls as your project gets larger.

Note how we query each link in sequence, the end of every event handler having an llMessageLinked() call to request the next one. This is a common pattern, used to process notecards, email, http requests and much else. Here it is again:

```lsl
state process
{
    state_entry()
    {
        llSetTimerEvent();
        llMessageLinked(......);
    }

    link_message(...)
    {
        // Disable timer
        llSetTimerEvent(0);

        // Process data
        ...
        // exit if we know we're done
        if () state done_processing;

        // Set timeout again
        llSetTimerEvent();
        llMessageLinked(......);
    }

    timer()
    {
        // We didn't get a response
        llSetTimerEvent(0);

        // Error handling - retries, whatever...
        ...
    }
}
```

A naive implementation of this would have simply broadcast the query to all prims and relied on the event queue to stash them and serve them back one by one. This is dangerous as the event queue is of undefined size, and due to the delay involved with running llRemoteLoadScriptPin(), any subsequent replies could easily be flushed out by whatever other events may be traversing your build.

Also note the timeout. Never assume anything is they way you wish it is. In your previous run you could have distributed a script which kills off the LinkNanny, or maybe you just screwed up the LinkNanny" itself... Debugging sucks, so add as many catchers as you can.

Finally, note the code that changes the object name to reflect the current version. In a real product, you would use a separate object to contain an updater which will itself upload the latest version of the scripts onto your build, and having this code in place allows you to see whether the updater was applied.

Two more observations:

The scripts were added as new scripts and not shoehorned into the existing scripts, for two reasons:

1. We want to make it easy to reuse the framework for other projects;
1. We want to preserve full freedom in the application to change state as needed. Note that this allows us to use states to prevent any incorrect processing of multiple "/1 upload" commands.

Maintaining remote scripts in the root prim is convenient, but we don't want them to actually run there. Therefore we place the following *suicide code* at the state_entry handler of the default state in the DisplayTouch and LinkNanny scripts:

```lsl
default
{
    state_entry()
    {
        // If we are in the the root prim...
        if (llGetLinkNumber() < 2)
        {
            // ... disable ourselves
            llSetScriptState(llGetScriptName(), FALSE);
            // ... and sleep to ensure nothing else gets executed
            llSleep(2);
        }
    }

    ...
}
```

One slight drawback of the LinkNanny is that we will need to distribute it one initial time by hand, but we're comforted by the fact that it will be the last time we need to actually open the contents of the linked prims.

---

## Subpage: Game_Logic_Two

Tic Tac Toe Steps

1. Leaf Objects
1. Root Objects
1. Game Logic part one
1. Version Control
1. Game Logic part two
1. All Scripts on a Single Page

Now with our uploader in place, we can add another message to the TouchDisplay script to color them red when we detect three in a row:

```lsl
// Locations of various bits on the texture
float e_pos_s = 0.75;
float e_pos_t = 0.75;
float x_pos_s = 0.75;
float x_pos_t = 0.25;
float o_pos_s = 0.25;
float o_pos_t = 0.25;

// Face on wjich the texture lives
integer DISPLAY_FACE = 4;
vector  RED   = <1,0,0>;
vector  WHITE = <1,1,1>;

// Message constants
integer MSG_RESET      = 0;
integer MSG_TOUCH      = 1;
integer MSG_SET_X      = 2;
integer MSG_SET_O      = 3;
integer MSG_IDLE       = 4;
integer MSG_IDLE_TOUCH = 5;
integer MSG_WIN        = 6;

default
{
    state_entry()
    {
        // If we are in the the root prim...
        if (llGetLinkNumber() < 2)
        {
            // ... disable ourselves
            llSetScriptState(llGetScriptName(), FALSE);
            llSleep(2);
        }

        // Reset color and texture
        llSetColor(WHITE, DISPLAY_FACE);
        llOffsetTexture(e_pos_s, e_pos_t, DISPLAY_FACE);
    }

    touch_start(integer touching_agents)
    {
        while (touching_agents--)
        {
            llMessageLinked(LINK_ROOT, MSG_TOUCH, "", llDetectedKey(touching_agents));
        }
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_SET_X) state x;
        if (msg_id == MSG_SET_O) state o;
        if (msg_id == MSG_IDLE) state idle;
    }
}

state x
{
    state_entry()
    {
        llOffsetTexture(x_pos_s, x_pos_t, DISPLAY_FACE);
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_RESET) state default;
        if (msg_id == MSG_IDLE) state idle;
        if (msg_id == MSG_WIN) llSetColor(RED, DISPLAY_FACE);
    }
}

state o
{
    state_entry()
    {
        llOffsetTexture(o_pos_s, o_pos_t, DISPLAY_FACE);
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_RESET) state default;
        if (msg_id == MSG_IDLE) state idle;
        if (msg_id == MSG_WIN) llSetColor(RED, DISPLAY_FACE);
    }
}

state idle
{
    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_RESET) state default;
    }

    touch_start(integer touching_agents)
    {
        llMessageLinked(LINK_ROOT, MSG_IDLE_TOUCH, "", NULL_KEY);
    }
}
```

We then go into the Controller script and add the logic to detect the game end:

```lsl
// Message constants
integer MSG_RESET      = 0;
integer MSG_TOUCH      = 1;
integer MSG_SET_X      = 2;
integer MSG_SET_O      = 3;
integer MSG_IDLE       = 4;
integer MSG_IDLE_TOUCH = 5;
integer MSG_WIN        = 6;

// Game timeout
integer GAME_TIMEOUT = 20;

// Game state
key player_x;
key player_o;
string turn;
string game;

// Helper function to linearize our 3x3 array
string at(integer u, integer v)
{
    integer p = u*3+v;
    return llGetSubString(game, p, p);
}

// return TRUE if game ends
integer game_ends(string player, integer move)
{
    game = llInsertString(llDeleteSubString(game, move, move), move, player);
    llSay(0, "game = "+game);

    // Check if this made three in a row
    integer u = move / 3;
    integer v = move % 3;
    integer i;
    integer c;

    // check horizontal
    c = 0;
    for (i = 0; i < 3; i++) if (at(i, v) == player) c++;
    if (c == 3)
    {
        // The magic number "2" is needed because the smallest child prim index is 2
        for (i = 0; i < 3; i++) llMessageLinked(2 + 3*i + v, MSG_WIN, "", NULL_KEY);
        return TRUE;
    }

    // check vertical
    c = 0;
    for (i = 0; i < 3; i++) if (at(u, i) == player) c++;
    if (c == 3)
    {
        // The magic number "2" is needed because the smallest child prim index is 2
        for (i = 0; i < 3; i++) llMessageLinked(2 + 3*u + i, MSG_WIN, "", NULL_KEY);
        return TRUE;
    }

    // check if we are on one diagonal
    c = 0;
    if (u == v) for (i = 0; i < 3; i++) if (at(i, i) == player) c++;
    if (c == 3)
    {
        // The magic number "2" is needed because the smallest child prim index is 2
        for (i = 0; i < 3; i++) llMessageLinked(2 + 4*i, MSG_WIN, "", NULL_KEY);
        return TRUE;
    }

    // check if we are on the other diagonal
    c = 0;
    if (u + v == 2) for (i = 0; i < 3; i++) if (at(i, 2-i) == player) c++;
    if (c == 3)
    {
        // Arithmetic has been applied, reconstruction left as an exercise to the reader
        for (i = 0; i < 3; i++) llMessageLinked(4 + 2*i, MSG_WIN, "", NULL_KEY);
        return TRUE;
    }

    // Check if there are any spaces left
    if (llSubStringIndex(game, "-") < 0) return TRUE;

    // Game goes on
    return FALSE;
}

default
{
    state_entry()
    {
        player_x = NULL_KEY;
        player_o = NULL_KEY;
        game = "---------";
        turn = "x";

        llMessageLinked(LINK_ALL_CHILDREN, MSG_RESET, "", NULL_KEY);
        state playing;
    }
}

state playing
{
    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_TOUCH)
        {
            llSay(0, "touch from "+(string)from);
            if (turn == "x" && NULL_KEY == player_x)
            {
                llSetTimerEvent(0);
                llMessageLinked(from, MSG_SET_X, "", NULL_KEY);
                player_x = id;
                if (game_ends(turn, from-2)) state idle; // magic "2" = smallest link prim index
                turn = "o";
                llSetTimerEvent(GAME_TIMEOUT);
            }
            else if (turn == "o" && NULL_KEY == player_o)
            {
                llSetTimerEvent(0);
                llMessageLinked(from, MSG_SET_O, "", NULL_KEY);
                player_o = id;
                if (game_ends(turn, from-2)) state idle; // magic "2" = smallest link prim index
                turn = "x";
                llSetTimerEvent(GAME_TIMEOUT);
            }
            else if (turn == "x" && id == player_x)
            {
                llSetTimerEvent(0);
                llMessageLinked(from, MSG_SET_X, "", NULL_KEY);
                if (game_ends(turn, from-2)) state idle; // magic "2" = smallest link prim index
                turn = "o";
                llSetTimerEvent(GAME_TIMEOUT);
            }
            else if (turn == "o" && id == player_o)
            {
                llSetTimerEvent(0);
                llMessageLinked(from, MSG_SET_O, "", NULL_KEY);
                if (game_ends(turn, from-2)) state idle; // magic "2" = smallest link prim index
                turn = "x";
                llSetTimerEvent(GAME_TIMEOUT);
            }
        }
    }

    timer()
    {
        llSetTimerEvent(0);
        state idle;
    }
}

state idle
{
    state_entry()
    {
        llSay(0, "state idle");
        llMessageLinked(LINK_ALL_CHILDREN, MSG_IDLE, "", NULL_KEY);
    }

    link_message(integer from, integer msg_id, string str, key id)
    {
        if (msg_id == MSG_IDLE_TOUCH) state default;
    }
}
```

Note that we don't have to check all possibilities, but only those which could be made possible by the last move.

We also needed to reorder our handling of incoming touch events slightly to ensure that the event timer is off when we process moves.

Then we type \1 update into the chat and play a couple of games to test.

Done.

Have fun!

---

## Subpage: Summary

Tic Tac Toe Steps

1. Leaf Objects
1. Root Objects
1. Game Logic part one
1. Version Control
1. Game Logic part two
1. All Scripts on a Single Page

The object we are scripting is composed of 9 cubes with an X/O texture pre-set and a back pane prim as the root prim. The link order of the child prims is assumed to be in any sequential reading order (left to right, top to bottom or similar).

- 1 Root Prim

  - 1.1 RootNanny (processes upload requests onto the child prims and manages object name)
  - 1.2 Controller (game logic)
- 2 Child Prims

  - 2.1 LinkNanny (answers queries from the RootNanny and manages the upload pin)
  - 2.2 TouchDisplay (handles clicks, displays game elements)

## Root Prim

The root prim is populated with the scripts below:

### RootNanny (processes upload requests onto the child prims and manages object name)

<lsl>
// Message constants
integer MSG_RESET = 0;
integer MSG_LINK_QUERY = 10;
integer MSG_LINK_REPLY = 11;

// Globals to propagate
string version = "1.5";
integer pin = 321;



// State
integer current_link_nr;

// Stuff to send out
list remote_scripts = [ "TouchDisplay", "LinkNanny" ];

request_next_object_id(integer link_nr)
{

```lsl
   // Send message, transmitting pin, hoping to get back objectid
   llMessageLinked(link_nr, MSG_LINK_QUERY, (string)pin, NULL_KEY);

   // Set timer in case link isn't replying
   llSetTimerEvent(2); // 2 secs seems generous
```

}

default
{

```lsl
   state_entry()
   {
       string name = llGetObjectName();
       integer space = llSubStringIndex(name, " v");
       if (space < 0) llSetObjectName(name + " v" + version);
       else llSetObjectName(llDeleteSubString(name, space+2, -1) + version);
       llListen(1, "", llGetOwner(), "update");
   }
```

```lsl
   listen(integer channel, string name, key id, string message)
   {
       state uploading;
   }
```

}

state uploading
{

```lsl
   state_entry()
   {
       current_link_nr = llGetNumberOfPrims();
       // Check if it's more than one
       if (1 < current_link_nr)
       {
           // avatars sitting on us get added at the end, so subtract...
           while (llGetAgentSize(llGetLinkKey(current_link_nr)))
               --current_link_nr;
           request_next_object_id(current_link_nr);
       }
   }

   link_message(integer from, integer msg_id, string str, key id)
   {
       if (from == current_link_nr && msg_id == MSG_LINK_REPLY)
       {
           llSetTimerEvent(0); // Cancel timeout
           integer i;
           for (i = 0; i < llGetListLength(remote_scripts); ++i)
           {
               string script = llList2String(remote_scripts, i);
               llSay(0, "Uploading '"+script+"' to link nr "+(string)current_link_nr);
               llRemoteLoadScriptPin(id, script, pin, TRUE, 0);
           }
           current_link_nr--;
           if (1 < current_link_nr)
           {
               request_next_object_id(current_link_nr);
           }
           else
           {
               llSay(0, "Done uploading remote scripts.");
               state default;
           }
       }
   }

   timer()
   {
       llSay(0, "Failed to receive reply from link nr "+(string)current_link_nr);
       current_link_nr--;
       if (1 < current_link_nr)
       {
           request_next_object_id(current_link_nr);
       }
       else
       {
           llSay(0, "Done uploading remote scripts.");
           state default;
       }
   }
```

}
</lsl>

### Controller (game logic)

<lsl>
// Message constants
integer MSG_RESET      = 0;
integer MSG_TOUCH      = 1;
integer MSG_SET_X      = 2;
integer MSG_SET_O      = 3;
integer MSG_IDLE       = 4;
integer MSG_IDLE_TOUCH = 5;
integer MSG_WIN        = 6;

// Game timeout
integer GAME_TIMEOUT = 20;

// Game state
key player_x;
key player_o;
string turn;
string game;

string at(integer u, integer v)
{

```lsl
   integer p = u*3+v;
   return llGetSubString(game, p, p);
```

}

// return TRUE if game ends
integer game_ends(string player, integer move)
{

```lsl
   game = llInsertString(llDeleteSubString(game, move, move), move, player);
   llSay(0, "game = "+game);
```

```lsl
   // Check if this made three in a row
   integer u = move / 3;
   integer v = move % 3;
   integer i;
   integer c;

   // check horizontal
   c = 0;
   for (i = 0; i < 3; i++) if (at(i, v) == player) c++;
   if (c == 3)
   {
       for (i = 0; i < 3; i++) llMessageLinked(2 + 3*i + v, MSG_WIN, "", NULL_KEY);
       return TRUE;
   }

   // check vertical
   c = 0;
   for (i = 0; i < 3; i++) if (at(u, i) == player) c++;
   if (c == 3)
   {
       for (i = 0; i < 3; i++) llMessageLinked(2 + 3*u + i, MSG_WIN, "", NULL_KEY);
       return TRUE;
   }

   // check if we are on one diagonal
   c = 0;
   if (u == v) for (i = 0; i < 3; i++) if (at(i, i) == player) c++;
   if (c == 3)
   {
       for (i = 0; i < 3; i++) llMessageLinked(2 + 4*i, MSG_WIN, "", NULL_KEY);
       return TRUE;
   }

   // check if we are on the other diagonal
   c = 0;
   if (u + v == 2) for (i = 0; i < 3; i++) if (at(i, 2-i) == player) c++;
   if (c == 3)
   {
       for (i = 0; i < 3; i++) llMessageLinked(4 + 2*i, MSG_WIN, "", NULL_KEY);
       return TRUE;
   }

   // Check if there are any spaces left
   if (llSubStringIndex(game, "-") < 0) return TRUE;
```

```lsl
   // Game goes on
   return FALSE;
```

}

default
{

```lsl
   state_entry()
   {
       player_x = NULL_KEY;
       player_o = NULL_KEY;
       game = "---------";
       turn = "x";
```

```lsl
       llMessageLinked(LINK_ALL_CHILDREN, MSG_RESET, "", NULL_KEY);
       state playing;
   }
```

}

state playing
{

```lsl
   link_message(integer from, integer msg_id, string str, key id)
   {
       if (msg_id == MSG_TOUCH)
       {
           llSay(0, "touch from "+(string)from);
           if (turn == "x" && NULL_KEY == player_x)
           {
               llSetTimerEvent(0);
               llMessageLinked(from, MSG_SET_X, "", NULL_KEY);
               player_x = id;
               if (game_ends(turn, from-2)) state idle;
               turn = "o";
               llSetTimerEvent(GAME_TIMEOUT);
           }
           else if (turn == "o" && NULL_KEY == player_o)
           {
               llSetTimerEvent(0);
               llMessageLinked(from, MSG_SET_O, "", NULL_KEY);
               player_o = id;
               if (game_ends(turn, from-2)) state idle;
               turn = "x";
               llSetTimerEvent(GAME_TIMEOUT);
           }
           else if (turn == "x" && id == player_x)
           {
               llSetTimerEvent(0);
               llMessageLinked(from, MSG_SET_X, "", NULL_KEY);
               if (game_ends(turn, from-2)) state idle;
               turn = "o";
               llSetTimerEvent(GAME_TIMEOUT);
           }
           else if (turn == "o" && id == player_o)
           {
               llSetTimerEvent(0);
               llMessageLinked(from, MSG_SET_O, "", NULL_KEY);
               if (game_ends(turn, from-2)) state idle;
               turn = "x";
               llSetTimerEvent(GAME_TIMEOUT);
           }
       }
   }
```

```lsl
   timer()
   {
       llSetTimerEvent(0);
       state idle;
   }
```

}

state idle
{

```lsl
   state_entry()
   {
       llSay(0, "state idle");
       llMessageLinked(LINK_ALL_CHILDREN, MSG_IDLE, "", NULL_KEY);
   }

   link_message(integer from, integer msg_id, string str, key id)
   {
       if (msg_id == MSG_IDLE_TOUCH) state default;
   }
```

}
</lsl>

## Child Prims

The child prims all have the same set of scripts:

### LinkNanny (answers queries from the RootNanny and manages the upload pin)

<lsl>
// Message constants
integer MSG_RESET = 0;
integer MSG_LINK_QUERY = 10;
integer MSG_LINK_REPLY = 11;

default
{

```lsl
   state_entry()
   {
       // If we are in the the root prim...
       if (llGetLinkNumber() < 2)
       {
           // ... disable ourselves
           llSetScriptState(llGetScriptName(), FALSE);
           llSleep(2);
       }
   }

   link_message(integer from, integer msg_id, string str, key id)
   {
       if (msg_id == MSG_LINK_QUERY)
       {
           // Set pin given
           llSetRemoteScriptAccessPin((integer)str);
           // Tell caller who we are
           llMessageLinked(from, MSG_LINK_REPLY, "", llGetKey());
       }
   }
```

}
</lsl>

### TouchDisplay (handles clicks, displays game elements)

<lsl>
// Locations of various bits on the texture
float e_pos_s = 0.75;
float e_pos_t = 0.75;
float x_pos_s = 0.75;
float x_pos_t = 0.25;
float o_pos_s = 0.25;
float o_pos_t = 0.25;

// Face on wjich the texture lives
integer DISPLAY_FACE = 4;
vector  RED   = <1,0,0>;
vector  WHITE = <1,1,1>;

// Message constants
integer MSG_RESET      = 0;
integer MSG_TOUCH      = 1;
integer MSG_SET_X      = 2;
integer MSG_SET_O      = 3;
integer MSG_IDLE       = 4;
integer MSG_IDLE_TOUCH = 5;
integer MSG_WIN        = 6;

default
{

```lsl
   state_entry()
   {
       // If we are in the the root prim...
       if (llGetLinkNumber() < 2)
       {
           // ... disable ourselves
           llSetScriptState(llGetScriptName(), FALSE);
           llSleep(2);
       }

       // Reset color and texture
       llSetColor(WHITE, DISPLAY_FACE);
       llOffsetTexture(e_pos_s, e_pos_t, DISPLAY_FACE);
   }
```

```lsl
   touch_start(integer touching_agents)
   {
       while (touching_agents--)
       {
           llMessageLinked(LINK_ROOT, MSG_TOUCH, "", llDetectedKey(touching_agents));
       }
   }

   link_message(integer from, integer msg_id, string str, key id)
   {
       if (msg_id == MSG_SET_X) state x;
       if (msg_id == MSG_SET_O) state o;
       if (msg_id == MSG_IDLE) state idle;
   }
```

}

state x
{

```lsl
   state_entry()
   {
       llOffsetTexture(x_pos_s, x_pos_t, DISPLAY_FACE);
   }
```

```lsl
   link_message(integer from, integer msg_id, string str, key id)
   {
       if (msg_id == MSG_RESET) state default;
       if (msg_id == MSG_IDLE) state idle;
       if (msg_id == MSG_WIN) llSetColor(RED, DISPLAY_FACE);
   }
```

}

state o
{

```lsl
   state_entry()
   {
       llOffsetTexture(o_pos_s, o_pos_t, DISPLAY_FACE);
   }
```

```lsl
   link_message(integer from, integer msg_id, string str, key id)
   {
       if (msg_id == MSG_RESET) state default;
       if (msg_id == MSG_IDLE) state idle;
       if (msg_id == MSG_WIN) llSetColor(RED, DISPLAY_FACE);
   }
```

}

state idle
{

```lsl
   link_message(integer from, integer msg_id, string str, key id)
   {
       if (msg_id == MSG_RESET) state default;
   }
```

```lsl
   touch_start(integer touching_agents)
   {
       llMessageLinked(LINK_ROOT, MSG_IDLE_TOUCH, "", NULL_KEY);
   }
```

}
</lsl>