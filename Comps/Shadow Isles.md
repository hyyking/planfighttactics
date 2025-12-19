---
tags:
  - "#AP"
  - "#fast8"
---
1. Augment Viego (pas essayé)
2. Vrmt tempo avec quickstricker



## Comments
```dataview
TABLE patch as Patch, file.cday as Date
FROM "Comments"
WHERE comp = [[Shadow Isles]]
SORT file.cday
```
## History
```dataview
TABLE encounter, placement, patch, date
FROM "Games"
WHERE comp = "Shadow Isles"
SORT file.date DESC
```
