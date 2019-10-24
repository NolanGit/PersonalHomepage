import axios from 'axios'

let base = ''

export const getWeatherData = params => { return axios.post(`${base}/weather/weatherData`, params).then(res => res.data) }