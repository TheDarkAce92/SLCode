---
name: "Resizer multi-prims"
category: "example"
type: "example"
language: "LSL"
description: "All description in first comments of the script. Maybe my English is not so good (I'm French). Hope anyone will understand."
wiki_url: "https://wiki.secondlife.com/wiki/Resizer_multi-prims"
author: ""
first_fetched: "2026-03-18"
last_updated: "2026-03-18"
has_versions: "true"
active_version: "scraped-sl-wiki-2026-03-18"
---

All description in first comments of the script.
Maybe my English is not so good (I'm French). Hope anyone will understand.

Update on october 11th, 2010
Autodetect official LL grids or opensim

Resizer

```lsl
/* =================================================================================== */
/*                                                                                     */
/*                                     Resizer v1.5                                    */
/*                                                                                     */
/* License :                                                                           */
/*   Français                                                                          */
/*      OpenSource. Licence GPL 2 et plus.                                             */
/*      Modification, Copie et Transfert autorisés                                     */
/*      Sous condition de laisser le script en full perm (Modify / Copy / Transfer)    */
/*                                                                                     */
/*   English                                                                           */
/*      OpenSource. License GPL 2 and later.                                           */
/*      Modify, Copy and Transfer allowed if this script stay full perm                */
/*                                                                                     */
/* Auteurs : Christy Mansbridge / Mingyar Ishtari, le 02 octobre 2010                  */
/*                                                                                     */
/* Modifications / Updates :                                                           */
/*  Author : Christy Mansbridge                                                        */
/*  Date   : 11 octobre 2010                                                           */
/*  Detail : Auto detection opensim/LL grids (version 1.4)                             */
/*                                                                                     */
/* Modifications / Updates :                                                           */
/*  Author : Christy Mansbridge                                                        */
/*  Date   : 30 octobre 2010                                                           */
/*  Detail : Limitation déplacement limité à 10m sur opensim (version 1.5)             */
/*                                                                                     */
/*  Author :                                                                           */
/*  Date   :                                                                           */
/*  Detail :                                                                           */
/*                                                                                     */
/* Usage :                                                                             */
/*   Français                                                                          */
/*      À placer dans le prim root (prim coutouré en jaune à l'édition)                */
/*      Cliquer l'objet pour obtention du menu bleu.                                   */
/*      Usage restreint au seul propriétaire.                                          */
/*                                                                                     */
/*   English                                                                           */
/*      Place the script in the root prim of the build.                                */
/*      Click the object to get the blue menu.                                         */
/*      Usage restricted to the owner.                                                 */
/*                                                                                     */
/* Fonctions :                                                                         */
/*   Français                                                                          */
/*      1) Script de redimensionnement d'un objet multi-prims respectant les           */
/*         proportions, en taille et en position, de chaque prim.                      */
/*                                                                                     */
/*      2) Lag minimal puisqu'un seul script par objet (1 à 256 prims)                 */
/*         Possibilité offerte de supprimer le script.                                 */
/*                                                                                     */
/*      3) Communication avec d'autres objets pour synchroniser le redimensionnement   */
/*          Pour permettre cette communication, plusieurs critères douvent être remplis*/
/*              a) L'objet doit être porté ainsi que celui/ceux à synchroniser         */
/*              b) Les objets doivent porter le même nom, à l'exception de la partie   */
/*                 finale séparée du reste par un espace.                              */
/*                 Exemple : Chaussure rouge gauche et Chaussure rouge droite          */
/*                                                                                     */
/*      4) Garantie de la conservation de l'intégrité de l'objet.                      */
/*          a) Si un agrandissement entraine une destruction du build,                 */
/*             Retour automatique à la taille avant agrandissement.                    */
/*                                                                                     */
/*          b) Si l'objet contient au moins un huge prim le script reste inactif.      */
/*             Cette sécurité résevée à la grille officielle SecondLife peut être      */
/*             désactivée pour opensim en passant à TRUE l'affectation de la variable  */
/*             globale iAllowResizeHugePrims.                                          */
/*                                                                                     */
/*      5) Prise en compte automatique des changements de liens (ajout/suppresion de   */
/*         prims ou redimensionnement manuel)                                          */
/*                                                                                     */
/*      6) 18 choix de redimensionnement prédéfinis en pourcentages :                  */
/*          -1, -2, -5, -10, -25, -50, -75,  -85,  -95.                                */
/*          +1, +2, +5, +10, +25, +50, +75, +100, +200,                                */
/*                                                                                     */
/*      7) 3 choix extrèmes : Dimensionnement Minimal, Maximal et par Défaut.          */
/*         La dimension par défaut est celle à l'initialisation du script ou           */
/*         celle affectée par le menu [Set default].                                   */
/*                                                                                     */
/*      8) Détermination de la taille maximale avant déformation de la construction    */
/*         Pour trouver la taille maximale possible, procéder ainsi :                  */
/*              Effectuer des agrandissements à +200% jusqu'à refus de dimensionnement */
/*              Répéter l'opération avec les pourcentages inférieurs, +100% puis +75%  */
/*              puis 50% ... jusqu'à répétition de l'opétation à +1%.                  */
/*              Après un refus de redimensionnement à +1% le script connait la vraie   */
/*              taille maximale.                                                       */
/*                                                                                     */
/*   English                                                                           */
/*      1) Script to resize a multi prims object with conservation of its integrity    */
/*         (size and relative position of each prim).                                  */
/*                                                                                     */
/*      2) Less lag : only 1 script for an object (1 to 256 prims)                     */
/*         Possibility to remove the script by the menu.                               */
/*                                                                                     */
/*      3) Communication with other objects to synchronize resize                      */
/*          To allow communication, objects have to comply with few criteria :         */
/*              a) The object has to be worn, objects to synchronize too.              */
/*              b) Objects have to have same name except last part separated by space  */
/*                 Example : Excelsior shoes Left and Excelsior shoes Right            */
/*                                                                                     */
/*      4) Integrity waranty.                                                          */
/*          a) If after increasing size the build is broken, automatic go back to      */
/*             previous good size.                                                     */
/*                                                                                     */
/*          b) If, at least, one huge prim is in the build, the script is inactive.    */
/*             This security is only for official grid SecondLife and may be bypassed  */
/*             for opensim, affecting TRUE to the iAllowResizeHugePrims global variable*/
/*                                                                                     */
/*      5) Automatic detection of manual scale change and link changes                 */
/*                                                                                     */
/*      6) 18 predefined resize choice in percentage :                                 */
/*          -1, -2, -5, -10, -25, -50, -75,  -85,  -95.                                */
/*          +1, +2, +5, +10, +25, +50, +75, +100, +200,                                */
/*                                                                                     */
/*      7) 3 other choices : Resize to Minimum, Maximum or Default size.               */
/*         The default size is the size at initialisation of the script or the size    */
/*         affected by the blue menu [Set default].                                    */
/*                                                                                     */
/*      8) How to find the real maximum size ?                                         */
/*         To find the real value :                                                    */
/*              Make an increase size by +200% until the script says it fails.         */
/*              Then, repeat this method with +100%, then after with +75% ...          */
/*              After the last increase with +1% the real maximum size is found and    */
/*              stored by the script.                                                  */
/*                                                                                     */
/* =================================================================================== */

integer iAllowResizeHugePrims = -1; // You can force to FALSE on official SecondLife grids and TRUE on opensim
integer iNumberOfPrims;
integer iFirst;
integer iLast;
integer iBcl;
integer iIdx;
integer iDeb;
integer iFin;
integer iSens;
float   fTmp;
vector  vSize;
vector  vPos;
float   fMin;
float   fMax;
float   fFactor;
float   fDefault;
integer iCanalComm = -8547548;
integer iCanalMenu;
integer iEcouteMenu;
integer iMenuOn;
integer iCurrentMenu;
string  sPctM1 = "1";
string  sPctM2 = "2";
string  sPctM3 = "5";
string  sPctP1 = "1";
string  sPctP2 = "2";
string  sPctP3 = "5";
string  sPct;
integer iNbPasses;
integer iHugeUsed;
float   fLimiteMax;
integer iNoMoreMax;
vector  vPos1;
integer iError;
list    lSortPrims;
list    lSizes;
list    lPos;
list    lElem;
list    lName;

// Hack to increase speed of the script (Mono)
Booster()
{
    for( iBcl = 0; iBcl < 5000; iBcl++ );
}

// Function to get size and/or relative position of the current prim
GetSizePos()
{
    vSize = llList2Vector( llGetLinkPrimitiveParams( iBcl, [ PRIM_SIZE ] ), 0 ) * fFactor;

    if( iBcl == iFirst )
    {
        if( llGetAttached() )
// Root prim and object attached to the avatar, position is local
            vPos = llGetLocalPos();
        else
// Root prim and object not attached, position is absolute position
            vPos = llGetRootPosition();
    }
    else
// Child prim, position is relative to the root prim
        vPos = ( ( llList2Vector( llGetLinkPrimitiveParams( iBcl, [ PRIM_POSITION ] ), 0 ) - llGetRootPosition() ) / llGetRootRotation() ) * fFactor;
}

// Function to control if current prim has expected size and relative position
ControlSizePos( vector vRefSize, vector vRefPos )
{
    if( llVecDist( llList2Vector( llGetLinkPrimitiveParams( iBcl, [ PRIM_SIZE ] ), 0 ), vRefSize ) > 0.001 )
        iError = TRUE;
    else if( iBcl != iFirst )
    {
        if( llVecDist( ( llList2Vector( llGetLinkPrimitiveParams( iBcl, [ PRIM_POSITION ] ), 0 ) - llGetRootPosition() ) / llGetRootRotation(),
                       vRefPos ) > 0.001 )
        iError = TRUE;
    }
}

// Function to test resize validity of the current prim, if resize is over stored maximum size
integer TestError()
{
    if( fMax > fLimiteMax )
        ControlSizePos( vSize, vPos );

    return( iError );
}

// Function to control build integrity after resize
ControlBuild( integer iBoost )
{
    if( iBoost )
        Booster();

// No individual error found
// Control of all the build prim after prim
    for( iIdx = iDeb; iIdx != iFin; iIdx += iSens )
    {
        iBcl = llList2Integer( lSortPrims, iIdx );

        ControlSizePos( llList2Vector( lSizes, iIdx ) * fFactor, llList2Vector( lPos, iIdx ) * fFactor );

        if( iError )
        {
            if( iBoost )
                iIdx = iFin - iSens;
            return;
        }
    }
}

// Function to resize (only the size) each prim of the build
ChangeSize( integer iCorrect )
{
    Booster();

    for( iIdx = iDeb; iIdx != iFin; iIdx += iSens )
    {
        iBcl = llList2Integer( lSortPrims, iIdx );
        GetSizePos();

        if( iCorrect )
            vPos /= fFactor;

        llSetLinkPrimitiveParamsFast( iBcl, [ PRIM_SIZE, vSize ] );

        if( TestError() )
            return;
    }
}

// Function to adapt relative position of each prim of the build
ChangePos( integer iCorrect )
{
    Booster();

    for( iIdx = iDeb; iIdx != iFin; iIdx += iSens )
        if( ( iBcl = llList2Integer( lSortPrims, iIdx ) ) != iFirst )
        {
            GetSizePos();
            vPos1 = vPos / fFactor;

            if( iCorrect )
                vSize /= fFactor;

            llSetLinkPrimitiveParamsFast( iBcl, [ PRIM_POSITION, vPos ] );
            llSetLinkPrimitiveParamsFast( iBcl, [ PRIM_POSITION, vPos ] );
            llSetLinkPrimitiveParamsFast( iBcl, [ PRIM_POSITION, vPos ] );

            if( TestError() )
                return;
        }
}

// Function to resize and adapt relative position of each prim of the build
ChangeSizePos()
{
    Booster();

    for( iIdx = iDeb; iIdx != iFin; iIdx += iSens )
    {
        iBcl = llList2Integer( lSortPrims, iIdx );
        GetSizePos();

        llSetLinkPrimitiveParamsFast( iBcl, [ PRIM_SIZE, vSize, PRIM_POSITION, vPos ] );
        llSetLinkPrimitiveParamsFast( iBcl, [ PRIM_POSITION, vPos ] );
        llSetLinkPrimitiveParamsFast( iBcl, [ PRIM_POSITION, vPos ] );

        if( TestError() )
            return;
    }
}

// Function to resize and position each prim to the previous stored good sizes and relative positions after an error
GoBackToGoodSize()
{
    llOwnerSay( "Error, back to previous good size..." );

    sPct = "aborted";

    if( llRound( fFactor * 100.0 ) == 101 )
        iNoMoreMax = TRUE;

    fMin     /= fFactor;
    fMax     /= fFactor;
    iFin      = iDeb - iSens;
    iDeb      = iIdx;
    iSens    *= -1;
    fFactor   = 1.0;
    iNbPasses = 3;

    if( iNoMoreMax )
        fLimiteMax = fMax;

    do
    {
        Booster();
        iError = FALSE;

        for( iIdx = iDeb; iIdx != iFin; iIdx += iSens )
        {
            iBcl = llList2Integer( lSortPrims, iIdx );

            lElem = [ PRIM_SIZE, llList2Vector( lSizes, iIdx ) ];

            if( iBcl != iFirst )
            {
                vPos  = llList2Vector( lPos, iIdx );

                lElem += [ PRIM_POSITION, vPos ];
            }

            llSetLinkPrimitiveParamsFast( iBcl, lElem );
            llSetLinkPrimitiveParamsFast( iBcl, lElem );
            llSetLinkPrimitiveParamsFast( iBcl, lElem );
        }

        ControlBuild( FALSE );
    }
    while( iError && --iNbPasses );

    if( iError )
        llOwnerSay( "Sorry, the build is broken and can't be repaired." );
}

// Function to store size and relative positions of each prim after a successfull resizing
SaveSizePos()
{
    Booster();

    fFactor = 1.0;
    lSizes  = [];
    lPos    = [];

    for( iIdx = 0; iIdx != iNumberOfPrims; iIdx++ )
    {
        iBcl = llList2Integer( lSortPrims, iIdx );
        GetSizePos();

        lSizes += [ vSize ];
        lPos   += [ vPos  ];
    }
}

// Function to resize the build
Resize( integer iMess )
{
// Apply factor of resizing to the min and max size found in the build
    fMin *= fFactor;
    fMax *= fFactor;

    sPct = "done";

    if( fFactor < 1.0 )
    {
// If resize is to decrease the size, we start whith the most distant prims from the root
        iDeb  = llGetListLength( lSortPrims ) - 1;
        iFin  = -1;
        iSens = -1;
    }
    else
    {
// If resize is to increase the size, we start whith the closer prims from the root
        iDeb  = 0;
        iFin  = llGetListLength( lSortPrims );
        iSens = 1;
    }

    iError = FALSE;

    if( fFactor < 0.5 )
// if decrease is more than a factor 2, we start by changing only relative positions
        ChangePos( FALSE );
    else if( fFactor > 2.0 )
// if increase is more than a factor 2, we start by changing only sizes
        ChangeSize( FALSE );
    else
// if factor is less or equal than 2, resize is both size and position
        ChangeSizePos();

    if( ! iError )
    {
        if( fFactor < 0.5 )
// Changing positions is successfull, we change positions
            ChangeSize( TRUE );
        else if( fFactor > 2.0 )
// Changing sizes is successfull, we change sizes
            ChangePos( TRUE );
    }

    if( ! iError )
        ControlBuild( TRUE );

    if( iError )
// Restore the last good size after error
        GoBackToGoodSize();
    else
    {
// Save the sizes and relative positions of each prim
        SaveSizePos();
        if( fMax == 10.0 && ! iAllowResizeHugePrims )
        {
            iNoMoreMax = TRUE;
            fLimiteMax = fMax;
        }
    }

    if( fMax > fLimiteMax )
// New max size found
        fLimiteMax = fMax;

// Start countdown for CHANGED_SCALE event
    llResetTime();

    if( iMess )
    {
// Inform user the resize is finished and call back the menu
        llOwnerSay( "Resize " + sPct + "." );
        Menu();
    }
}

AlreadyAt( integer iMess, string sMess )
{
    if( iMess )
    {
        llOwnerSay( "Already at " + sMess + " size." );
        Menu();
    }
}

// Function to resize to the minimum size
MinimumSize( integer iMess )
{
    if( ( fFactor = 0.01 / fMin ) != 1.0 )
    {
        if( iMess )
        {
            sPct = (string)llRound( ( fFactor - 1.0 ) * 100.0 );
            if( fFactor > 1.0 )
                sPct = "+" + sPct;
            llOwnerSay( "Minimum size (" + sPct + "%)..." );
        }

        Resize( iMess );
    }
    else
        AlreadyAt( iMess, "minimum" );
}

// Function to resize to the maximum size
MaximumSize( integer iMess )
{
    if( ( fFactor = fLimiteMax / fMax ) != 1.0 )
    {
        if( iMess )
        {
            sPct = (string)llRound( ( fFactor - 1.0 ) * 100.0 );
            if( fFactor > 1.0 )
                sPct = "+" + sPct;
            llOwnerSay( "Maximum size (" + sPct + "%)..." );
        }

        Resize( iMess );
    }
    else
        AlreadyAt( iMess, "maximum" );
}

// Function to resize to the default size
DefaultSize( integer iMess )
{
    vSize = llList2Vector( llGetLinkPrimitiveParams( iFirst, [ PRIM_SIZE ] ), 0 );

    if( ( fFactor = fDefault / vSize.x ) != 1.0 )
    {
        if( iMess )
        {
            sPct = (string)llRound( ( fFactor - 1.0 ) * 100.0 );
            if( fFactor > 1.0 )
                sPct = "+" + sPct;
            llOwnerSay( "Default size (" + sPct + "%)..." );
        }

        Resize( iMess );
    }
    else
        AlreadyAt( iMess, "default" );
}

// Close the menu
FinMenu( integer iAlert )
{
    iMenuOn = FALSE;
    llSetTimerEvent( 0.0 );
    llListenRemove( iEcouteMenu );
    if( iAlert )
        llOwnerSay( "Menu timeout." );
}

// Main menu
Menu()
{
    llSetTimerEvent( 30.0 );
    llDialog( llGetOwner(),
              "Resizer action :\n" +
              "Quit : Leave this menu.\n" +
              "Options : Current size becomes default.\n" +
              ">> : Next set of percentages.\n" +
              "Min : Resize to minimum size.\n" +
              "Default : Return to initial size.\n" +
              "Max : Resize to maximum size.",
              [ "Quit", "Options", ">>",
                "-" + sPctM1 + "%", "Min",     "+" + sPctP1 + "%",
                "-" + sPctM2 + "%", "Default", "+" + sPctP2 + "%",
                "-" + sPctM3 + "%", "Max",     "+" + sPctP3 + "%" ],
              iCanalMenu );
}

// Function to return min or max element of vSize vector
float MinMaxVal( integer iOperation )
{
    return( llListStatistics( iOperation, [ vSize.x, vSize.y, vSize.z ] ) );
}

// Initialisation of the script
init()
{
    Booster();

    iNumberOfPrims = llGetNumberOfPrims();
    iFirst         = (integer)( iNumberOfPrims > 1 );
    iLast          = iNumberOfPrims - (integer)( iNumberOfPrims == 1 );

    llOwnerSay( "Searching min/max prim size..." );

    fMin    = 10.0;
    fMax    = 0.01;
    fFactor = 1.0;
    for( iBcl = iFirst; ( fMax <= 10.0 || iAllowResizeHugePrims ) && iBcl <= iLast; iBcl++ )
    {
        GetSizePos();

        if( iBcl == iFirst )
        {
            fDefault = vSize.x;
            lElem = [ 0.0, iFirst ];
        }
        else
            lElem += [ llVecDist( ZERO_VECTOR, vPos ), iBcl ];

        fTmp = MinMaxVal( LIST_STAT_MIN );
        if( fTmp < fMin )
            fMin = fTmp;

        fTmp = MinMaxVal( LIST_STAT_MAX );
        if( fTmp > fMax )
            fMax = fTmp;
    }

    if( fMax > 10.0 && ! iAllowResizeHugePrims )
    {
        iHugeUsed = TRUE;
        llOwnerSay( "Script not active, object uses huge prim." );
    }
    else
    {
        llOwnerSay( "Size range : " + (string)fMin + " -> " + (string)fMax );

        iNoMoreMax = FALSE;
        iHugeUsed  = FALSE;

        llOwnerSay( "Sorting prims..." );

        lElem = llListSort( lElem, 2, TRUE );

        lSortPrims = [];
        for( iBcl = 1; iBcl < llGetListLength( lElem ); iBcl += 2 )
            lSortPrims += [ llList2Integer( lElem, iBcl ) ];

        llOwnerSay( (string)iNumberOfPrims + " prim" + llList2String( [ "", "s" ], (integer)(iNumberOfPrims > 1) ) + " sorted." );

        fLimiteMax = llListStatistics( LIST_STAT_MAX, [ 10.0, fMax ] );

        llOwnerSay( "Storing size/pos of each prim..." );

        SaveSizePos();
    }

    llOwnerSay( "Init. complete." );
}

default
{
    state_entry()
    {
        if( iAllowResizeHugePrims < 0 )
            iAllowResizeHugePrims = (integer)( llSubStringIndex( llGetSimulatorHostname(), ".lindenlab.com" ) < 0 );

        init();
        llListen( iCanalComm, "", NULL_KEY, "" );
    }

    changed( integer iChange )
    {
        if(   ( iChange & CHANGED_LINK  ) ||
            ( ( iChange & CHANGED_SCALE ) &&
              llGetTime() > 5.0 / llList2Float( [ llGetRegionTimeDilation(), 0.01 ],
                                                (integer)( llGetRegionTimeDilation() < 0.01 ) ) ) )
            init();
    }

    listen( integer iChannel, string sName, key kId, string sMess )
    {
        if( iChannel == iCanalMenu )
        {
            llSetTimerEvent(  0.0 );

            if( sMess == ">>" )
            {
                if( (++iCurrentMenu) == 3 )
                    iCurrentMenu = 0;

                if( ! iCurrentMenu )
                {
                    sPctM1 = "1";
                    sPctM2 = "2";
                    sPctM3 = "5";
                    sPctP1 = "1";
                    sPctP2 = "2";
                    sPctP3 = "5";
                }
                else if( iCurrentMenu == 1 )
                {
                    sPctM1 = "10";
                    sPctM2 = "25";
                    sPctM3 = "50";
                    sPctP1 = "10";
                    sPctP2 = "25";
                    sPctP3 = "50";
                }
                else
                {
                    sPctM1 = "75";
                    sPctM2 = "85";
                    sPctM3 = "95";
                    sPctP1 = "75";
                    sPctP2 = "100";
                    sPctP3 = "200";
                }

                Menu();
            }
            else if( sMess == "Options" || sMess == " " )
            {
                llSetTimerEvent( 30.0 );
                llDialog( llGetOwner(),
                          "\nResizer options :\n \n" +
                          "Quit : Leave this menu.\n" +
                          "BACK : To main menu.\n" +
                          "Set default : Current size is default.\n" +
                          "Remove : Remove the script.",
                          [ "Quit", " ", "BACK",
                            "Set default", " ", "Remove" ],
                          iCanalMenu );
            }
            else if( sMess == "BACK" )
                Menu();
            else if( sMess == "Set default" )
            {
                vSize = llList2Vector( llGetLinkPrimitiveParams( iFirst, [ PRIM_SIZE ] ), 0 );
                fDefault = vSize.x;

                if( llGetAttached() )
                    llSay( iCanalComm, (string)llGetOwner() + "|Default|" + (string)fDefault );

                llOwnerSay( "This size is now the default size." );
                Menu();
            }
            else if( sMess == "Remove" )
            {
                llSetTimerEvent( 30.0 );
                llDialog( llGetOwner(),
                          "\nSure to remove the script from this object ?",
                          [ "Yes", "No" ],
                          iCanalMenu );
            }
            else if( sMess == "Default" )
                DefaultSize( TRUE );
            else if( sMess == "Min" )
                MinimumSize( TRUE );
            else if( sMess == "Max" )
                MaximumSize( TRUE );
            else if( ( iBcl = llListFindList( [ "+", "-" ], [ llGetSubString( sMess, 0, 0 ) ] ) ) >= 0 )
            {
                fFactor = 1.0 + (float)llGetSubString( sMess, 0, -2 ) / 100.0;
                fTmp    = llList2Float( [ llList2Float( [ 10.0, 10000.0 ], iAllowResizeHugePrims ), fLimiteMax ], iNoMoreMax );

                if( fMin * fFactor < 0.01 )
                    fFactor = 0.01 / fMin;
                else if( fMax * fFactor > fTmp )
                    fFactor = fTmp / fMax;

                if( fMin * fFactor >= 0.01 && fMax * fFactor <= fTmp && llRound( fFactor * 100.0 ) != 100 )
                {
                    sPct = (string)llRound( ( fFactor - 1.0 ) * 100.0 ) + "%";
                    if( fFactor > 1.0 )
                        sPct = "+" + sPct;
                    llOwnerSay( llList2String( [ "Increas", "Reduc" ], iBcl ) + "ing size : " +
                                sPct + llList2String( [ " (" + sMess + " asked)", "" ], (integer)(sMess == sPct) ) + "..." );

                    if( llGetAttached() )
                        llSay( iCanalComm, (string)llGetOwner() + "|Factor|" + (string)fFactor );

                    Resize( TRUE );
                }
                else
                {
                    llOwnerSay( "Out of size range." );
                    Menu();
                }
            }
            else
            {
                FinMenu( FALSE );

                if( sMess == "Yes" )
                {
                    if( llGetAttached() )
                        llSay( iCanalComm, (string)llGetOwner() + "|Remove" );
                    llRemoveInventory( llGetScriptName() );
                }
            }
        }
        else if( llGetAttached() && sName != llGetObjectName() )
        {
            lElem = llParseString2List( sName, [ " " ], [ "" ] );
            if( llGetListLength( lElem ) < 2 )
                return;
            lName = llParseString2List( llGetObjectName(), [ " " ], [ "" ] );
            if( llGetListLength( lName ) < 2 )
                return;

            if( llDumpList2String( llList2List( lElem, 0, -2 ), " " ) !=
                llDumpList2String( llList2List( lName, 0, -2 ), " " ) )
                return;

            lElem = llParseString2List( sMess, [ "|" ], [ "" ] );

            if( llList2String( lElem, 0 ) == (string)llGetOwner() )
            {
                if( llList2String( lElem, 1 ) == "Remove" )
                    llRemoveInventory( llGetScriptName() );
                else if( llList2String( lElem, 1 ) == "Factor" )
                {
                    fFactor = llList2Float( lElem, 2 );
                    Resize( FALSE );

                    llResetTime();
                }
                else if( llList2String( lElem, 1 ) == "Min" )
                    MinimumSize( FALSE );
                else if( llList2String( lElem, 1 ) == "Max" )
                    MaximumSize( FALSE );
                else if( llList2String( lElem, 1 ) == "Default" )
                {
                    if( llGetListLength( lElem ) == 2 )
                        DefaultSize( FALSE );
                    else
                        fDefault = llList2Float( lElem, 2 );
                }
            }
        }
    }

    timer()
    {
        FinMenu( TRUE );
    }

    touch_start( integer iNum )
    {
        if( llDetectedKey( 0 ) == llGetOwner() && ! iMenuOn && ! iHugeUsed )
        {
//llOwnerSay( (string)llGetFreeMemory() );
            iMenuOn = TRUE;
            iCanalMenu = iCanalComm - 10 - (integer)llFrand( 124578 );
            iEcouteMenu = llListen( iCanalMenu, "", llGetOwner(), "" );
            Menu();
        }
    }
}
```