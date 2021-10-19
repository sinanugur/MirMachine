import { useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getResults } from '../../utils/Repository'
import { ResultFetchError } from '../../utils/Errors'

const Result = () => {
    const { jobID } = useParams()
    const [results, setResults] = useState()

    useEffect(() => {
        const getResult = async () => {
            try{
                const data = await getResults(jobID)
                setResults(data)
            } catch(err) {
                alert(err.message)
            }
        }
        getResult()
    }, [])
    return(
        <div>
            {results &&
                <>
                    <span>{results.fasta}</span>
                    <span>{results.filtered_gff}</span>
                    <span>{results.heatmap}</span>
                </>
            }
        </div>
    )
}

export default Result