import { useParams, Link } from 'react-router-dom'
import { useEffect, useState } from "react";
import { fetchJob } from "../utils/Repository";

const Job = () => {
    const { jobID } = useParams()
    const [jobData, setJobData] = useState()
    const [error, setError] = useState()
    useEffect(() => {
        const getJobData = async () => {
            try {
                let data = await fetchJob(jobID)
                console.log(data)
                setJobData(data)
            } catch(err) {
                setError(err.message)
            }
        }
        getJobData()
    },[])
    return(
        <div className={'flex-column'}>
            {jobData &&
            <>
            <h1> Your job</h1>
                <span>ID: {jobData.id}</span>
                <span>Status: {jobData.status}</span>
                <span>Initiated at: {jobData.initiated.split('T')[0] + ' @ ' + jobData.initiated.split('T')[1].substring(0,5) + ' GMT'}</span>
                <span>Dataset hash: {jobData.hash}</span>
                <span>Species tag: {jobData.species}</span>
                <span>Model type: {jobData.model_type === 'both' ? jobData.model_type : jobData.model_type + 'stome'}</span>
                {jobData.single_fam_mode ? null :
                    <>
                    <span>Node: {jobData.node}</span>
                    <span>Single node: {jobData.single_node ? 'yes' : 'no'}</span></>
                }
                <span>Single family mode: {jobData.single_fam_mode ? 'yes' : 'no'}</span>
                {jobData.single_fam_mode ?
                    <span>Family: {jobData.family}</span> : null
                }
                {jobData.mail_address == '' ? null :
                    <span>{`E-mail: ${jobData.mail_address}`}</span>
                }
                <div className={'loading-container'}>
                    <img src={'/static/mir.svg'} alt='Mir logo'className={'loader'}/>
                    <p>Working...</p>
                </div>
                <div className={'info-pane'}>
                    Please store your job ID safely for later reference.<br/>
                    This is needed to access your results if you didn't register your email.<br/>
                    Large MirMachine jobs can be quite time consuming,
                    and your page may timeout in the meantime, which is why this is necessary.<br/>
                    To access your job, head over to the "Ongoing Job" section and enter your ID.<br/>
                    From there you can also choose to cancel your job if you want to make adjustments.<br/>
                    Therefore, you shouldn't share the ID with anyone you don't trust.<br/>
                    Once you have stored your id, you may close this page. <br/>
                    If you registered your email, you will be notified when your job is complete.
                </div>
            </>
            }
            {error &&
            <>
                <div className={'info-pane'}>{error}</div>
                <Link to='/retrieve'>
                    <span className={'button button--reset'}>
                       Back to retrieval page
                    </span>
                </Link>
            </>
            }
        </div>
    )
}
export default Job