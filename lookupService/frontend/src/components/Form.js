import { useState, useEffect } from "react";
import { ChevronIkon, ForstorrelsesglassIkon } from "@sb1/ffe-icons-react";
import { fetchTree, submitJob, getFamilies, getFamiliesIncludedInSearch } from '../utils/Repository'
import { Redirect } from 'react-router-dom'
import Tree from './Tree'
import SearchableDropdown from "./SearchableDropdown";

export const SearchForm = () => {
    // Form states
    const [optionalActive, setOptionalActive] = useState(false)
    const [modal, setModal] = useState(false)
    const [showIncluded, setShowIncluded] = useState(false)

    // Form data
    const [inputMode, setInputMode] = useState("text")
    const [node, setNode] = useState("")
    const [singleNode, setSingleNode] = useState(false)
    const [selectedFamily, setSelectedFamily] = useState("")
    const [singleFam, setSingleFam] = useState(false)

    const [redirect, setRedirect] = useState()

    // Tree data
    const [nodes, setNodes] = useState()
    const [edges, setEdges] = useState()

    // Family data
    const [families, setFamilies] = useState()
    const [includedFamilies, setIncludedFamilies] = useState()

    useEffect(() => {
        // disable modal after selection
        setModal(false)
    },[node])


    useEffect(() => {
        // fetch data upon page load
        const getData = async () => {
            let treeData = await fetchTree()
            let familyData = await getFamilies()
            setNodes(treeData.nodes)
            setEdges(treeData.edges)
            setFamilies(familyData)
        }
        getData()
    },[])

    const handleSubmit = async () => {
        const data = {
            data: document.getElementById('sequence').value,
            mode: document.getElementById('mode').value,
            node: node,
            species: document.getElementById('species').value,
            model_type: document.getElementById('model').value,
            single_node: singleNode,
            single_fam_mode: singleFam,
            family: singleFam ? selectedFamily : '',
            mail_address: document.getElementById('email').value
        }
        const response = await submitJob(data)
        setRedirect(response.id)
    }

    const handleIncludedFamilyFetching = async () => {
        if(singleFam){
            setIncludedFamilies({families: [selectedFamily]})
            return
        }
        if(!showIncluded && node){
            setIncludedFamilies(await getFamiliesIncludedInSearch(node, false, singleNode))
        }
        setShowIncluded(!showIncluded)
    }

    return(
        <form className={'flex-column limit-width'}
              name={'query'} id={'query'} onSubmit={event => event.preventDefault()}>
            {modal && <Tree hook={setNode} show={setModal} nodes={nodes} edges={edges}/>}
            <span className={'input-cell'}>
                    <label className={'label'} htmlFor={'sequence'}>Sequence:</label>
                { inputMode === 'text' ?
                    <textarea id={'sequence'} name={'sequence'} rows={2}
                              placeholder={'Input sequence here'}/> :
                    <input
                        type={inputMode === 'file' ? 'file' : 'text'}
                        placeholder={`Input ${inputMode === 'link' ? 'link' : 'accession number'} here`}
                        name={'sequence'}
                        id={'sequence'}
                    />
                }
                </span>
            <span className={'input-cell'}>
                    <label className={'label'} htmlFor={'mode'}>Mode:</label>
                    <select id={'mode'} name={'mode'} onChange={event => {setInputMode(event.target.value)}}>
                        <option value={'text'}>Text input</option>
                        <option value={'file'}>File upload</option>
                        <option value={'link'}>Genome link</option>
                        <option value={'accNum'}>GenBank accession number</option>
                    </select>
                </span>
            <div className={'input-row'}>
                    <span className={'input-cell'}>
                        <label className={'label'} htmlFor={'species'}>Species:</label>
                        <input type={'text'} name={'species'} id={'species'} placeholder={'e.g. Caenorhabditis'}/>
                    </span>
                <span className={'input-cell'}>
                    <label className={'label'} htmlFor={'node'}>Node:</label>
                        <span className={'same-line'}>
                            <SearchableDropdown
                                data={nodes} selected={node}
                                setSelected={setNode} disabled={singleFam}
                                placeholder={'e.g. C elegans'} identifier={'node'}
                                displayParam={'text'} filterParam={'id'}
                            />
                            <span className={`button button--default default-margins ${singleFam ? 'disabled' : ''}`}
                                  onClick={() => {if(!singleFam) setModal(true)}}>Visualize</span>
                        </span>
                    </span>
            </div>
            <span className={'button button--default'}
                  onClick={() => {setOptionalActive(!optionalActive)}}>
                    Optional params <ChevronIkon className={`icon icon--chevron ${optionalActive ? '' : 'icon--chevron__right'}`}/>
                </span>
            <div className={`optional-section optional-section__${optionalActive ? 'active' : 'passive'}`}>
                    <span className={'input-row'}>
                        <span className={'input-cell'}>
                            <label htmlFor={'model'}>Model type:</label>
                            <select id={'model'} name={'model'}>
                                <option value={'both'}>Both</option>
                                <option value={'proto'}>Proto</option>
                                <option value={'deutero'}>Deutero</option>
                            </select>
                        </span>
                        <span className={'input-cell align-left'}>
                            <span>
                                <input type={'checkbox'} id={'singleFam'} checked={singleFam} onChange={
                                    (event) => {
                                        setSingleFam(event.target.checked)
                                        setSingleNode(false)
                                    }}/>
                                <label htmlFor={'singleFam'}>Single family mode</label>
                            </span>
                            { singleFam ?
                                <SearchableDropdown data={families} selected={selectedFamily}
                                                    setSelected={setSelectedFamily} disabled={false}
                                                    placeholder={'e.g. Mir-71'} identifier={'family'}
                                                    displayParam={'name'} filterParam={'name'}
                                /> : null
                            }
                            <span>
                                <input type={'checkbox'} id={'singleNode'} checked={singleNode}
                                       onChange={(event) => {
                                           setSingleFam(false)
                                           setSingleNode(event.target.checked)
                                       }}/>
                                <label htmlFor={'singleNode'}>Single node mode</label>
                            </span>
                        </span>
                    </span>
                <span className={'input-cell'}>
                        <label className={'label'} htmlFor={'email'}>Mail address:</label>
                        <input type={'text'} id={'email'} name={'email'} placeholder={'example@example.com'}/>
                    </span>
            </div>
            <span className={'button button--action'} id={'submit'} onClick={() => {
                handleSubmit()
            }}>
                    Run MirMachine <ForstorrelsesglassIkon className={'icon icon--run'}/>
            </span>
            <span className={'button button--default'} onClick={async () => {
                handleIncludedFamilyFetching()
                }}>
                Included families
            </span>
            <div className={`optional-section optional-section__${showIncluded ? 'active' : 'passive'}`}>
                <span className={'default-margins pane-heading'}>
                    {node && 'Families that will be included in the search'}
                    {!node && 'Select a node and hit the refresh button'}
                </span>
                <span className={'button button--default'} onClick={async () => {
                    handleIncludedFamilyFetching()
                }}>
                    Refresh
                </span>
                <div className={'scrolling-list-wrapped'}>
                    {includedFamilies &&
                    includedFamilies.families.map((it) => {
                        return <span className={'default-margins'}>{it}</span>
                    })}
                </div>
            </div>
            {redirect && <Redirect to={`/job/${redirect}`}/>}
        </form>
    )
}