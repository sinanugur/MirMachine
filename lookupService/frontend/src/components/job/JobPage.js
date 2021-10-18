import { useParams, Link, Redirect } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { fetchJob, cancelJob } from '../../utils/Repository'
import { connectToSocket } from '../../utils/WebSockets'
import { formatDjangoTime } from '../../utils/Formatters'
import Loader from './Loader'
import ProgressBar from "./ProgressBar";

const Job = () => {
    const { jobID } = useParams()
    const [jobData, setJobData] = useState()
    const [redirect, setRedirect] = useState(false)
    const [error, setError] = useState()
    const [socket, setSocket] = useState()
    const [socketStatus, setSocketStatus] = useState()
    const [socketProgress, setSocketProgress] = useState()
    const [queueNumber, setQueueNumber] = useState()
    const [initTime, setInitTime] = useState()
    const [completedTime, setCompletedTime] = useState()
    useEffect(() => {
        const getJobData = async () => {
            try {
                let data = await fetchJob(jobID)
                setJobData(data)
                setSocketStatus(data.status)
                setInitTime(data.initiated)
                setCompletedTime(data.completed)
                if(data.status !== 'halted' && data.status !== 'completed')
                    setSocket(connectToSocket(jobID, setSocketStatus,
                        setSocketProgress, setQueueNumber, setInitTime, setCompletedTime))
            } catch(err) {
                setError(err.message)
            }
        }
        getJobData()
        return () => {
            if(socket)
                if(socket.readyState === 1) // 1 = OPEN
                    socket.close(1000, 'User left')
        }
    },[])
    useEffect(() => {
        if((socketStatus === 'halted' || socketStatus === 'completed') && socket){
            console.log('trying to close socket in socketMessage useEffect')
            socket.close(1000, 'Got required info')
        }
    },[socketStatus])
    return(
        <div className={'flex-column'}>
            {jobData &&
            <>
            <h1> Your job</h1>
                <span>ID: {jobData.id}</span>
                <span>
                    Status: {socketStatus && socketStatus}
                </span>
                {socketStatus && queueNumber && socketStatus === 'queued' ?
                <span>Position in queue: {queueNumber}</span> : null}
                <span>Submitted at: {formatDjangoTime(jobData.submitted)}</span>
                {initTime && <span>Initiated at: {formatDjangoTime(initTime)}</span>}
                {completedTime && <span>Completed at: {formatDjangoTime(completedTime)}</span>}
                <span>Dataset hash: {jobData.hash}</span>
                <span>Species tag: {jobData.species}</span>
                <span>Model type: {jobData.model_type === 'combined' ? jobData.model_type : jobData.model_type + 'stome'}</span>
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
                <Loader status={socketStatus}/>
                {socketProgress && <ProgressBar progress={socketProgress}/>}
                <span className={'button button--reset'} onClick={() => {
                    cancelJob(jobID)
                    setRedirect(true)
                }}>
                    {socketStatus === 'ongoing' ? 'Cancel job' : 'Delete job'}
                </span>
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
            {redirect &&
                <Redirect to={'/'}/>
            }
        </div>
    )
}
export default Job