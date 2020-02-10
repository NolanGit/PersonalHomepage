import axios from 'axios'

let base = ''

export const userLogin = params => { return axios.post(`${base}/login/userLogin`, params).then(res => res.data) }

export const userLoginSalt = params => { return axios.post(`${base}/login/userLoginSalt`, params).then(res => res.data) }

export const userChangePassword = params => { return axios.post(`${base}/login/userChangePassword`, params).then(res => res.data) }

export const userAdd = params => { return axios.post(`${base}/login/userAdd`, params).then(res => res.data) }