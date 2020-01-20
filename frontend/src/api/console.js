import axios from 'axios'

let base = ''

export const consoleGet = params => { return axios.get(`${base}/console/get`, params).then(res => res.data) }

export const consoleScriptSubSystem = params => { return axios.get(`${base}/console/consoleScriptSubSystem`, params).then(res => res.data) }

export const consoleScriptSubSystemScript = params => { return axios.post(`${base}/console/consoleScriptSubSystemScript`, params).then(res => res.data) }

export const consoleScriptRun = params => { return axios.post(`${base}/console/consoleScriptRun`, params).then(res => res.data) }

export const consoleScriptTerminate = params => { return axios.post(`${base}/console/consoleScriptTerminate`, params).then(res => res.data) }

export const consoleScriptRunOutput = params => { return axios.post(`${base}/console/consoleScriptRunOutput`, params).then(res => res.data) }

export const consoleScriptEdit = params => { return axios.post(`${base}/console/consoleScriptEdit`, params).then(res => res.data) }

export const consoleScriptReplay = params => { return axios.post(`${base}/console/consoleScriptReplay`, params).then(res => res.data) }

export const consoleScriptDelete = params => { return axios.post(`${base}/console/consoleScriptDelete`, params).then(res => res.data) }

export const consoleScriptSaveOutput = params => { return axios.post(`${base}/console/consoleScriptSaveOutput`, params).then(res => res.data) }

export const consoleScriptGetLogs = params => { return axios.post(`${base}/console/consoleScriptGetLogs`, params).then(res => res.data) }

export const consoleScriptGetNewestLog = params => { return axios.post(`${base}/console/consoleScriptGetNewestLog`, params).then(res => res.data) }

export const consoleScriptSchedule = params => { return axios.post(`${base}/console/consoleScriptSchedule`, params).then(res => res.data) }

export const consoleScriptScheduleEdit = params => { return axios.post(`${base}/console/consoleScriptScheduleEdit`, params).then(res => res.data) }

export const consoleScriptScheduleDelete = params => { return axios.post(`${base}/console/consoleScriptScheduleDelete`, params).then(res => res.data) }

export const consoleScriptExtraButtonScriptRun = params => { return axios.post(`${base}/console/consoleScriptExtraButtonScriptRun`, params).then(res => res.data) }

export const userGet = params => { return axios.post(`${base}/privilege/userGet`, params).then(res => res.data) }

export const roleGet = params => { return axios.get(`${base}/privilege/roleGet`, params).then(res => res.data) }

export const privilegeGet = params => { return axios.get(`${base}/privilege/privilegeGet`, params).then(res => res.data) }

export const rolePrivilegeGet = params => { return axios.post(`${base}/privilege/rolePrivilegeGet`, params).then(res => res.data) }