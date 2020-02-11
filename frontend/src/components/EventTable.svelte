<script>
  import{ getAllEvents } from '../api';
  import { Link, navigate } from "svelte-routing";

  let events = [];
  let eventsDisplayed = [];
  let id = 0;

  let queryTextForEvent = "",
    queryTextForLocation = "";

 getAllEvents() 
   .then(r => r.json())
   .then(function(r) {
      events = r;
      eventsDisplayed = r;
    })
    .catch(function(error) {
      console.log(error);
    });
  /* 
  function viewAttendees() {
    navigate("viewAttendees", { replace: true });
  } */

  function searchEvent() {
    console.log(queryTextForEvent);

    if (queryTextForEvent === "") eventsDisplayed = events;
    else
      eventsDisplayed = events.filter(e =>
        e.name.toUpperCase().includes(queryTextForEvent.toUpperCase())
      );
  }
  function searchLocation() {
    console.log(queryTextForLocation);
    if (queryTextForLocation === "") eventsDisplayed = events;
    else
      eventsDisplayed = events.filter(e =>
        e.location.toUpperCase().includes(queryTextForLocation.toUpperCase())
      );
  }

  function selectSearchField() {
    if (document.getElementById("searchLocation").disabled == true) {
      document.getElementById("searchEvent").value = "";
      document.getElementById("searchLocation").disabled = false;
      document.getElementById("searchEvent").disabled = true;
    } else {
      document.getElementById("searchLocation").value = "";
      document.getElementById("searchLocation").disabled = true;
      document.getElementById("searchEvent").disabled = false;
    }
    eventsDisplayed = events;
  }
</script>

<style>
  table {
    width: 80vw;
    border-collapse: collapse;
    border-radius: 3px;
    margin-bottom: 5vh;
    counter-reset: rowNumber;
  }

  .eventRow {
    counter-increment: rowNumber;
  }

  /* table,
  tr, */
  .tableData:first-child::before {
    content: counter(rowNumber);
  }

  tr {
    height: 8vh;
    border: 1px black solid;
  }

  .filter {
    margin: 15px;
    display: inline-block;
  }
</style>

<div class="filter">
  <input
    type="radio"
    name="choice"
    value="Location"
    id="location"
    on:change={selectSearchField} />
  <label for="location">Location:</label>
  <input
    type="text"
    on:keyup={searchLocation}
    placeholder="Search for location.."
    disabled
    title="Type in a location"
    id="searchLocation"
    bind:value={queryTextForLocation} />
</div>
<div class="filter">
  <input
    type="radio"
    name="choice"
    value="Event"
    id="event"
    checked="true"
    on:change={selectSearchField} />
  <label for="event">Event:</label>
  <input
    type="text"
    on:keyup={searchEvent}
    placeholder="Search for events.."
    title="Type in a event"
    id="searchEvent"
    bind:value={queryTextForEvent} />
</div>
<table id="eventTable">
  <tr>
    <th>N.o.</th>
    <th>Event Name</th>
    <th>Location</th>
    <th></th>
  </tr>
  {#if (eventsDisplayed != [])}
  {#each eventsDisplayed as event}
    <tr class="eventRow">

      <td class="tableData" />
      <td class="tableData">{event.name}</td>
      <td class="tableData">
      {#each event.locations as locations} 
          {locations.name + " "}
      {/each}</td> 
      <td></td>
    </tr>
    {/each}
  {:else}
    <tr>
      <td colspan="100%">
        <h5 class="text-center">There are no Events.</h5>
      </td>
    </tr>
  {/if}

</table>
