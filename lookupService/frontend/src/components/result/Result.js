import { useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getResults } from '../../utils/Repository'
import { parseGFF } from '../../utils/ResultParser'

const Result = () => {
    const { jobID } = useParams()
    const [results, setResults] = useState()
    const [gffData, setGffData] = useState()

    useEffect(() => {
        const getResult = async () => {
            try{
                const data = await getResults(jobID)
                setResults(data)
                setGffData(parseGFF(data.filtered_gff))
            } catch(err) {
                alert(err.message)
            }
        }
        getResult()
    }, [])
    return(
        <div className={'result-container'}>
        {results &&
            <>
                <span className={'black-text'}>GFF results</span>
                <table>
                    <thead>
                        <tr>
                            <th>Sequence</th>
                            <th>Source</th>
                            <th>Feature</th>
                            <th>Start</th>
                            <th>End</th>
                            <th>Score</th>
                            <th>Strand</th>
                            <th>Phase</th>
                            <th>Gene-id</th>
                            <th>E-value</th>
                            <th>30NT Sequence</th>
                        </tr>
                    </thead>
                    <tbody>
                        {gffData && gffData.map((it, i) => {
                            if(it.length !== 0)
                            return(
                            <tr key={i}>
                                {it.map((e, j) => {
                                    return(<td key={j}>{e}</td>)
                                })}
                                <td className={''}>
                                    <span className={'button button--default cell-button'}>
                                        View
                                    </span>
                                </td>
                            </tr>)
                        })}
                    </tbody>
                </table>
                <span className={'black-text'}>Hit areas:</span>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Sequence</th>
                        </tr>
                    </thead>
                    <tbody>
                        {results && results.fasta.split('>').map((it) => {
                            const separated = it.split('\n')
                            if(separated.length !== 0 && separated[0] !== '')
                            return(
                                <tr>
                                    <td>{separated[0]}</td>
                                    <td>{separated[1]}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
                <span className={'button button--action'}>
                    Download raw result
                </span>
                <span>{/*results.fasta*/}</span>
                <span>{/*results.filtered_gff*/}</span>
                <span>{/*results.heatmap*/}</span>
            </>
        }
        </div>
    )
}

export default Result