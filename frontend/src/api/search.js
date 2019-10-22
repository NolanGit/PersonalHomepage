import axios from 'axios'

let base = ''

export const searchEnginesData = params => { return axios.get(`${base}/search/searchEnginesData`, params).then(res => res.data) }

export const searchEnginesAutoComplete = params => { return axios.post(`${base}/search/searchEnginesAutoComplete`, params).then(res => res.data) }

export const searchEnginesSearch = params => { return axios.post(`${base}/search/searchEnginesSearch`, params).then(res => res.data) }