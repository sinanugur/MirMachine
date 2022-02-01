import { Link } from 'react-router-dom'

const NotFound = () => {
    return(
        <div className={'limit-width'}>
            <h2>The page you were looking for could not be found</h2>
            <Link className={'button button--action'} to={'/'}>Take me home, country road!</Link>
        </div>
    )
}

export default NotFound