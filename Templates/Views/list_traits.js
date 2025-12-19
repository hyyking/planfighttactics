dv.execute(`
TABLE WITHOUT ID traits as Trait, length(rows) as Count
FROM "Units"
FLATTEN file.inlinks.file.link as l
WHERE l = ${dv.current().file.link} AND traits
FLATTEN traits
GROUP BY traits
SORT length(rows) DESC
`);