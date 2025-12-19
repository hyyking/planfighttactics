---
tags:
  - "#AP"
  - "#fast8"
---
Opener reroll, ligne AP avec des augments qui donne des rabadons
## Comp

![[Pasted image 20251219115542.png]]
## Tips

Managen sur [carry :: [[Veigar]]] obligatoire
Attackspeed exellent sur [carry :: [[Ziggs]]]

- Push 4 yordles le plus vite possible pour trouver des upgrades en natural.
- Push 6 yordles > 30g possible pour les rerolls
- Push 8 a 0 golds pour 8 yordle, farm des items
- Drop 8 yordle une fois upgrade, kennen 3 star facile avec les dups
## Unlocks
```dataview
TABLE unlock
FROM "Units"
FLATTEN file.inlinks.file.link as l
WHERE unlock != "" AND l = this.file.link
```
## Comments
```dataview
TABLE patch as Patch, file.cday as Date
FROM "Comments"
WHERE comp = [[Yordle Veigar]]
SORT file.cday
```
## History
```dataview
TABLE encounter, placement, patch, date
FROM "Games"
WHERE comp = [[Yordle Veigar]]
```


