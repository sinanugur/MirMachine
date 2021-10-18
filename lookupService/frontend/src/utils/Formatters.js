
export const formatDjangoTime = (djangoTime) => {
    return djangoTime.split('T')[0] + ' @ ' + djangoTime.split('T')[1].substring(0,5) + ' GMT'
}

export const getElapsedTime = (startTime) => {
    const start = Date.parse(startTime.split('T')[0] + ' ' + startTime.split('T')[1].split('.')[0])
    const now = Date.parse(new Date().toLocaleString('en-US', {timeZone: 'UTC'}))
    const elapsed = now - start
    const seconds = Math.floor((elapsed/1000) % 60)
    const minutes = Math.floor((elapsed/1000/60) % 60)
    const hours = Math.floor(elapsed/(1000*60*60))
    return {hours, minutes, seconds}
}

export const updateClockAndFormatString = (startTime) => {
    let cur = getElapsedTime(startTime)
    return `Elapsed: ${cur.hours}h:${cur.minutes}m:${cur.seconds}s`

}