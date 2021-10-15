

const ProgressBar = (props) => {
    console.log(props.progress)
    return(
        <div className={'progress-container'}>
            <span className={'progress-bar'}>
                <span className={'progress'} style={{width: props.progress}}>
                    {props.progress}
                </span>
            </span>
        </div>
    )
}

export default ProgressBar