'use strict'

const express = require('express')
const router = express.Router()

const dealRegMod = require('../models/deal-registration')

router.get('/mapping/:pn', (req, res) => {
  dealRegMod.getRegEntry(req.params.pn, (err, entry) => {
    if (err) {
      console.log(err)
      if(err.status !== undefined) {
        res.status(err.status).json({
          errName: err.name,
          errMsg: err.message
        })
      } else {
        res.status(500).json({
          errName: 'Internal Server Error',
          errMsg: 'Internal Server Error'
        })
      }
    } else {
      res.json(entry)
    }
  })
})

module.exports = router
