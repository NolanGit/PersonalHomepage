import axios from 'axios'

let base = ''

export const userGet = params => { return axios.post(`${base}/privilege/userGet`, params).then(res => res.data) }

export const roleGet = params => { return axios.get(`${base}/privilege/roleGet`, params).then(res => res.data) }

export const privilegeGet = params => { return axios.get(`${base}/privilege/privilegeGet`, params).then(res => res.data) }

export const rolePrivilegeGet = params => { return axios.post(`${base}/privilege/rolePrivilegeGet`, params).then(res => res.data) }

export const userRoleChange = params => { return axios.post(`${base}/privilege/userRoleChange`, params).then(res => res.data) }

export const rolePrivilegeEdit = params => { return axios.post(`${base}/privilege/rolePrivilegeEdit`, params).then(res => res.data) }

export const roleAdd = params => { return axios.post(`${base}/privilege/roleAdd`, params).then(res => res.data) }
