import { Redirect } from 'react-router-dom'
import { useState } from 'react'

const Retrieval = () => {
    const [redir, setRedir] = useState(false)

    const handleSubmit = async (event) => {
        event.preventDefault()
        setRedir(true)
    }
    return(
        <div className={'flex-column'}>
            <h1>Job retrieval page</h1>
            <form name={'retrieval'} className={'flex-column limit-width'} onSubmit={(event) => handleSubmit(event)}>
                <span className={'input-cell'}>
                    <label htmlFor={'id-input'}>Enter job id:</label>
                    <input className={'default-margins'} type={'text'} id={'id-input'} name={'id-input'} width={35}/>
                </span>
                <button type={'submit'}>Get job!</button>
            </form>
            {redir ? <Redirect to={'/job/' + document.getElementById('id-input').value}/> : null}
        </div>
    )
}

export default Retrieval