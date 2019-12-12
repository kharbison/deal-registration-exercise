const assert = require('chai').assert
const pgp = require('pg-promise')()

process.env.DEAL_REG_DB_URL = 'postgresql://postgres@localhost:5432/TestDB'

const model = require('../server/models/deal-registration.js')

describe('Testing Get Reg Entry Method', function () {
  describe('Get Reg Entry', function () {
    before(async function () {
      try {
        await model.db.none('DROP IF EXISTS tbl_deal_reg')
        await model.db.one('INSERT INTO tbl_deal_reg(part_num, deal_reg_group, active_flag, end_date, part_type) VALUES($1, $2, $3, $4, $5)',
                    ['SWPT000796', 'Service Action', 'Y', new Date('12/31/9999 00:00:00'), 'SW'])
        await model.db.one('INSERT INTO tbl_deal_reg(part_num, deal_reg_group, active_flag, end_date, part_type) VALUES($1, $2, $3, $4, $5)',
                    ['SWPT000750', 'IBM Brand', 'N', new Date('12/10/2019 00:00:00'), 'SW'])
      }
      catch(ex) {
        return ex
      }
    })
    it('Finds active part with correct part number', function (done) {
      model.getRegEntry('SWPT000796', (err, entry) => {
        assert(err === null)
        assert(entry.part_num === 'SWPT000796')
        done()
      })
    })
    it('Inactive part is not returned', function (done) {
      model.getRegEntry('SWPT000750', (err, entry) => {
        assert(err.status === 404)
        assert(entry === null)
        done()
      })
    })
    it('Part not found returns Not Found error', function (done) {
      model.getRegEntry('SWPT000723', (err, entry) => {
        assert(err.status === 404)
        assert(entry === null)
        done()
      })
    })
    it('Inavlid part number returns Unprocessable Entry error', function (done) {
      model.getRegEntry('000723', (err, entry) => {
        assert(err.status === 422)
        assert(entry === null)
        done()
      })
    })
  })
})