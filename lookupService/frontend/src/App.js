import { useEffect, useState } from 'react'
import { SearchForm, AboutPage } from './components/MainPageComponents'
import Job from './components/JobPage'
import Header from './components/Header'
import Retrieval from "./components/Retrieval";
import { Switch, Route, useLocation } from 'react-router-dom'


const App = () => {
    const [activeHeader, setActiveHeader] = useState('/')
    let location = useLocation()

    useEffect(() => {
        setActiveHeader(location.pathname)
    }, [location])

  return (
    <div className="App">
      <Header activeHeader={activeHeader}/>
        <main className={'flex-column content'}>
            <Switch>
                <Route exact path={'/'} component={SearchForm}/>
                <Route path={'/about'} component={AboutPage}/>
                <Route path={'/job/:jobID'} component={Job}/>
                <Route path={'/retrieve'} component={Retrieval}/>
            </Switch>
        </main>
    </div>
  );
}


export default App;
