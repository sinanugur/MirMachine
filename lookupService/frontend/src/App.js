import { useState, useEffect } from 'react'


const App = () => {
    const [optionalActive, setOptionalActive] = useState(true)
    useEffect(() => {
        console.log(optionalActive)
    },[optionalActive])
  return (
    <div className="App">
      <header className="App-header">
        <p>Hello you</p>
      </header>
        <main className={'flex-column content'}>
            <h1>MirMachine</h1>
            <form className={'flex-column input-section'}>
                <span className={'input-cell'}>
                    <label htmlFor={'sequence'}>Sequence:</label>
                    <input
                        type={'text'}
                        placeholder={'Input sequence here'}
                        name={'sequence'}
                        id={'sequence'}
                    />
                </span>
                <span className={'input-cell'}>
                    <label htmlFor={'mode'}>Mode:</label>
                    <select id={'mode'} name={'mode'}>
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
                <button onClick={() => {setOptionalActive(!optionalActive)}}>Optional params</button>
                <div className={`optional-section optional-section__${optionalActive ? 'active' : 'passive'}`}>
                    <span className={'input-cell'}>
                        <label htmlFor={'model'}>Model type:</label>
                        <select id={'model'} name={'model'}>
                            <option value={'proto'}>Proto</option>
                            <option value={'deutero'}>Deutero</option>
                            <option value={'both'}>Both</option>
                        </select>
                    </span>
                    <span className={'input-cell'}>
                        <input type={'checkbox'} id={'singleFam'}/>
                        <input type={'checkbox'} id={'dryRun'}/>
                    </span>
                </div>
            </form>
        </main>
    </div>
  );
}


export default App;
