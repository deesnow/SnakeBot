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
    - [1.4.1](#141)

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
Amikor nagyon sok karaktereden történt változás, de csak egy speciális csapatot (5 kari, egy teljes squad) szeretnél megnézni, akkor van lehetőség egy filter megadására. Filter létrehozásához a Guild-ben valakinek rendelkezni kell a megfelelő Discord joggal (role; jelenleg ez Master). A filter-ek adminisztrációjáról külön szekcióban beszélek majd [itt].

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



### 1.4.1
