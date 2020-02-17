import axios from 'axios'

let base = ''

export const consoleGet = params => { return axios.get(`${base}/console/get`, params).then(res => res.data) }

export const consoleScriptSubSystem = params => { return axios.get(`${base}/script/consoleScriptSubSystem`, params).then(res => res.data) }

export const consoleScriptSubSystemScript = params => { return axios.post(`${base}/script/consoleScriptSubSystemScript`, params).then(res => res.data) }

export const consoleScriptRun = params => { return axios.post(`${base}/script/consoleScriptRun`, params).then(res => res.data) }

export const consoleScriptTerminate = params => { return axios.post(`${base}/script/consoleScriptTerminate`, params).then(res => res.data) }

export const consoleScriptRunOutput = params => { return axios.post(`${base}/script/consoleScriptRunOutput`, params).then(res => res.data) }

export const consoleScriptEdit = params => { return axios.post(`${base}/script/consoleScriptEdit`, params).then(res => res.data) }

export const consoleScriptReplay = params => { return axios.post(`${base}/script/consoleScriptReplay`, params).then(res => res.data) }

export const consoleScriptDelete = params => { return axios.post(`${base}/script/consoleScriptDelete`, params).then(res => res.data) }

export const consoleScriptSaveOutput = params => { return axios.post(`${base}/script/consoleScriptSaveOutput`, params).then(res => res.data) }

export const consoleScriptGetLogs = params => { return axios.post(`${base}/script/consoleScriptGetLogs`, params).then(res => res.data) }

export const consoleScriptGetNewestLog = params => { return axios.post(`${base}/script/consoleScriptGetNewestLog`, params).then(res => res.data) }

export const consoleScriptSchedule = params => { return axios.post(`${base}/script/consoleScriptSchedule`, params).then(res => res.data) }

export const consoleScriptScheduleEdit = params => { return axios.post(`${base}/script/consoleScriptScheduleEdit`, params).then(res => res.data) }

export const consoleScriptScheduleDelete = params => { return axios.post(`${base}/script/consoleScriptScheduleDelete`, params).then(res => res.data) }

export const consoleScriptExtraButtonScriptRun = params => { return axios.post(`${base}/script/consoleScriptExtraButtonScriptRun`, params).then(res => res.data) }

