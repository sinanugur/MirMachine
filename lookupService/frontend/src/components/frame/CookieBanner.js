

const CookieBanner = (props) => {
    return(
        <div className={`cookie-banner ${props.active ? 'cookie-banner--active' : ''}`}>
            We only use functional cookies that are strictly necessary. We don't care who you are or what you do on the internet.
            We only care that our site works. Happy annotating!
            <span className={'cookie-cross'} onClick={() => props.setActive(false)}>&times;</span>
        </div>
    )
}

export default CookieBanner