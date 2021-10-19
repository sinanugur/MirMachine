

const ProgressBar = (props) => {
    console.log(props.progress)
    return(
        <div className={'progress-container'}>
            <span className={'progress-bar'}>
                <p className={'no-margins progress-text'}>{props.progress}</p>
                <span className={'bar-container'}>
                    <span className={'progress'} style={{width: props.progress}}/>
                </span>
            </span>
        </div>
    )
}

export default ProgressBar