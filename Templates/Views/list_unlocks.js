dv.execute(`
TABLE WITHOUT ID file.link as Unit, unlock as Condition
FROM "Units"
FLATTEN file.inlinks.file.link as l
WHERE unlock AND l = ${dv.current().file.link}
`);