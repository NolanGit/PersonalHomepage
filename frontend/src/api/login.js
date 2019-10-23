import axios from 'axios'

let base = ''

export const userLogin = params => { return axios.post(`${base}/login/userLogin`, params).then(res => res.data) }

export const userLoginGetSalt = params => { return axios.post(`${base}/login/userLoginGetSalt`, params).then(res => res.data) }