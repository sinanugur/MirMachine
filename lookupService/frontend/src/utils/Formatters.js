
export const formatDjangoTime = (djangoTime) => {
    return djangoTime.split('T')[0] + ' @ ' + djangoTime.split('T')[1].substring(0,5) + ' GMT'
}