import { SporsmalstegnIkon } from "@sb1/ffe-icons-react";
import { useState } from 'react'


const HelpText = (props) => {
    const [active, setActive] = useState(false)
    return(
        <span className={'help-wrapper'}>
            <span className={'question-button'} onClick={() => setActive(!active)}>
                <SporsmalstegnIkon className={'question-mark'}/>
                <span className={`help-text help-text__${active ? 'active' : 'passive'}`}>
                    {props.text}
                </span>
            </span>
        </span>
    )
}

export default HelpText