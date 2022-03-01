import { Link } from "react-router-dom";


const Header = (props) => {
    return(
        <header className="App-header">
            <div className={'header-content'}>
                <Link to={'/'} className={'logo-container'}>
                    <img className={'mirmachine-logo'} src={'/static/assets/mirm_cropped.png'} alt={'mirmachine-logo'}/>
                </Link>
                <Link to={'/retrieve'} className={`button button--header ${props.activeHeader==='/retrieve' ? 'button--header__active' : ''}`}>
                    Ongoing job
                </Link>
                <Link to='/about' className={`button button--header ${props.activeHeader==='/about' ? 'button--header__active' : ''}`}>
                    About
                </Link>
            </div>
        </header>
    )
}

export default Header