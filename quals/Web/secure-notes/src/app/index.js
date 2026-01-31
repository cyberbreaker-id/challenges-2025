const express = require('express');
const session = require('express-session');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

const { dbManager } = require('./utils/database')

app.use(express.static(path.join(__dirname, 'templates')));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(session({
    secret: process.env.SECRET_KEY || "secret",
    resave: false,
    saveUninitialized: false,
    cookie: { httpOnly: true }
}));

const routes = require('./routes');
app.use('/', routes);

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
    console.log(process.env)
    dbManager.migrate();
});