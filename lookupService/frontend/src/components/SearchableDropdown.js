import { useRef, useState, useEffect } from "react";


const SearchableDropdown = (props) => {
    const [dropdown, setDropdown] = useState(false)
    const focusRef = useRef('list0')
    const filteredData = useRef()

    useEffect(() => {
        // reset focus in dropdown list after selection or list despawn
        focusRef.current = 'list0'
    },[dropdown, props.selected])

    const handleKeyPress = (event) => {
        let key = event.key
        let curIndex = parseInt(focusRef.current.substring(4))

        if(props.data && filteredData.current) {
            switch (key) {
                case "ArrowDown":
                    event.preventDefault()
                    focusRef.current = `list${String((curIndex + 1) % filteredData.current.length)}`
                    document.getElementById(focusRef.current).focus()
                    break
                case "ArrowUp":
                    event.preventDefault()
                    focusRef.current = `list${Math.max((curIndex - 1), 0)}`
                    document.getElementById(focusRef.current).focus()
                    break
                case "Enter":
                    document.getElementById(focusRef.current).click()
                    break
            }
        }
    }

    const updateFilteredInput = (value) => {
        if(props.data) {
            filteredData.current =
                props.data.filter(it => (it.text.toLowerCase().startsWith(value.toLowerCase()) && it.text !== ''))
        }
    }
    return(
        <span className={'dropdown'} onBlur={(event) => {
            if(event.relatedTarget && event.relatedTarget.id.startsWith('list')){
                return
            }
            setDropdown(false)
        }}>
            <input
                placeholder={props.placeholder} autoComplete={'off'}
                className={'dropdown--button'} type={'text'} name={'node'} id={'node'}
                onFocus={() => {
                    if(props.data && !filteredData.current)
                        updateFilteredInput('')
                    setDropdown(true)
                }}
                value={props.selected} onChange={(event) => {
                props.setSelected(event.target.value)
                updateFilteredInput(event.target.value)
            }}
                disabled={props.disabled}
                onKeyDown={(event) => {handleKeyPress(event)}}/>
            <span tabIndex={'0'} id='dropdown'
                  className={`dropdown--list dropdown--list__${dropdown ? 'active' : 'passive'}`}>
                {props.data && filteredData.current &&
                filteredData.current.map((elem, i) => {
                    return <span key={i} id={`list${i}`} className={'dropdown--element'} tabIndex={'0'}
                                 onClick={() => {
                                     props.setSelected(elem.id)
                                     setDropdown(false)
                                 }}
                                 onKeyDown={(event) => {handleKeyPress(event)}}>
                                <span className={'dropdown--text'}>{elem.text}</span>
                            </span>
                })}
            </span>
        </span>
    )
}







export default SearchableDropdown