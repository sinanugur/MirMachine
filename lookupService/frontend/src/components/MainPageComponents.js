import { useState } from "react";
import { ChevronIkon, ForstorrelsesglassIkon } from "@sb1/ffe-icons-react";
import { submitJob } from '../utils/Repository'
import { Redirect } from 'react-router-dom'

export const SearchForm = () => {
    const [optionalActive, setOptionalActive] = useState(false)
    const [inputMode, setInputMode] = useState("text")
    const [redirect, setRedirect] = useState()

    const handleSubmit = async () => {
        const data = {
            data: document.getElementById('sequence').value,
            mode: document.getElementById('mode').value,
            node: document.getElementById('node').value,
            species: document.getElementById('species').value,
            model_type: document.getElementById('model').value,
            dry_run: document.getElementById('dryRun').checked,
            single_fam_mode: document.getElementById('singleFam').checked,
            mail_address: document.getElementById('email').value
        }
        console.log(data)
        const response = await submitJob(data)
        console.log(response)
        setRedirect(response.id)
    }
    return(
        <form className={'flex-column limit-width'}
                name={'query'} id={'query'} onSubmit={event => event.preventDefault()}>
                <span className={'input-cell'}>
                    <label htmlFor={'sequence'}>Sequence:</label>
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
                    <label htmlFor={'mode'}>Mode:</label>
                    <select id={'mode'} name={'mode'} onChange={event => {setInputMode(event.target.value)}}>
                        <option value={'text'}>Text input</option>
                        <option value={'file'}>File upload</option>
                        <option value={'link'}>Genome link</option>
                        <option value={'accNum'}>GenBank accession number</option>
                    </select>
                </span>
            <div className={'input-row'}>
                    <span className={'input-cell'}>
                        <label htmlFor={'species'}>Species:</label>
                        <input type={'text'} name={'species'} id={'species'} placeholder={'e.g. Caenorhabditis'}/>
                    </span>
                <span className={'input-cell'}>
                        <label htmlFor={'node'}>Node:</label>
                        <input type={'text'} name={'node'} id={'node'} placeholder={'e.g. Caenorhabditis_elegans'}/>
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
                                <option value={'proto'}>Proto</option>
                                <option value={'deutero'}>Deutero</option>
                                <option value={'both'}>Both</option>
                            </select>
                        </span>
                        <span className={'input-cell align-left'}>
                            <span>
                                <input type={'checkbox'} id={'singleFam'} value={'true'}/>
                                <label htmlFor={'singleFam'}>Single family mode</label>
                            </span>
                            <span>
                                <input type={'checkbox'} id={'dryRun'} value={'true'}/>
                                <label htmlFor={'dryRun'}>Dry run</label>
                            </span>
                        </span>
                    </span>
                <span className={'input-cell'}>
                        <label htmlFor={'email'}>Mail address:</label>
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