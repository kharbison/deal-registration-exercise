'use strict'

const express = require('express')
const app = express()
const port = 3000

if (!('DEAL_REG_DB_URL' in process.env)) {
  console.log("Error: DEAL_REG_DB_URL environment error has not been set.")
  process.exit(1)
}
else if (process.env.DEAL_REG_DB_URL == '') {
  console.log('Error: The DEAL_REG_DB_URL environment cannot be and empty string.')
  process.exit(1)
}


// Load routes
var dealReg = require('./routers/deal-registration')

// Mount JSON body parser
app.use(express.json())

app.use(function(req, res, next) {
  res.header('Access-Control-Allow-Origin', '*')
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
  res.header('Access-Control-Allow-Methods', '*')
  next()
})

// Mount the logging middleware
app.use(logRequest)

// Mount the part number search router at /deal-registration
app.use('/deal-registration', dealReg)

// start the http server
app.listen(port, () => {
  console.log(`App listening on port ${port}!`)
})

// define a logging middleware
function logRequest (req, res, next) {
  console.debug(`Received ${req.method} ${req.url}`)
  return next()
}