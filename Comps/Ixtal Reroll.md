---
tags:
  - "#reroll6"
  - "#AP"
  - "#LooseStreak"
---
## Comp

## Tips

## Reroll

Reroll avec [carry :: [[Bard]]]

* Reroll: Pas mauvais meilleur en winstreak

Peut cashout < 500

## Full Open

Seulement si bonnes quêtes pour cashout > 500

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
WHERE comp = this.file.link
SORT file.cday DESC
```

## History
```dataview
TABLE encounter, placement, patch, date
FROM "Games"
WHERE comp = this.file.link
SORT file.date DESC
```

