---
tags:
---
## Comments
```dataview
TABLE patch as Patch, file.cday as Date
FROM "Comments"
WHERE comp = {{title}}
SORT file.cday
```