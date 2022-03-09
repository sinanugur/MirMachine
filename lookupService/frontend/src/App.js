import { useEffect, useState } from 'react'
import { AboutPage } from './components/about/About'
import { SearchForm } from './components/form/Form'
import NotFound from './components/NotFound'
import Job from './components/job/JobPage'
import Header from './components/frame/Header'
import Footer from './components/frame/Footer'
import CookieBanner from './components/frame/CookieBanner'
import Retrieval from './components/retrieval/Retrieval'
import Result from './components/result/Result'
import { Switch, Route, useLocation } from 'react-router-dom'
import { checkIfNewUser } from './utils/Repository'


const App = () => {
    const [activeHeader, setActiveHeader] = useState('/')
    const [cookiePrompt, setCookiePrompt] = useState(false)
    let location = useLocation()

    useEffect(() => {
        setActiveHeader(location.pathname)
    }, [location])

    useEffect(() => {
        const cookieCheck = async () => {
            let response = await checkIfNewUser()
            if (response.message === 'new_user') {
                setCookiePrompt(true)
            }
        }
        cookieCheck()
    }, [])

  return (
    <div className="App">
        <CookieBanner active={cookiePrompt} setActive={setCookiePrompt}/>
        <Header activeHeader={activeHeader}/>
        <main className={'flex-column content'}>
            <Switch>
                <Route exact path={'/'} component={SearchForm}/>
                <Route path={'/about'} component={AboutPage}/>
                <Route path={'/job/:jobID'} component={Job}/>
                <Route path={'/retrieve'} component={Retrieval}/>
                <Route path={'/result/:jobID'} component={Result}/>
                <Route component={NotFound}/>
            </Switch>
        </main>
        <Footer/>
    </div>
  );
}


export default App;
