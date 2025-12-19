---
aliases:
  - IE
---
```dataview
TABLE  f.link
FROM "Units"
FLATTEN file.outlinks.file as f
WHERE (endswith(f.folder, "Families") AND contains(f.outlinks, this.file.link)) OR (f.link = this.file.link)
```





