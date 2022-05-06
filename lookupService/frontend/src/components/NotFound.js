import { Link } from 'react-router-dom'
import {handleButtonKeyPress} from "../utils/Buttons";

const NotFound = () => {
    return(
        <div className={'limit-width flex-column'}>
            <h2>The page you were looking for could not be found</h2>
            <span
                tabindex={'0'}
                role={'button'}
                onKeyDown = {(event) => handleButtonKeyPress(event, true)}
            >
                <Link className={'button button--action'} to={'/'}>Take me home</Link>
            </span>
        </div>
    )
}

export default NotFound