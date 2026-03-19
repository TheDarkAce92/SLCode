---
name: "HTTP Post request to a PHP server"
category: "example"
type: "example"
language: "LSL"
description: "Second life allows scripts to make requests to a web site."
wiki_url: "https://wiki.secondlife.com/wiki/HTTP_Post_request_to_a_PHP_server"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/LSL

## How to use

Second life allows scripts to make requests to a web site.

The command lets you send Post data to PHP.
The format of the HTTP Post is however a bit tricky.

This library lets you call a PHP page and post as many variables in your call as you want.

On top of that I introduce a little checksum/password system to limit potential abuse.

## How to use

**The second life script**

In the beginning of your script you must copy the xrequest function
and also choose a SECRET_NUMBER and a SECRET_STRING.
In SL you should also make sure that the script is not visible to other people than yourself (this is the default access right).

```lsl
 integer SECRET_NUMBER=123456789;
 string SECRET_STRING="abcdefghi";
 key http_request_id;

xrequest(string url, list l)
{
    integer i;
    string body;
    integer len=llGetListLength(l) & 0xFFFE; // make it even
    for (i=0;i0) body+="&";
        body+=llEscapeURL(varname)+"="+llEscapeURL(varvalue);
    }
    string hash=llMD5String(body+llEscapeURL(SECRET_STRING),SECRET_NUMBER);
    http_request_id = llHTTPRequest(url+"?hash="+hash,[HTTP_METHOD,"POST",HTTP_MIMETYPE,"application/x-www-form-urlencoded"],body);
}
```

To make a call to the function you have to provide 2 parameters:

For example:

xrequest("[http://www.yourserver.com/your_page.php](http://www.yourserver.com/your_page.php)",["parameter1",123,"parameter2","parameter2 value"]);

The first parameter is the address of the webpage which will process your request. I assume, you own a website which supports PHP (about any version).

The second parameter is a list containing the parameters you want to pass to the page.
They will be sent to the page as if they had been type in a WebForm.
The list can be empty [] or contain any number of 'variable name','variable value' pairs.

**The PHP Page**

The php page must contains the function below, if you're a PHP wiz, you also include it inside another file.

Note that the page must be modified to contain your own SECRET_NUMBER.
Your page will then use the function checkHash() to make sure the correct password was used.
If the password is wrong, the page won't run any further.

If the password is right you can then read the content of the parameters using a simple $_POST["parameter_name"]

```lsl
<?php
  // this function tweak slightly urlencode to make it behave exactly like llEscapeURL in Second Life.
  function llEscapeURL($s)
  {
    $s=str_replace(
      array(" ","+","-",".","_"),
      array("%20","%20","%2D","%2E","%5F"),
      urlencode($s));
    return $s;
  }

  // this my main SL page XML-RPC page
  function checkHash()
  {
    global $body;
    $hash=$_GET["hash"];
    $body="";
    $cpt=0;
    $SECRET_NUMBER=123456789;
    $SECRET_STRING="abcdefghi";

    foreach ($_POST as $name => $value) {
      if ($cpt++>0) $body.="&";
      if (get_magic_quotes_gpc()) {
        // $name = stripslashes($name); not a good idea though
        $value = stripslashes($value);
        $_POST[$name]=$value;
      }
      $body.=llEscapeURL($name)."=".llEscapeURL($value);
    }
    $calcHash=md5($body.$SECRET_STRING.':'.$SECRET_NUMBER);
    if ($hash!=$calcHash)
    {
      sleep(2); // slow down the requests
      echo "result=FAIL\nMSG=Invalid request.";
      die;
    }
  }

  checkHash();
  // You can use the parameters here by simply using $_POST["parameter_name"]
  echo "OK";
?>
```

I hope it helps.
Don't hesitate to ask any question to Corto Maltese or improve this page.