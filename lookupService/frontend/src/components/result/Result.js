import { useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getResults } from '../../utils/Repository'
import { parseGFF } from '../../utils/ResultParser'

const Result = () => {
    const { jobID } = useParams()
    const [results, setResults] = useState()
    const [gffData, setGffData] = useState()
    const [modal, setModal] = useState(false)
    const [modalSequence, setModalSequence] = useState()
    const [selectedSequence, setSelectedSequence] = useState()

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
        {modal &&
            <div className={'modal'}>
                <div className={'flex-column'}>
                    <div className={'sequence-modal'}>
                        <span className={'close'} onClick={() => {setModal(false)}}>&times;</span>
                        <span className={'flex-column'}>
                            <p className={'no-margins'}><b>30NT sequence for {selectedSequence}:</b></p>
                            {modalSequence}
                        </span>
                    </div>
                </div>
            </div>
        }
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
                            if(it.length !== 0 && it[0])
                            return(
                            <tr key={i}>
                                {it.map((e, j) => {
                                    if(j !== it.length-1 && e !== '')
                                        return(<td key={j}>{e}</td>)
                                })}
                                <td>
                                    <span className={'button button--default cell-button'}
                                        onClick={() => {
                                            setSelectedSequence(it[8])
                                            setModalSequence(it[it.length-1])
                                            setModal(!modal)
                                        }}>
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
                        {results && results.fasta.split('>').map((it, i) => {
                            const separated = it.split('\n')
                            if(separated.length !== 0 && separated[0] !== '')
                            return(
                                <tr key={i}>
                                    <td>{separated[0]}</td>
                                    <td>{separated[1]}</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
                <a className={'button button--action'}
                   href={`http://localhost:8000/api/download/${jobID}`} download={'results.zip'}>
                    Download raw result
                </a>
                <span>{/*results.fasta*/}</span>
                <span>{/*results.filtered_gff*/}</span>
                <span>{/*results.heatmap*/}</span>
            </>
        }
        </div>
    )
}

export default Result