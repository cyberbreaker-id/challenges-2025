
const routes = require('express').Router();
const path = require('path');

const user = require('./user')
const note = require('./notes')
const folder = require('./folders')

routes.get('/', (req, res) => {
  if (req.session.user) {
    res.redirect('/note');
  } else {
    res.sendFile(path.join(__dirname, '../templates/login.html'));
  }
});

routes.use('/user', user)
routes.use('/note', note)
routes.use('/folder', folder)

module.exports = routes;