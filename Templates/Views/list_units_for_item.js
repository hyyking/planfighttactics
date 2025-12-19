dv.execute(`
TABLE WITHOUT ID file.link as Champion, cost
FROM "Units"
FLATTEN file.outlinks.file as f
WHERE (endswith(f.folder, "Families") AND contains(f.outlinks, ${dv.current().file.link})) OR (f.link = ${dv.current().file.link})
SORT cost ASC
`);