import axios from 'axios'

let base = ''

export const bookmarksData = params => { return axios.post(`${base}/bookmarks/bookmarksData`, params).then(res => res.data) }