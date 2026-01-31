
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');


function sanitize_tables(input) {
    let regex = /`/gi;
    let dangerous = input.filter(inp => regex.test(inp));
    let whitelist_tables = ["notes", "folders"]    
    // removing input that contains dangerous and perform whitelisting tables
    let safe = input.filter(i => 
        !dangerous.includes(i) && 
        (whitelist_tables.includes(i) || !whitelist_tables.some(table => i.includes(table)))
    );

    return safe;
}


function sanitize_notes(input) {
    if (!input || typeof input !== 'string') {
        return '';
    }
    
    try {
        const window = new JSDOM('').window;
        const DOMPurify = createDOMPurify(window);
        // removing super duper evil html
        return DOMPurify.sanitize(input, {
            ALLOWED_ATTR: []
        });
    } catch (e) {
        return '';
    }
}

module.exports = {
    sanitize_tables,
    sanitize_notes
};
