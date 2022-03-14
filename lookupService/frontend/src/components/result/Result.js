import { useParams, Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getResults } from '../../utils/Repository'
import { parseAndCountOccurrencesGFF, parseFamiliesInNodes, countHitsInFamilies } from '../../utils/ResultParser'
import { baseURL } from '../../config'
import { BarChart, BarSeries, Bar } from 'reaviz'
import {white} from "@sb1/ffe-core";

const Result = () => {
    const { jobID } = useParams()
    const [results, setResults] = useState()
    const [gffData, setGffData] = useState()
    const [nodeMap, setNodeMap] = useState()
    const [nodeCount, setNodeCount] = useState()

    useEffect(() => {
        const getResult = async () => {
            try{
                const data = await getResults(jobID)
                setResults(data)
                setGffData(parseAndCountOccurrencesGFF(data.filtered_gff, 10))
                setNodeMap(parseFamiliesInNodes(data.families, data.heatmap))
            } catch(err) {
                alert(err.message)
            }
        }
        getResult()
    }, [])
    useEffect(() => {
        if(nodeMap) setNodeCount(countHitsInFamilies(nodeMap, 10))
    }, [nodeMap])
    return(
        <div className={'flex-column'}>
            <span className={'result-button-container'}>
                <Link className={'button button--back'} to={'/job/' + jobID}>Back to job page</Link>
                <a className={'button button--back'}
                   href={'http://' + baseURL + `/api/download/${jobID}?type=zip`} download={'results.zip'}>
                        Download all results
                </a>
                <a className={'button button--back'}
                   href={'http://' + baseURL + `/api/download/${jobID}?type=gff`} download={'results.zip'}>
                        Download GFF file
                </a>
                <a className={'button button--back'}
                   href={'http://' + baseURL + `/api/download/${jobID}?type=filtered_gff`} download={'results.zip'}>
                        Download filtered GFF
                </a>
                <a className={'button button--back'}
                   href={'http://' + baseURL + `/api/download/${jobID}?type=fasta`} download={'results.zip'}>
                        Download FASTA file
                </a>
                <a className={'button button--back'}
                   href={'http://' + baseURL + `/api/download/${jobID}?type=heatmap`} download={'results.zip'}>
                        Download heatmap
                </a>
            </span>
            <div className={'result-container'}>
                <div className={'graph-row'}>
                {gffData &&
                    <span>
                    <h3>Families occurring the most</h3>
                    <BarChart
                        series={
                            <BarSeries
                                colorScheme={(_data, index) => (index % 2 ? '#047576' : '#049F9E')}
                            />
                            }
                        margins={45}
                        height={450}
                        width={450}
                        data={gffData}/>
                    </span>
                }
                {nodeCount &&
                    <span>
                        <h3>Nodes with the most hits</h3>
                        <BarChart
                            series={
                                <BarSeries
                                    colorScheme={(_data, index) => (index % 2 ? '#047576' : '#049F9E')}
                                />
                            }
                            margins={45}
                            height={450}
                            width={450}
                            data={nodeCount}/>
                    </span>
                    }
                    </div>
                <table>
                    <thead>
                        <tr>
                            <th>Phylogenetic Node</th>
                            <th>Families Found</th>
                        </tr>
                    </thead>
                    <tbody>
                    {nodeMap && Object.keys(nodeMap).map((k) => {
                        return(
                        <tr key={k}>
                            <td>{k} ({nodeMap[k].length})</td>
                            <td>{nodeMap[k].map((fam) => {
                                return(fam + ' ')
                            })}</td>
                        </tr>
                        )
                    })}
                    </tbody>
                </table>
            </div>
        </div>
    )
}

export default Result