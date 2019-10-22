import axios from 'axios'

let base = ''

export const searchEnginesData = params => { return axios.get(`${base}/search/searchEnginesData`, params).then(res => res.data) }