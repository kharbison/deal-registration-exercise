<template>
  <div class='searchForm'>
    <h3>Deal Registration Group Mapping</h3>
    <br>
    <div>
      <cv-form>
        <cv-text-input
          v-model='partNum'
          v-on:keydown.enter.prevent
          label="Part Number Search"
          helper-text="Enter a part number to get the associated Deal Registration Group"
          placeholder="Part Number">
        </cv-text-input>
        <br>
        <cv-button type="button" v-on:click="getRegGroup">Search</cv-button>
      </cv-form>
    </div>
    <br>
    <div v-if="searchResults.length > 0" class="searchResults">
      <cv-data-table
        :columns="columns" :data="searchResults"  ref="table"></cv-data-table>
      <br>
      <cv-button type="button" v-on:click="clearHistory">Clear History</cv-button>
    </div>
    <div v-else class="noResults">
      <h5>No Results To Display</h5>
    </div>
  </div>
</template>

<script>
import { CvForm, CvTextInput, CvButton, CvDataTable } from '@carbon/vue'

const axios = require('axios')

export default {
  name: 'PartNumberSearch',
  components: {
    CvForm,
    CvTextInput,
    CvButton,
    CvDataTable
  },
  data () {
    return {
      columns: [
        'Part Number',
        'Deal Registratioon Group'
      ],
      searchResults: [],
      partNum: null
    }
  },
  methods: {
    getRegGroup: function () {
      axios
        .get(`${process.env.VUE_APP_API_URL}/deal-registration/mapping/${encodeURIComponent(this.partNum)}`)
        .then(res => {
          this.searchResults.unshift([ res.data.part_num, res.data.deal_reg_group ])
        })
        .catch((err) => {
          if (err) {
            let errorMsg = err.response.data.errMsg
            alert(`Error Trying to get part number ${this.partNum}: ${errorMsg}`)
          }
        })
    },
    clearHistory: function () {
      this.searchResults = []
    }
  }
}
</script>

<style scoped>
.searchForm {
  font-size: 15px;
  margin-top: 5%;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 50px;
  max-width: 50%;
  align-self: center;
}

h3 {
  margin-bottom: 20px;
}

.searchResults, .noResults {
  margin-top: 40px;
}

</style>
