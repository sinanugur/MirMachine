
export const formatDjangoTime = (djangoTime) => {
    return djangoTime.split('T')[0] + ' @ ' + djangoTime.split('T')[1].substring(0,5) + ' GMT'
}

const getElapsedTime = (startTime, endTime) => {
    const start = Date.parse(startTime.split('T')[0] + ' ' + startTime.split('T')[1].split('.')[0])
    const now = endTime ? Date.parse(endTime.split('T')[0] + ' ' + endTime.split('T')[1].split('.')[0]) :
        Date.parse(new Date().toLocaleString('en-US', {timeZone: 'UTC'}))
    const elapsed = now - start
    const seconds = Math.floor((elapsed/1000) % 60)
    const minutes = Math.floor((elapsed/1000/60) % 60)
    const hours = Math.floor(elapsed/(1000*60*60))
    return {hours, minutes, seconds}
}

export const updateClockAndFormatString = (startTime) => {
    let cur = getElapsedTime(startTime, undefined)
    return `Elapsed: ${cur.hours}H:${cur.minutes}M:${cur.seconds}S`
}

export const getTimeConsumed = (startTime, endTime) => {
    let cur = getElapsedTime(startTime, endTime)
    return `Time used: ${cur.hours}H:${cur.minutes}M:${cur.seconds}S`
}
