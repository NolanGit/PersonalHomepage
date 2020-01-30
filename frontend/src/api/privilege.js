import axios from 'axios'

let base = ''

export const userGet = params => { return axios.post(`${base}/privilege/userGet`, params).then(res => res.data) }

export const userRoleChange = params => { return axios.post(`${base}/privilege/userRoleChange`, params).then(res => res.data) }


export const roleGet = params => { return axios.get(`${base}/privilege/roleGet`, params).then(res => res.data) }

export const rolePrivilegeGet = params => { return axios.post(`${base}/privilege/rolePrivilegeGet`, params).then(res => res.data) }

export const rolePrivilegeEdit = params => { return axios.post(`${base}/privilege/rolePrivilegeEdit`, params).then(res => res.data) }

export const roleEdit = params => { return axios.post(`${base}/privilege/roleEdit`, params).then(res => res.data) }

export const roleDisable = params => { return axios.post(`${base}/privilege/roleDisable`, params).then(res => res.data) }

export const roleEnable = params => { return axios.post(`${base}/privilege/roleEnable`, params).then(res => res.data) }

export const roleDelete = params => { return axios.post(`${base}/privilege/roleDelete`, params).then(res => res.data) }


export const privilegeGet = params => { return axios.get(`${base}/privilege/privilegeGet`, params).then(res => res.data) }

export const privilegeEdit = params => { return axios.post(`${base}/privilege/privilegeEdit`, params).then(res => res.data) }

export const privilegeDisable = params => { return axios.post(`${base}/privilege/privilegeDisable`, params).then(res => res.data) }

export const privilegeEnable = params => { return axios.post(`${base}/privilege/privilegeEnable`, params).then(res => res.data) }

export const privilegeDelete = params => { return axios.post(`${base}/privilege/privilegeDelete`, params).then(res => res.data) }
