import axios from 'axios'

let base = ''

export const consoleScriptRun = params => { return axios.post(`${base}/script/run`, params).then(res => res.data) }

export const consoleScriptRunOutput = params => { return axios.post(`${base}/script/runOutput`, params).then(res => res.data) }

export const consoleScriptExtraButtonScriptRun = params => { return axios.post(`${base}/script/extraButtonScriptRun`, params).then(res => res.data) }

