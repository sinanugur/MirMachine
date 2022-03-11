import {HakeSirkelIkon, KryssSirkelIkon} from "@sb1/ffe-icons-react";

const Loader = (props) => {
    if(props.status === 'halted'){
        return(
            <div className={'loading-container'}>
                <KryssSirkelIkon className={'fill-warning-color'}/>
                <p>Something went wrong with your job</p>
            </div>
        )
    } else if(props.status === 'completed'){
        return(
            <div className={'loading-container'}>
                <HakeSirkelIkon className={'fill-main-color'}/>
                <p>Job completed!</p>
            </div>
        )
    } else {
        return(
            <div className={'loading-container'}>
                <span className={'loader-circle'}>
                <img src={'/static/assets/mirm_logo.png'} alt='Mir logo' className={'loader'}/>
                </span>
                <p>Working...</p>
            </div>
        )
    }
}
export default Loader