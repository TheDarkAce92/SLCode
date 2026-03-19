---
name: "llBreakAllLinks"
category: "function"
type: "function"
language: "LSL"
description: 'Delinks all prims in the link set.

To run this function the script must request the PERMISSION_CHANGE_LINKS permission with llRequestPermissions and it must be granted by the owner.'
signature: "void llBreakAllLinks()"
return_type: "void"
sleep_time: ""
energy_cost: "10.0"
wiki_url: 'https://wiki.secondlife.com/wiki/llBreakAllLinks'
deprecated: "false"
first_fetched: "2026-03-10"
last_updated: "2026-03-10"
patterns: ["llbreakalllinks"]
---

Delinks all prims in the link set.

To run this function the script must request the PERMISSION_CHANGE_LINKS permission with llRequestPermissions and it must be granted by the owner.


## Signature

```lsl
void llBreakAllLinks();
```


## Caveats

- Energy cost: **10.0**.


## See Also

- [SL Wiki](https://wiki.secondlife.com/wiki/llBreakAllLinks)


<!-- wiki-source -->
_Source: [SL Wiki](https://wiki.secondlife.com/wiki/llBreakAllLinks) — scraped 2026-03-18_

Delinks all prims in the link set.

## Caveats

| Permissions |
| --- |
| - Do not depend upon the auto-grant status of permissions. **Always** use the run_time_permissions event. - If the script lacks the permission PERMISSION_CHANGE_LINKS, the script will shout an error on DEBUG_CHANNEL and the operation fails (but the script continues to run). - If PERMISSION_CHANGE_LINKS is granted by anyone other than the owner, then when the function is called an error will be shouted on DEBUG_CHANNEL. - Once the PERMISSION_CHANGE_LINKS permission is granted there is no way to revoke it except from inside the script (for example, with a new llRequestPermissions call) or the script is reset or deleted. |

- This function fails if the owner does not have edit permissions on the object containing the script, the system message "*Delink failed because you do not have edit permission*" is received by the owner.

## Examples

```lsl
//-- requests permission to change linkes, then breaks all links on touch.
default{
  state_entry(){
    llRequestPermissions( llGetOwner(), PERMISSION_CHANGE_LINKS );
  }

  run_time_permissions( integer vBitPermissions ){
    if (PERMISSION_CHANGE_LINKS & vBitPermissions){
      state sMain;
    }else{
      llResetScript();
    }
  }
}

state sMain{
  touch_start( integer vIntTouched ){
    llBreakAllLinks();
  }
}
```

## See Also

### Events

- **run_time_permissions** — Permission receiving event
- **changed** — CHANGED_LINK

### Functions

- **llGetPermissions** — Get the permissions granted
- **llGetPermissionsKey** — Get the agent who granted permissions
- **llRequestPermissions** — Request permissions
- **llBreakLink** — Break a link
- **llCreateLink** — Link to another object

### Articles

- Script permissions

<!-- /wiki-source -->
