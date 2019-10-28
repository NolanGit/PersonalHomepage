import axios from 'axios'

let base = ''

export const weatherData = params => { return axios.post(`${base}/weather/weatherData`, params).then(res => res.data) }

export const weatherPersonalizedSave = params => { return axios.post(`${base}/weather/weatherPersonalizedSave`, params).then(res => res.data) }