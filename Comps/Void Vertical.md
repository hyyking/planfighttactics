---
tags:
  - "#AP"
  - "#Guinsoo"
  - "#fast8"
  - "#fast10"
---

Bonne compo pour un solide top 4

## Comp
[carry::[[Kai'Sa]]]
[carry::[[Rift Herald]]]

## Tips

Hard reroll au 8 pour les upgrades

Peut flex un [[Swain]] pour jugg+arcaniste et [[Wukong]] pour bruiser

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