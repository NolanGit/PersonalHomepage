export const deepClone = obj => {
    return JSON.parse(JSON.stringify(obj))
}

export const formatDate = obj => {
    var seperator1 = "-";
    var year = obj.getFullYear();
    var month = obj.getMonth() + 1;
    var strDate = obj.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    var dateFormatted = year + seperator1 + month + seperator1 + strDate;
    return dateFormatted;
}