dv.execute(`
LIST
FROM "Comps"
FLATTEN file.outlinks as f
WHERE f = ${dv.current().file.link}
GROUP BY file.link
`);