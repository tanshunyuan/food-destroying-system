<script>
  import { getAttendance, getStudents, getAllEvents } from '../api';
  import { onMount } from 'svelte';

  let attendanceRecords = null;
  let students, events;

  export const fetchAttendance = (eventID) => getAttendance(eventID).then(r => r.json())
      .then(response => {
        attendanceRecords = response.data;
      })
      .catch(console.error);  

  onMount(() => {
      Promise.all([getStudents(), getAllEvents()])
      .then(async (results) => Promise.all(results.map(r => r.json())))
      .then(([s, e]) => {
        students = s.data;
        events = e;
      });
  });

  function getStudentName(id) {
    return students.filter(s => s.id === id)[0].name;
  }

  function getEventName(id) {
    return events.filter(e => e.id === id)[0].name;
  }

</script>

<style>
table {
  width: 100%;
}
</style>

<table>
<tr>
  <th>Name</th>
  <th>Type</th>
  <th>Event</th>
  <th>Date and Time</th>
</tr>
{#if attendanceRecords !== null}
  {#if attendanceRecords.length < 1}
    <p> No attendance records! </p>
  {:else} 
    {#each attendanceRecords as attendance}
      <tr>
        <td>{getStudentName(attendance.user_id)}</td>
        <td>Student</td>
        <td>{getEventName(attendance.event_id)}</td>
        <td>{attendance.date_time}</td>
      </tr>
    {/each}
  {/if}
{:else}
  <p> Loading... </p>
{/if}
</table>
