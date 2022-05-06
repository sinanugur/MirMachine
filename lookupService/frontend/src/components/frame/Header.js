import { Link } from "react-router-dom";
import {handleButtonKeyPress} from "../../utils/Buttons";


const Header = (props) => {
    return(
        <header className="App-header">
            <div className={'header-content'}>
                <span
                    tabindex={'0'}
                    role={'button'}
                    onKeyDown = {(event) => handleButtonKeyPress(event, true)}
                >
                    <Link to={'/'} className={'logo-container'}>
                        <img className={'mirmachine-logo'} src={'/static/assets/mirm_cropped.png'} alt={'The MirMachine Logo'}/>
                    </Link>
                </span>
                <span
                    tabindex={'0'}
                    role={'button'}
                    onKeyDown = {(event) => handleButtonKeyPress(event, true)}
                >
                    <Link to={'/retrieve'} className={`button button--header ${props.activeHeader==='/retrieve' ? 'button--header__active' : ''}`}>
                        Ongoing job
                    </Link>
                </span>
                <span
                    tabindex={'0'}
                    role={'button'}
                    onKeyDown = {(event) => handleButtonKeyPress(event, true)}
                >
                    <Link to='/about'

                          className={`button button--header ${props.activeHeader==='/about' ? 'button--header__active' : ''}`}>
                        About
                    </Link>
                </span>
            </div>
        </header>
    )
}

export default Header