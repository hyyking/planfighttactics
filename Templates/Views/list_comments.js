dv.execute(`
TABLE patch as Patch, file.cday as Date
FROM "Comments"
WHERE comp = ${dv.current().file.link}
SORT file.cday DESC
`);