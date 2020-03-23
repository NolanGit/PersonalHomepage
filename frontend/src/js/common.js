export const deepClone = obj => {
    return JSON.parse(JSON.stringify(obj))
}