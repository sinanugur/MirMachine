import { Link } from 'react-router-dom'

const NotFound = () => {
    return(
        <div className={'limit-width flex-column'}>
            <h2>The page you were looking for could not be found</h2>
            <Link className={'button button--action'} to={'/'}>Take me home</Link>
        </div>
    )
}

export default NotFound