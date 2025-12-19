## Comps
```dataview
TABLE tags
FROM "Comps"
```



## Patch

```dataview
TABLE WITHOUT ID file.link as Patch, patch as SubPatches, notes as "Patch Notes"
FROM "Patches"
```

