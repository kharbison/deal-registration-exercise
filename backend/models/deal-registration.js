'use strict'

const pgp = require('pg-promise')()
const db = pgp('postgresql://@localhost:5432/DealRegDB')

function getRegEntry(pn, cb) {
  let pattern = new RegExp('^[A-Z]+PT[0-9]+$')
  pn.trim()
  let matchResult = pn.match(pattern)

  if (matchResult !== null) {
    db.any('SELECT * FROM tbl_deal_reg WHERE part_num = $1', pn)
    .then(result => {
      //console.log(result)
      // If a result was found process it to determine if we can send back to the user
      if(result.length !== 0) {
        if(result.length > 1) {
          // This should not happen but in the case it does, an error should be thrown
          let error = new Error('Internal Server Error')
          error.name = 'Internal Server Error'
          error.status = 500
          return cb(error, null)
        }
        // Check that part number is still active
        if(result[0].active_flag === "N"){
          let error = new Error('No active entry for the part number requested was found. Please verify the part number is correct.')
          error.name = 'Not Found'
          error.status = 404
          return cb(error, null)
        }
        // Return part number information if all checks pass
        return cb(null, result[0])
      } else {
        let error = new Error('No entry for the part number requested was found. Please verify the part number is correct.')
        error.name = 'Not Found'
        error.status = 404
        return cb(error, null)
      }
    })
    .catch(error => {
      return cb(error, null)
    })
  } else {
    // Return error if the partnumber given is not in the correct format
    let error = new Error('The part number given was not formated correctly. Please enter a single part number that looks like SWPT000123')
    error.name = 'Unprocessable Entity'
    error.status = 422
    return cb(error, null)
  }
}

module.exports = {
  getRegEntry
}