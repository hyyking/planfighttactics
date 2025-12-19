dv.execute(`
TABLE unlock
FROM "Units"
FLATTEN file.inlinks.file.link as l
WHERE unlock AND l = ${dv.current().file.link}
`);