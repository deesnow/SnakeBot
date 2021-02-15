# SnakeBot - Egy SWGOH Bot a fejlődés követéséhez

Ez a **SnakeBot** rövid ismertetője, mely a SWGOH mobil játékhoz készült. A következőkben megpróbálom bemutatni a SnakeBot működését.
Amennyiben bármivel elakadnál akkor gyere fel a bothoz létrehozott [Fejlesztői Discord Server-re](https://discord.gg/xr9KUmH9) ahol szívesen segítünk.

- [SnakeBot - Egy SWGOH Bot a fejlődés követéséhez](#snakebot---egy-swgoh-bot-a-fejlődés-követéséhez)
- [1. Parancsok](#1-parancsok)
  - [1.1 Help](#11-help)
    - [1.1.1 Alap help megjelenítése](#111-alap-help-megjelenítése)
  - [1.2 Parancs szintaktika](#12-parancs-szintaktika)
  - [snk| RosterMentés vagy sr vagy save| Játékos Discord tag vagy saját magad esetén `me` |Egy mentés név](#snk-rostermentés-vagy-sr-vagy-save-játékos-discord-tag-vagy-saját-magad-esetén-me-egy-mentés-név)
  - [1.3 Játékos Regisztrálása](#13-játékos-regisztrálása)
  - [1.4 Roster Parancsok](#14-roster-parancsok)
    - [1.4.1 RosterMentés](#141-rostermentés)
    - [1.4.2 MentésLista](#142-mentéslista)
    - [1.4.3 MentésTörlés](#143-mentéstörlés)
    - [1.4.4 Fejlődés](#144-fejlődés)
      - [1.4.4.1 Fejlődés lekérdezés filterrel](#1441-fejlődés-lekérdezés-filterrel)
  - [1.5 Guild Parancsok](#15-guild-parancsok)
    - [1.5.1 GuildReport](#151-guildreport)
    - [1.5.2 GuildSave](#152-guildsave)
    - [1.5.3 GuildTörlés](#153-guildtörlés)
  - [1.6 Team Management](#16-team-management)
    - [1.6.1 Karakter keresése](#161-karakter-keresése)
    - [1.6.2 Alias hozzárendelése](#162-alias-hozzárendelése)
    - [1.6.3 Alias eltávolítása](#163-alias-eltávolítása)
    - [1.6.4 Csapat hozzáadása](#164-csapat-hozzáadása)
    - [1.6.5 Csapat törlése](#165-csapat-törlése)
    - [1.6.6 Csapat keresése](#166-csapat-keresése)

# 1. Parancsok

## 1.1 Help

A Bot-ban található egy beépített help. Egyelőre nem túl felhasználó barát, de itt elmagyarázom az értelmezését.

### 1.1.1 Alap help megjelenítése
> `snk help`
```
Guild Parancsok:
  GuildReport    
  GuildSave      
  GuildTörlés   
Regisztráció:
  register       
Roster Parancsok:
  Fejlődés      
  MentésLista   
  MentésTörlés 
  RosterMentés  
Team Management:
  add_alias      
  add_team       
  delete_team    
  list_team      
  pop_alias      
  search_char    
  search_team    
​No Category:
  help           Shows this message

Type snk help command for more info on a command.
You can also type snk help category for more info on a category.
```

## 1.2 Parancs szintaktika

> `snk help RosterMentés`

```
snk [RosterMentés|sr|save] <user> <save_name>
```
Prefix | [Parancs] | <paraméter_1> | <paraméter_2>
-------|---------|-------------|------------
snk| RosterMentés vagy sr vagy save| Játékos Discord tag vagy saját magad esetén `me` |Egy mentés név
-------





Egy helyes parancs a fentiek alapján így nézne ki:

> `snk RosterMentés me 20210210`

vagy
> `snk sr me 20210210`

más részére
> `snk sr @DeeSnow0408 20210210`


## 1.3 Játékos Regisztrálása
Ahhoz hogy érdemben használható legyen a bot a játékost regisztrálni kell.
> `snk [register|reg|r] <user> <ally_code>`

például
> `snk reg @DeeSnow0408 376764962`



## 1.4 Roster Parancsok
A Roster szekció fedi le azokat a parancsokat melyek az egyéni metések készítéséhez, azok litázásához, törléséhez, és az egyéni fejlődés lekérdezéséhez szükségesek.
### 1.4.1 RosterMentés
> `snk [RosterMentés|sr|save] <user> <save_name>`

például
> `snk save me 20210201`


### 1.4.2 MentésLista
> `snk [MentésLista|list|ls] <user>`

például
> `snk list me`

A kapott eredmény valami ilyesmi:
```md
Roster Mentések
Mentett állapotok listája:
**<Mentés név>**
<Mentés dátuma>
--------------------
--------------------
**20200811**
2020-08-10
**20200925**
2020-09-23
**20201030**
2020-10-30
**20210106**
2021-01-06
**20210208**
2021-02-08
Are these droids you are looking for?
```
> A **-gal jelzett sorok a mentés nevek, alatta a mentés dátuma.

### 1.4.3 MentésTörlés
> `snk [MentésTörlés|ds|del] <user> <save>`

például
> `snk del me 20210208`

### 1.4.4 Fejlődés
Az egyik legfontosabb parancs. Ha készítettél egy mentést, és azóta bármely karaktereden bármilyen (csillag, gear, zeta, relic) változás történt akkor ez a parancs megmutatja azt. Érdemes a mentés készítése után várni pár napot, de akár több hetet is hogy érdemben meg tudjuk változás jeleníteni, ugyanakkor ha több hónapra visszamenőleg kérdezel le változást, akkor jó nagy listád lesz. Ennek célirányos szűrűsére alkalmazható egy filter, de erről majd később [itt](#1441-fejlődés-lekérdezés-filterrel)

> `snk [Fejlődés|now|fejlodes] <user> <save1> [filter]`

például
> `snk now me 20210208`

Ahogy a fenti példa is mutatja a `filter`-t nem kötelező megadni.
Az eredmény valami ilyesmi lesz:

```
ROSTER FEJLŐDÉS - 1. OLDAL
A rostereden a következő fejlesztések történtek
-----------------   Lando Calrissian   -----------------
<Level>:                    80 ▶ 85
<Gear>:                      8 ▶  9
----------------   Hoth Rebel Soldier   ----------------
<Csillag>:                   6 ▶  7
------------   Rebel Officer Leia Organa   -------------
<Gear>:                      9 ▶ 10
Are these droids you are looking for?
```

#### 1.4.4.1 Fejlődés lekérdezés filterrel
Amikor nagyon sok karaktereden történt változás, de csak egy speciális csapatot (5 kari, egy teljes squad) szeretnél megnézni, akkor van lehetőség egy filter megadására. Filter létrehozásához a Guild-ben valakinek rendelkezni kell a megfelelő Discord joggal (role; jelenleg ez Master). A filter-ek adminisztrációjáról külön szekcióban beszélek majd [itt](#16-Team-Management).

Első körben nézzük meg a guildben elérhető filtereket:

> `snk [list_team|listteam|lt]`

azaz
> `snk lt`

```ini
Team List:
1. [KAM]  <shaakti, rex, fives, echo, arc>
2. [SLKRPitP1]  <slkr, hux, kru, gat, wat>
3. [SLKRPitP2]  <slkr, daka, zombie, gat, wat>
```
A csapatnevek a [ ]-ben található, míg utána értelemszerűen a csapat található. Ez a csapatnév használható filterként

> `snk now me 20210106 KAM`

Az eredmény pedig csak az adott 5 karakterből azokat tartalmazza, amin változás történt

```
ROSTER FEJLŐDÉS - 1. OLDAL
A rostereden a következő fejlesztések történtek
----------------   CT-21-0408 "Echo"   -----------------
<Relic>:                     2 ▶  6
-----------------   CT-5555 "Fives"   ------------------
<Relic>:                     5 ▶  7
------------------   CT-7567 "Rex"   -------------------
<Relic>:                     2 ▶  5
-------------------   ARC Trooper   --------------------
<Gear>:                     12 ▶ 13
<Relic>:                     0 ▶  6
---------------------   Shaak Ti   ---------------------
<Relic>:                     3 ▶  5
Are these droids you are looking for?
```



## 1.5 Guild Parancsok
A guild parancsok csak Master joggal rendelkezők érhetik el. Itt a teljes guildre kiterjedően lehet mentést készíteni, vagy törölni, illetve fejlődés riportot lekérdezni.

### 1.5.1 GuildReport
A bot a teljes guild minden tagjára kiterjedő riportot generál a megadott mentéshez képest. A riportot DM-ben kapja meg a parancs futtatója excel formátumban. A riportra filter is alkalmazható, azaz a riport lekérhető egy specifikus csapatra.

> `snk [GuildReport|gr] <save_name> [filter]`

például
> `snk gr 20210201 KAM`

Az eredmény excel fileként érkezik.

### 1.5.2 GuildSave
Guild szintű mentés, azaz az aktuális állapotról minden a guildhez tartozó játékosról mentés készül, akkor is ha valaki nincs regisztrálva. Későbbi regisztráció esetén a mentések autómatikusan a regisztrált játékoshoz kapcsolódnak.

> `snk [GuildSave|gs] <save_name>`

például
> `snk gs gs20210210`

```md
Guild adatok lekérdezése folyamatban 
 - Guild adatok letöltve, játékosok roosterének lekérdezése folyamatban 
 - Játékos adatok letöltve, mentések indítása
 - Játékos adatok mentése befejezve
Nem Regisztrált Játékosok:
Regisztráld a felsorolt játékosokat a következő paranccsal:
snk reg <discordUser> <allycode>
-------------------- 1-10 -------------------
[roberto baggio]      ------   [858848128]
[Uruwiel]      -------------   [776341154]
[Hnorbee]      -------------   [639149383]
[Hegzsa]      --------------   [638846191]
[Roffus]      --------------   [587317346]
[Olasz]      ---------------   [414293475]
Are these droids you are looking for?
```

### 1.5.3 GuildTörlés

A parancs segítségével törölhető a nem kívánt vagy már elavult guild szintű mentés.

> `snk [GuildTörlés|gd] <save_name>`

például
> `snk gd gs20210210`

## 1.6 Team Management
A Team Management szekció alatt lévő panacsok segítségével 5 fős squad-ok hozhatók létre. Ezek a csapatok használhatók a [Fejlődés](#144-fejlődés) és a [GuildReport](#151-guildreport) parancsokban mint filter.

### 1.6.1 Karakter keresése
Kerekter ID (eygedi azonosító) keresése azért szükséges, mert csak ehhez tudunk egy általunk használt rövid becenevet (alias-t) hozzárendelni. **A keresésben az első betű mindig nagybetű legyen!**

> `snk [search_char|searchchar|sc] <char>`

például

> `snk sc Revan`

```
1.  DARTHREVAN
 aliases: ['dr']
2.  JEDIKNIGHTREVAN
 aliases: ['jkr']
 ```

 Ha a karakterhez van mér hozzárendelt alias akkor azt a search_char kilistázza. Az egyedi **ID** a sorszám utáni **NAGYBETŰS** név Egy karakterhez több alias is hozzáadható.

 ### 1.6.2 Alias hozzárendelése

 Becenév hozzárendelése

 > `snk [add_alias|aa] <id> <new_alias>`

például
> `snk aa JEDIKNIGHTREVAN jkr`

### 1.6.3 Alias eltávolítása
Rossz vagy nem használt alias törlése

> `snk [pop_alias|pop|pa] <id> <new_alias>`

például
> `snk pop JEDIKNIGHTREVAN jkr`

### 1.6.4 Csapat hozzáadása
Egy csapat létrehozásához szükséged lesz az 5 csapattag alias-ára. Az elő lesz mindig a leader.

> `snk [add_team|addteam|at] <team_name> [ch1] [ch2] [ch3] [ch4] [ch5]`

azaz
> `snk at KAM shaakti rex fives echo arc`

```ini
Team KAM created
 [KAM]  <shaakti, rex, fives, echo, arc>
 ```
### 1.6.5 Csapat törlése

Szükésgtelen csapatok törlése

> `snk [delete_team|deleteteam|dt] <team>`

például
> `snk dt KAM`

```
Team: KAM deleted.
```
### 1.6.6 Csapat keresése
Ha nem akarod az össes csapatot listázni, akkor keresni is tudsz. Elegendő a csapat kezdetét megadni.

> `snk [search_team|searchteam|st] <team>`

például
> `snk st SL`

```
Team 1:
[SLKRPitP1]
= Supreme Leader Kylo Ren =
- Kylo Ren (Unmasked)
- General Hux
- Wat Tambor
- Grand Admiral Thrawn
```



 





