import axios from 'axios'

let base = ''

export const consoleGet = params => { return axios.get(`${base}/console/get`, params).then(res => res.data) }