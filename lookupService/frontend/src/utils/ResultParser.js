

export const parseGFF = (plainText) => {
    const lines = plainText.split('\n')
    let i = 0
    let line = lines[i]
    while(line.startsWith('#')){
        i += 1
        line = lines[i]
    }
    let data = []
    for(let j = i; j<lines.length; j++){
        let tempList = lines[j].split('\t')
        let attributes = tempList[tempList.length-1].split(';')
        for(let k = 0; k < attributes.length; k++){
            attributes[k] = attributes[k].split('=')[1]
        }
        attributes.pop() //remove sequence
        tempList.pop() //remove attributes entry
        data.push(tempList.concat(attributes))
    }
    return data
}