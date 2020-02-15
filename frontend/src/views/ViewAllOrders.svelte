<!-- Manager and Chef -->

<!-- Chef:  Allow options to prepare order & ready order -->
<!-- Manager: View all orders made -->
<script>
    import { OrderState } from "../components/OrderState.js";
    import { Order } from "../components/OrderState.js";
    // import { state } from "../components/OrderState.js";
    import { currentTime } from "../components/OrderState.js";
    import { user } from "./../stores.js";
    import { onMount } from "svelte";
    import { getOrders } from '../api';

    let orders = [];

    // Get all orders
    onMount(() => {
        getOrders()
        .then(r => r.json())
        .then(response => {
            orders = response;
        });
    });
    
    function convertToTime(time) {
        return time.slice(11, 19);
    }
</script>
  
<div class="content">
    <h1>All Pending Orders</h1>
    <h4><i>Current Time: {currentTime()}</i></h4>
    <br>
    <table id="eventTable">

    <tr>
        <th>Time Ordered</th>
        <th>Ordered Items</th>
        <th>Actions</th>
    </tr>

    {#if orders != []}
        {#each orders as order}
        <tr>
            <td class="tableData">{convertToTime(order.createdDateTime)}</td>
            <td class="tableData">
            {#each order.orderedItems as item}
                {item.name}<br>
            {/each}
            </td>
            <td>
            <div>
                {#if $user.role === 'employee'}
                    {#if order.current.order === 'new'}
                    <button on:click={state.change()}>Prepare Order 🔥</button>
                    {/if}
                    {#if state.current.order === 'preparing'}
                    <button on:click={state.current.chefUpdateOrder()}>Ready 👍</button>
                    {/if}
                {/if}
            </div>
            </td>
        </tr>
        {/each}
    {:else}
        <tr>
        <td colspan="100%">
            <h5 class="text-center">There are no pending orders!</h5>
        </td>
        </tr>
    {/if}

    </table>
</div>


<style>
table {
    width: 100%;
}
tr:hover {
    background: whitesmoke;
}
.selected {
    background: whitesmoke;
}
td,
th {
    text-align: left;
    word-wrap: break-word;
}
</style>