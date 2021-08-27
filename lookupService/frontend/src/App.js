import { useState } from 'react'
import { SearchForm, AboutPage } from './components/MainPageComponents'

const App = () => {
    const [activeHeader, setActiveHeader] = useState('search')

  return (
    <div className="App">
      <header className="App-header">
          <div className={'header-content'}>
              <h1 className={'no-margins'}>MirMachine</h1>
              <span className={`button button--header ${activeHeader==='search' ? 'button--header__active' : ''}`}
              onClick={() => setActiveHeader('search')}>
                  Lookup Service
              </span>
              <span className={`button button--header ${activeHeader==='about' ? 'button--header__active' : ''}`}
                    onClick={() => setActiveHeader('about')}>
                  About
              </span>
          </div>
      </header>
        <main className={'flex-column content'}>
            {activeHeader === 'search' ?
                <SearchForm/> : <AboutPage/>
            }
        </main>
    </div>
  );
}


export default App;
