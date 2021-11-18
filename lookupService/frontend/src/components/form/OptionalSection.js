import SearchableDropdown from "./SearchableDropdown";
import HelpText from "./HelpText";
import { Texts } from '../../utils/HelpTexts'

const OptionalSection = (props) => {
    return(
        <div className={`optional-section optional-section__${props.optionalActive ? 'active' : 'passive'}`}>
            <span className={'default-margins pane-heading'}>Optional parameters</span>
                    <span className={'input-row'}>
                        <span className={'input-cell'}>
                            <span className={'input-info'}>
                                <label htmlFor={'model'}>Model type:</label>
                                <HelpText text={Texts[4]}/>
                            </span>
                            <select id={'model'} name={'model'}>
                                <option value={'combined'}>Combined</option>
                                <option value={'proto'}>Proto</option>
                                <option value={'deutero'}>Deutero</option>
                            </select>
                        </span>
                        <span className={'input-cell align-left'}>
                            <span>
                                <input type={'checkbox'} id={'singleFam'} checked={props.singleFam} onChange={
                                    (event) => {
                                        props.setSingleFam(event.target.checked)
                                        props.setSingleNode(false)
                                    }}/>
                                <label htmlFor={'singleFam'}>Single family mode</label>
                            </span>
                            { props.singleFam ?
                                <>
                                    <span className={'input-info'}>
                                        <label htmlFor={'family'} className={'label'}>Family name</label>
                                        <HelpText text={Texts[5]}/>
                                    </span>
                                <SearchableDropdown data={props.families} selected={props.selectedFamily}
                                                    setSelected={props.setSelectedFamily} disabled={false}
                                                    placeholder={'e.g. Mir-71'} identifier={'family'}
                                                    displayParam={'name'} filterParam={'name'}
                                /></> : null
                            }
                            <span>
                                <input type={'checkbox'} id={'singleNode'} checked={props.singleNode}
                                       onChange={(event) => {
                                           props.setSingleFam(false)
                                           props.setSingleNode(event.target.checked)
                                       }}/>
                                <label htmlFor={'singleNode'}>Single node mode</label>
                            </span>
                        </span>
                    </span>
                    {/*<span className={'input-cell'}>
                        <span className={'input-info'}>
                            <label className={'label'} htmlFor={'email'}>Mail address:</label>
                            <HelpText text={Texts[6]}/>
                        </span>
                        <input type={'text'} id={'email'} name={'email'} placeholder={'example@example.com'}/>
                    </span>*/}
        </div>
    )
}
export default OptionalSection