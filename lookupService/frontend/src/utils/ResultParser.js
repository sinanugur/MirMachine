

const parseGFF = (plainText) => {
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
        tempList.pop() //remove attributes entry
        data.push(tempList.concat(attributes))
    }
    return data
}


export const parseAndCountOccurrencesGFF = (plainText, nItems) => {
    const parsed = parseGFF(plainText)
    const counts = {}
    for(let i = 0; i < parsed.length; i++){
        let curFamily = parsed[i][8]
        if(curFamily === undefined) continue
        curFamily = curFamily.split('.')[0]
        if(curFamily in counts){
            counts[curFamily] = counts[curFamily] + 1
        } else {
            counts[curFamily] = 1
        }
    }
    //sort dictionary
    let pairedItems = Object.keys(counts).map((key) => {
        return [key, counts[key]]
    })
    pairedItems.sort((first, second) => {
        return second[1] - first[1]
    })
    //extract top N entries
    const filtered_counts = []
    let n = Math.min(nItems, pairedItems.length)
    for(let i = 0; i < n; i++){
        filtered_counts.push({key: pairedItems[i][0].toUpperCase(), data: pairedItems[i][1]})
    }
    return filtered_counts
}


export const parseFamiliesInNodes = (nodesAndFamilies, heatmap) => {
    const node_dict = {}
    const found_families = []
    const heatmapLines = heatmap.split('\n')
    for(let i = 1; i<heatmapLines.length; i++){
        let line = heatmapLines[i]
        if(line.trim() === '') continue
        found_families.push(line.split(' ')[2].toLowerCase())
    }
    for(let i = 0; i<nodesAndFamilies.length; i++){
        let cur_obj = nodesAndFamilies[i]
        let node = cur_obj['node']
        let family = cur_obj['family']
        if(found_families.includes(family.toLowerCase())) {
            if (node in node_dict) {
                node_dict[node].push(family.toUpperCase())
            } else {
                node_dict[node] = [family.toUpperCase()]
            }
        }
    }
    return node_dict
}

export const countHitsInNodes = (nodeMap, nItems) => {
    const keys = Object.keys(nodeMap)
    const pairedObjects = []
    for(let i = 0; i<keys.length; i++){
        pairedObjects.push([keys[i], nodeMap[keys[i]].length])
    }
    pairedObjects.sort((first, second) => {
        return second[1] - first[1]
    })
    const filtered = []
    let n = Math.min(nItems, pairedObjects.length)
    for(let i = 0; i<n; i++){
        let cur = pairedObjects[i]
        filtered.push({key: cur[0], data: cur[1]})
    }
    return filtered
}