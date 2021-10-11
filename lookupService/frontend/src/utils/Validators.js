
export const validData = (data, file) => {
    if(data.data === '' && !file) return 'Please add a file to upload'
    else if(data.single_fam_mode && data.family === '') return 'Select a family to use in single family mode'
    else if(!data.single_fam_mode && data.node === '') return 'Select a node to base the search on'
    else if(!validSpecies(data.species)) return 'Your species contains illegal characters'
    else if(!validGenome(data.data)) return 'The genome you entered is invalid'
    return ''
}

const validGenome = (genome) => {
    const lines = genome.split('\n')
    const legalChars = 'agtcun'
    for(let i = 0; i<lines.length; i++){
        let line = lines[i]
        if(line.startsWith('>') || line.startsWith(';')) continue
        let lower = line.toLowerCase()
        for(let i = 0; i < lower.length; i++){
            if(!legalChars.includes(lower[i])) return false
        }
    }
    return true
}

const validSpecies = (species) => {
    if(species.includes('/')) return false
    else if(species.includes('.')) return false
    else if(species.includes('\\')) return false
    return true
}

export const validFile = async (file) => {
    let genome = await new Promise((resolve) => {
        let reader = new FileReader()
        reader.onload = (e) => resolve(reader.result)
        reader.readAsText(file, 'utf-8')
    })
    return validGenome(genome)
}