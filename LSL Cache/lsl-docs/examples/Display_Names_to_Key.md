---
name: "Display Names to Key"
category: "example"
type: "example"
language: "LSL"
description: "default { state_entry() { llListen(101,\"\",\"\",\"\"); } listen(integer c, string n, key id, string message) { if(c == 101) { NAME = message; reqid = llHTTPRequest( URL + \"?name=\" + llEscapeURL(NAME), [..."
wiki_url: "https://wiki.secondlife.com/wiki/Display_Names_to_Key"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

## Library

```lsl
string NAME;
string URL   = "http://cyber.caworks-sl.de/name2key/n2k.php";
string URL2 = "http://www.aga-sl.de/projekte/name2key/n2k.php"; // just in case the URL above should not be working
key reqid;

/// chat: /101

default
{
    state_entry()
    {
        llListen(101,"","","");
    }
    listen(integer c, string n, key id, string message)
    {
        if(c == 101)
        {
            NAME = message;
            reqid = llHTTPRequest( URL + "?name=" + llEscapeURL(NAME), [], "" );
        }
    }
    http_response(key id, integer status, list meta, string body)
    {
        body = llDeleteSubString(body, 0 , llSubStringIndex(body, "
") + 3);
        if ( id != reqid )
        {
            return;
        }
        if ( status == 499 )
        {
            llOwnerSay("timed out");
        }
        else if ( status != 200 )
        {
            llOwnerSay("Server Offline");
        }
        else
        {
            llOwnerSay(NAME + "'s key is: " + body );
        }
    }
}
```



and here the PHP for use on your Server. Name it n2k.php. It also integrates to websites. So you can use it to search from you page.

```lsl

<?php
$username = $_GET["name"];
if($username == "")
{
echo '



';
}
else
{
$uuid = name2Key($username);
echo "
$uuid";
}
    function getPage($web)
	{
		$html = "";
		  $ch = curl_init($web);
		  curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.12) Gecko/20070508 Firefox/1.5.0.12");
		  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		  curl_setopt($ch, CURLOPT_HEADER, 0);
		  curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
		  curl_setopt($ch, CURLOPT_AUTOREFERER, 1);
		  curl_setopt($ch, CURLOPT_TIMEOUT, 5);
		  $html = curl_exec($ch);
		  if(curl_errno($ch))
		  {
			  $html = "";
		  }
		  curl_close ($ch);
		return $html;
	}
    function getBetween($content,$start,$end)
	{
		$a1 = strpos($content,$start);
		$content = substr($content,$a1 + strlen($start));
		while($a2 = strrpos($content,$end))
		{
			$content = substr($content,0,$a2);
		}
		return $content;
	}
    function name2Key($name)
	{
		$SL_SEARCH = 'http://search.secondlife.com/client_search.php?s=People&t=N&q=';
		$sName = split(' ',$name);
		$data = getPage($SL_SEARCH.$sName[0].'%20'.$sName[1]);
		$uuid = getBetween($data,'http://world.secondlife.com/resident/','"');
                if(!preg_match("/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/",$uuid)) $uuid = '00000000-0000-0000-0000-000000000000';
		return $uuid;
	}
?>
```