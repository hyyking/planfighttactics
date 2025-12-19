---
tags:
---
## Comp

## Tips

## Comments
```dataview
TABLE patch as Patch, file.cday as Date
FROM "Comments"
WHERE comp = "{{title}}"
SORT file.cday DESC
```
## History
```dataview
TABLE encounter, placement, patch, date
FROM "Games"
WHERE comp = "{{title}}"
SORT file.date DESC
```
