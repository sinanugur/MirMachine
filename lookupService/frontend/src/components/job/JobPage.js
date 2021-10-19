import { useParams, Link, Redirect } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { fetchJob, cancelJob } from '../../utils/Repository'
import { connectToSocket } from '../../utils/WebSockets'
import { formatDjangoTime, updateClockAndFormatString, getTimeConsumed } from '../../utils/TimeManagers'
import Loader from './Loader'
import ProgressBar from "./ProgressBar";

const Job = () => {
    const { jobID } = useParams()
    const [jobData, setJobData] = useState()
    const [redirectHome, setRedirectHome] = useState(false)
    const [redirectResults, setRedirectResults] = useState(false)
    const [error, setError] = useState()
    const [socket, setSocket] = useState()
    const [socketStatus, setSocketStatus] = useState()
    const [socketProgress, setSocketProgress] = useState()
    const [queueNumber, setQueueNumber] = useState()
    const [initTime, setInitTime] = useState()
    const [completedTime, setCompletedTime] = useState()
    const [elapsed, setElapsed] = useState()
    const [intervalMethod, setIntervalMethod] = useState()

    useEffect(() => {
        const getJobData = async () => {
            try {
                let data = await fetchJob(jobID)
                setJobData(data)
                setInitTime(data.initiated)
                setSocketStatus(data.status)
                setCompletedTime(data.completed)
                if(data.status !== 'halted' && data.status !== 'completed')
                    setSocket(connectToSocket(jobID, setSocketStatus,
                        setSocketProgress, setQueueNumber, setInitTime, setCompletedTime))
                else if(data.status !== 'queued'){
                    setElapsed(getTimeConsumed(data.initiated, data.completed))
                }
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
            socket.close(1000, 'Got required info')
            if(intervalMethod){
                console.log('Stopping interval')
                clearInterval(intervalMethod)
            }
        } else if(socketStatus === 'ongoing'){
            setIntervalMethod(initializeTimer(initTime))
        }
    },[socketStatus])

    const initializeTimer = (startTime) => {
        const timeInterval = setInterval(() => {
            setElapsed(updateClockAndFormatString(startTime))
        },1000)
        return timeInterval
    }
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
                <span>Dataset hash (MD5): {jobData.hash}</span>
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
                {elapsed && <span>{elapsed}</span>}
                {socketProgress && <ProgressBar progress={socketProgress}/>}
                {socketStatus === 'completed' ?
                    <span className={'button button--action'} onClick={() => {
                        setRedirectResults(true)
                    }}>
                        View results
                    </span> : null}
                <span className={'button button--reset'} onClick={() => {
                    cancelJob(jobID)
                    setRedirectHome(true)
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
            {redirectHome &&
                <Redirect to={'/'}/>
            }
            {redirectResults &&
                <Redirect to={`/result/${jobID}`}/>
            }
        </div>
    )
}


export default Job