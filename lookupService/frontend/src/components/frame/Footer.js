import React from 'react'
import { Github } from 'react-bootstrap-icons'

const Footer = () => {
    return(
        <footer className={'app-footer'}>
            <a href={'https://github.com/selfjell/MirMachine/'} target={'_blank'} className={'default-margins'}>
                <Github className={'footer-icon'} size={25}/>
            </a>
            <a href={'https://mirgenedb.org/'} target={'_blank'}>
                <span className={'mirgenedb default-margins'}>
                    <span className={'mirgenedb__red'}>Mir</span>
                    <span className={'mirgenedb__black'}>Gene</span>
                    <span className={'mirgenedb__blue'}>DB</span>
                </span>
            </a>
            <a className={'default-margins uio-container'} href={'https://www.uio.no/english/'} target={'_blank'}>
                <img src={'/static/assets/UiO-logo.svg'} alt={'UiO Logo'} className={'uio'}/>
            </a>
        </footer>
    )
}

export default Footer