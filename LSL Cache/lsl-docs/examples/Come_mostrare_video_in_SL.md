---
name: "Come mostrare video in SL"
category: "example"
type: "example"
language: "LSL"
description: "Avatar | Problemi Risolti | Comunicazione | Comunità | Glossario | Terre e Isole | Multimedia | Navigazione | Oggetti | Video Tutorials | Viewer | Wiki | Miscellanea"
wiki_url: "https://wiki.secondlife.com/wiki/Come_mostrare_video_in_SL"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

/it

Portale di aiuto:

Avatar
| Problemi Risolti
| Comunicazione
| Comunità
| Glossario
| Terre e Isole
| Multimedia
| Navigazione
| Oggetti
| Video Tutorials
| Viewer
| Wiki
| Miscellanea

**Come impostare e avviare uno streaming video in Second Life.**

Questo articolo copre ognuno dei passi necessari dall'encoding del contenuto video al visualizzarlo in Second Life.

- 1 Codificare un Video File

  - 1.1 Impostazioni per Quicktime Pro
- 2 Configurazioni di un Web Server
- 3 Impostazioni per la Land
- 4 Scriptare un Display

  - 4.1 Script di Base per Video Display

## Codificare un Video File

Il video da una qualsiasi sorgente deve prima essere convertito ad un file per computer da qualsiasi fonte esso proviene. Ci sono una varietà di programmi e dispositivi che possono fare questo. Una volta che il video è dentro al computer deve essere codificato in un formato che Quicktime può leggere. Le seguenti sono le impostazioni usate in Quicktime Pro per creare un movie che Second Life può leggere. Ci possono essere altre combinazioni che possono andare bene ma per questo esempio si sono scelte queste:

### Impostazioni per Quicktime Pro

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

A questo punto il programma farà partire l'encoding del video e produrrà un file .MOV. Ora è pronto per essere inserito nel tuo web server.

## Configurazioni di un Web Server

Avrai bisogno di accedere ad un web server, o un normale sito web o un server di streaming specializzato che è configurato per supportare http access. Una volta che il file è inserito determina il suo indirizzo URL. Se puoi vedere il video in Quicktime sul tuo computer usando l'indirizzo URL, ci sono buone possibilità che sarà visibile anche in SL.

## Impostazioni per la Land

Le impostazioni della land per i video richiedono che devi essere un land owner oppure membro di un gruppo che ha i privilegi di impostare i Media per "streammare" video. A questa opzione si può accedere cliccando col destro sulla terra e selezionando il menù About Land. Apri la scheda Media.

Ci sono due oggetti da impostare qua per i video. Una texture che sarà sostituita dal video quando sarà avviato e l'indirizzo URL per il file video. La texture può essere ogni immagine, ma è meglio impostare una texture che indica che un video è disponile. È mia opinione che la texture dovrebbe avvertire che esiste un video così come alcune instruzioni su come avviarlo. Una volta che la texture e l'URL sono impostati sei pronto/a ad avviare lo spettacolo.

Tutti i dispositivi che fanno vedere un video possono solo mostrare l'URL impostato nel Land Media settings. Se un cambiamento è fatto su questo URL tutti i dispositivi video in questa parcella sono immediatamente cambiati. Ogni visitatore non vede la stessa porzione del video che un altro sta guardando. Questo è perchè ogni client è indipendentemente connesso all'URL. Se il video verrà visto usando un display, allora tutti i presenti attrezzati a vederlo lo vedranno allo stesso tempo. Confuso? Io certamente lo ero la prima volta! Guarda l'articolo [Streaming Media](http://secondlife.com/app/help/guides/streamingmedia.php) per maggiori informazioni su come il video è attuato in SL.

## Scriptare un Display

Ci sono numerosi dispositivi "TV" gratuiti e a pagamento (detti video display) disponibili in SL, ma se vuoi creare un tuo display qua ci sono alcuni suggerimenti su come farlo!

La grandezza (larghezza e altezza del display) del video non controlla quanto grande te puoi costruire il tuo display in SL, stabilendo uno standard ratio tra larghezza e altezza. Ogni multiplo di questi numeri avranno il corretto aspetto ratio e mostreranno un video non distorto. Tutto ciò che non è in rapporto di corrispondenza farà sì che il video a schermo sarà allungato o distorto. Una conveniente dimensione può essere fatta costruendo il tuo display prim da un cubo impostato a X=2.0, Y=1.5 (questo valori sono quattro volte 0.5m unità di larghezza e tre 0.5m unità di altezza!) Il valore di z può essere impostato a qualunque profondità sia necessaria al vostro dispositivo. Queste misure fanno risultare il display rivolto verso l'alto. La superfice del display avrà il suo punto iniziale (0, zero) allo zero del cubo. questo è importante per avere una corretta orientazione così la tua texture non sia dal lato sbagliato! Rimuovere ogni texture sulla faccia zero e impostarla ad un colore grigio scuro o nero. Questo farà apparire il Tv come spento. Ora sei pronto un semplice script che farà partire il movie!

### Script di Base per Video Display

Il seguente script verrà eseguito, ma presto lo troverai scomodo da usare. È solo un esempio per illustrare questi comandi:

llParcelMediaQuery()

Fa ottenere le impostazioni della Land media per il video.

llSetPrimitiveParams()

Mostra il video su una superficie facendo apparire il dispositivo acceso o spento.

llParcelMediaCommandList()

Controllare attivazione del media stream attraverso il TV.

**Code:** Basic video display script

```lsl
// Questo script dovrebbe essere usato nel prim che mostrerà il video sulla superfice zero.
// Toccando il prim farà partire o fermerà il video display impostato nella Land.

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

**NOTA:** L'uso del ErrMsg texture è un utile promemoria se il TV non può funzionare a causa di autorizzazioni non disponibili per il proprietario. Questo è il testo usato in bianco su blue:

```lsl
  You are not a land owner or land group member; or parcel does not have media set. Cannot connect to parcel media.
```

Questo dà un'idea di base sul perchè il video non parte.