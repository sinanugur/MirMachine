import { useEffect, useState } from 'react'
import { SearchForm, AboutPage } from './components/MainPageComponents'
import { Switch, Route, useLocation, Link } from 'react-router-dom'
import Header from './components/Header'


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
            </Switch>
        </main>
    </div>
  );
}


export default App;
