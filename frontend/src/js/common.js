export const deepClone = obj => {
    return JSON.parse(JSON.stringify(obj))
}
export const isExistInArray = (array, obj) => {
    return array.indexOf(obj)
}