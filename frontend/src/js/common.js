export const deepClone = obj => {
    return JSON.parse(JSON.stringify(obj))
}
export function isExistInArray(array, obj) {
    return array.indexOf(obj)
}