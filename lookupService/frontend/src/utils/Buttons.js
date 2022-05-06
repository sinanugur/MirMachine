

export const handleButtonKeyPress = (event, header) => {
    let key = event.key
    if(key === "Enter"){
        if(header){
            event.target.firstChild.click()
        } else {
            event.target.click()
        }
    }
}