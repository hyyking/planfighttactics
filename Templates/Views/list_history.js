dv.execute(`
TABLE WITHOUT ID file.link as Game, encounter as Encounter, placement as Placement, patch as Patch, date as Date
FROM "Games"
WHERE comp = ${dv.current().file.link}
SORT file.date DESC
`);