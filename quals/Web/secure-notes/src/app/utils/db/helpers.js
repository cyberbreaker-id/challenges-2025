function normalizeResult(rows) {
    if (!Array.isArray(rows)) return rows;
    
    return rows.map(row => {
        if (!row || typeof row !== 'object') return row;
        
        const normalized = Object.create(null);
        
        Object.keys(row).forEach(tableKey => {
            const tableData = row[tableKey];
            if (tableData && typeof tableData === 'object' && !Array.isArray(tableData)) {
                Object.keys(tableData).forEach(key => {
                    normalized[key] = tableData[key];
                });
            }
        });
        
        return normalized;
    });
}

module.exports = { normalizeResult };