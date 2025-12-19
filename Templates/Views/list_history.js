dv.execute(`
TABLE encounter, placement, patch, date
FROM "Games"
WHERE comp = ${dv.current().file.link}
SORT file.date DESC
`);