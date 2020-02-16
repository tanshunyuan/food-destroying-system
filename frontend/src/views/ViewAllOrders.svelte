<!-- Manager and Chef -->

<!-- Chef:  Allow options to prepare order & ready order -->
<!-- Manager: View all orders made -->
<script>
    import { OrderState, Order, currentTime } from "../components/OrderState.js";
    import { user } from "./../stores.js";
    import { onMount } from "svelte";
    import { getOrders, updateOrderStatus } from '../api';
    import axios from "axios";

    let orders = [];

    // Get all orders
    onMount(() => {
        // DEBUG ONLY: CHANGE STATE OF ORDER TO NEW
        // axios
        // .put(`${process.env.API_URL}api/order`, {
        //     id: '1',
        //     orderStatus: 'new'
        // })
        // .then(
        //     response => { 
        //         console.log(response)
        //     },
        //     error => {
        //         console.log(error);
        //         errorMsg = "Order cannot be updated.";
        //     }
        // );
        
        getOrders()
        .then(r => r.json())
        .then(response => {
            orders = response;
        });
    });
    
    function convertToTime(time) {
        return time.slice(11, 19);
    }

    function getCurrentState(order) {
        var state = new OrderState(order);
        return state;
    }

    function getDisplayedOrders(orders) {
        let displayedOrders = [];
        for (var i = 0; i < orders.length; i++) {
            if (orders[i].orderStatus === 'new' || orders[i].orderStatus === 'preparing') {
                displayedOrders.push(orders[i]);
            }
        }
        console.log(displayedOrders)
        return displayedOrders;
    }
</script>
  
<div class="content">
    <h1>All Pending Orders</h1>
    <h4><i>Current Time: {currentTime()}</i></h4>
    <br>
    <table id="eventTable">

    {#if getDisplayedOrders(orders).length != 0}
    <tr>
        <th>Time Ordered</th>
        <th>Ordered Items</th>
        <th>Status</th>
        <th>Actions</th>
    </tr>
        {#each getDisplayedOrders(orders) as order}
        <tr>
            <!-- Time -->
            <td class="tableData">{convertToTime(order.createdDateTime)}</td>
            
            <!-- Ordered Items -->
            <td class="tableData">
            {#each order.orderedItems as item}
                {item.name}<br>
            {/each}
            </td>

            <!-- Status -->
            <td>{order.orderStatus}</td>

            <!-- Actions -->
            <td>
            <div>
                {#if $user.role === 'employee'}
                    {#if order.orderStatus === 'new'}
                    <button on:click={getCurrentState(order).current.chefAcceptsOrder(order, getCurrentState(order))}>Prepare Order 🔥</button>
                    {/if}

                    {#if order.orderStatus === 'preparing'}
                    <button on:click={getCurrentState(order).current.chefUpdateOrder(order, getCurrentState(order))}>Ready 👍</button>
                    {/if}
                {/if}
            </div>
            </td>
        </tr>
        {/each}
    
    {:else}
        <tr>
        <td colspan="100%">
            <h5>There are no new orders at the moment.</h5>
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
h5 {
    text-align: center;
}
td:first-letter {
    text-transform:capitalize;
}
</style>