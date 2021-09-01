import { useParams } from 'react-router-dom'
import { useEffect, useState } from "react";
import { fetchJob } from "../utils/Repository";

const Job = () => {
    const { jobID } = useParams()
    const [jobData, setJobData] = useState()
    useEffect(() => {
        const getJobData = async () => {
            let data = await fetchJob(jobID)
            setJobData(data)
        }
        getJobData()
    },[])
    return(
        <div className={'flex-column'}>
            {jobData &&
            <>
            <h1> Your job</h1>
                <span>ID: {jobData.id}</span>
                <span>Status: ongoing</span>
                <span>Initiated at: {jobData.initiated.split('T')[0] + ' @ ' + jobData.initiated.split('T')[1].substring(0,5) + ' GMT'}</span>
                <span>Mode: {jobData.mode}</span>
                <span>Species tag: {jobData.species}</span>
                <span>Node: {jobData.node}</span>
                <span>Model type: {jobData.model_type}</span>
                <span>Dry run: {jobData.dry_run ? 'yes' : 'no'}</span>
                <span>Single family mode: {jobData.single_fam_mode ? 'yes' : 'no'}</span>
                <span>E-mail: {jobData.mail_address}</span>
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
        </div>
    )
}
export default Job