import axios from 'axios'

let base = ''

export const userInfo = params => { return axios.post(`${base}/userInfo`, params).then(res => res.data) }