import { useNavigate } from 'react-router-dom'
import React, { useState, useEffect, useRef } from 'react'
import { settingLinks } from "./Nav"

export default function PastEvents(props) {
  const events = useRef([])
  const [filteredEvents, setFilteredEvents] = useState([])
  const [search, setSearch] = useState('')
  const navigate = useNavigate()
  const [, , , , eventsLink] = settingLinks()
  const [searchedEvents, setSearchedEvents] = useState([])



  useEffect(() => {
    const requestEvents = async () => {
      const url = `${process.env.REACT_APP_EVENTS}/events/`
      const response = await fetch(url)
      if (response.ok) {

        const data = await response.json()
        events.current = data.Events
        const formerEvents= []
        const eventGrp = events.current

        for(let event of eventGrp){
          const endDate= new Date(event.end)
          const currentDate= new Date()
          if(currentDate > endDate){
            formerEvents.push(event)
          }
        }
        setFilteredEvents(formerEvents)

      } else {
        console.log("Could not load the events, try again")
      }
    }
    requestEvents()
  }, [])

  
  function searchFilter() {
    const searchedEvents = filteredEvents.filter(event => event.name.toLowerCase().includes(search.toLowerCase()))
    setSearchedEvents(searchedEvents)
  }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { searchFilter() }, [search])

  function handleChange(event) {
    setSearch(event.target.value) 
  }

  const eventsList = search.length < 1
        ? filteredEvents
        : searchedEvents;

  return (
    <>
      <div className='event-bg'></div>
      <div className="mt-3 mb-3">
        <div className='container'>
          <div className="row">
            <div className="col">
              <h1>Search Former Events</h1>
            </div>
            <div className="col align-right">
            <div><a className="btn btn-dark rounded-pill mb-3" href={`${eventsLink}create/`} role="button">Add Event</a></div>
            </div>
            <div className="align-right">
            <div><a className="btn btn-dark rounded-pill mb-3" href={`${eventsLink}/`} role="button">Search Current Events</a></div>
            </div>
          </div>
          </div>
        <div>
          <input
            type="search"
            id="search"
            className="form-control"
            placeholder="Search for events"
            onChange={handleChange}
            aria-label="Search"
          />
        </div>
        <div className="row">
          {eventsList.map(event => {
            return (
              <div className="col-sm-4 mt-3 mb-3" key={event.id}>
                <div className="card mb-3 shadow h-100 event-pointer"
                  onClick={() => {
                    navigate(`/events/${event.id}/`)
                  }}>
                  <img src={event.picture_url} className="card-img-top crop-image" alt="" />
                  <div className="card-body">
                    <h5 className="card-title">{event.name}</h5>
                    <h6 className="card-subtitle mb-2 text-muted">
                      {event.activity.name}
                    </h6>
                    <p className="card-text">
                      {event.description}
                    </p>
                  </div>

                  <div className="card-footer">
                    {new Date(event.start).toLocaleDateString()}
                    {/* -
                        {new Date(event.end).toLocaleDateString()} */}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
        </div>
      </>
      )
}