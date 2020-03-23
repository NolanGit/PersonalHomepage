export const deepClone = obj => {
    return JSON.parse(JSON.stringify(obj))
}

function isExistInArray(array, obj) {
    return array.indexOf(obj)
}