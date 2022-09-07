import { useEffect, useState } from "react"


function FetchEvent() {
    const [Events, setEventsData] = useState([])
    const [error, setError] = useState("")


    useEffect(() => {
        const getEventData = async () => {
            const url = `${process.env.REACT_APP_EVENTS}/events/` // Will need to update this to dynamic url (.../events/1/)
            const response = await fetch(url)
            if (response.ok) {
                const data = await response.json()
                // console.log(data)
                setEventsData(data["Events"])
            } else {
                setError("Could not load the events, try again")
            }
        }
        getEventData()
    }, [setEventsData, setError])

    return (
        <>
            <div className='m-3'>
                <h1 className='display-4'> {Events[0]?.name || ''}</h1>
                {<img src={Events[0]?.picture_url} className='img-fluid max-width: 100%' />}
                <p className='lead'> Description: {Events[0]?.description || ''}</p>
                <p className='lead'> Activity: {Events[0]?.activity.name || ''}</p>
                <p className='lead'>Date: {new Date(Events[0]?.start).toLocaleString()} - {new Date(Events[0]?.end).toLocaleString()}</p>
            </div>
        </>
    )
}

export default FetchEvent