import { useState, useEffect, useRef } from "react";
import { ChevronIkon, ForstorrelsesglassIkon } from "@sb1/ffe-icons-react";
import {fetchTree, submitJob} from '../utils/Repository'
import { Redirect } from 'react-router-dom'
import Tree from './Tree'

export const SearchForm = () => {
    // Form states
    const [optionalActive, setOptionalActive] = useState(false)
    const [modal, setModal] = useState(false)
    const [nodeDropdown, setNodeDropdown] = useState(false)
    const focusRef = useRef('nodeList0')
    const filteredNodes = useRef()

    // Form data
    const [inputMode, setInputMode] = useState("text")
    const [node, setNode] = useState("")
    const [singleFam, setSingleFam] = useState(false)
    const [singleNode, setSingleNode] = useState(false)

    const [redirect, setRedirect] = useState()

    // Tree data
    const [nodes, setNodes] = useState()
    const [edges, setEdges] = useState()

    useEffect(() => {
        // disable modal after selection
        setModal(false)
    },[node])

    useEffect(() => {
        // reset focus in dropdown list after selection or list despawn
        focusRef.current = 'nodeList0'
    },[nodeDropdown, node])

    useEffect(() => {
        // fetch data upon page load
        const getNewickTree = async () => {
            let data = await fetchTree()
            setNodes(data.nodes)
            setEdges(data.edges)
        }
        getNewickTree()
    },[])

    const handleSubmit = async () => {
        const data = {
            data: document.getElementById('sequence').value,
            mode: document.getElementById('mode').value,
            node: document.getElementById('node').value,
            species: document.getElementById('species').value,
            model_type: document.getElementById('model').value,
            single_node: singleNode,
            single_fam_mode: singleFam,
            family: singleFam ? document.getElementById('family').value : '',
            mail_address: document.getElementById('email').value
        }
        const response = await submitJob(data)
        setRedirect(response.id)
    }

    const updateFilteredNodes = (value) => {
        if(nodes) {
            filteredNodes.current =
                nodes.filter(it => (it.text.toLowerCase().startsWith(value.toLowerCase()) && it.text !== ''))
        }
    }

    const handleKeyPress = (event) => {
        let key = event.key
        let curIndex = parseInt(focusRef.current.substring(8))

        if(nodes && filteredNodes.current) {
            switch (key) {
                case "ArrowDown":
                    event.preventDefault()
                    focusRef.current = `nodeList${String((curIndex + 1) % filteredNodes.current.length)}`
                    document.getElementById(focusRef.current).focus()
                    break
                case "ArrowUp":
                    event.preventDefault()
                    focusRef.current = `nodeList${Math.max((curIndex - 1), 0)}`
                    document.getElementById(focusRef.current).focus()
                    break
                case "Enter":
                    document.getElementById(focusRef.current).click()
                    break
            }
        }
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
                            <span className={'dropdown'} onBlur={(event) => {
                                if(event.relatedTarget && event.relatedTarget.id.startsWith('nodeList')){
                                    return
                                }
                                setNodeDropdown(false)
                            }}>
                                <input
                                    placeholder={'e.g. C elegans'} autoComplete={'off'}
                                    className={'dropdown--button'} type={'text'} name={'node'} id={'node'}
                                    onFocus={() => {
                                        if(nodes && !filteredNodes.current)
                                            updateFilteredNodes('')
                                        setNodeDropdown(true)
                                    }}
                                    value={node} onChange={(event) => {
                                        setNode(event.target.value)
                                        updateFilteredNodes(event.target.value)
                                    }}
                                    disabled={singleFam}
                                    onKeyDown={(event) => {handleKeyPress(event)}}
                                />
                                <span tabIndex={'0'} id='nodeDropdown'
                                      className={`dropdown--list dropdown--list__${nodeDropdown ? 'active' : 'passive'}`}>
                                    {nodes && filteredNodes.current &&
                                        filteredNodes.current.map((elem, i) => {
                                            return <span key={i} id={`nodeList${i}`} className={'dropdown--element'} tabIndex={'0'}
                                                     onClick={() => {
                                                         setNode(elem.id)
                                                         setNodeDropdown(false)
                                                     }}
                                                     onKeyDown={(event) => {handleKeyPress(event)}}>
                                                <span className={'dropdown--text'}>{elem.text}</span>
                                                </span>
                                    })}
                                </span>
                            </span>
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
                                <span>
                                    <input className={'limit-input-width'} type={'text'} id={'family'} placeholder={'e.g. Mir-71'}/>
                                </span> : null
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
            {redirect && <Redirect to={`/job/${redirect}`}/>}
        </form>
    )
}

export const AboutPage = () => {
    return(
        <div className={'limit-width'}>
            <h2>About MirMachine</h2>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit,
                sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat.
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum
                dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
                sunt in culpa qui officia deserunt mollit anim id est laborum.
            </p>
        </div>
    )
}

