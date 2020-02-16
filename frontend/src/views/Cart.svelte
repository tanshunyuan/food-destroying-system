<script>
  import { onMount } from 'svelte';
  import { cart, user } from '../stores';
  import { getFoods, postOrder } from '../api';

  let itemNames = {};
  let itemPrices = {};
  let cartItems = []; // Exclusive list

  function makeOrder() {
    postOrder({
       customer_id: $user.id,
       deliveryDateTime: (new Date()).toISOString(),
       readyDateTime: (new Date()).toISOString(),
       orderStatus: 'new',
       totalAmount: getTotalCost(),
       food_ids: $cart
    }).then(r => {
      if (r.status === 200) cart.set([]);
    })
    .catch(console.error);
  }

  function getItemCount(id) {
    return $cart.filter(c => c === id).length;
  }

  function getTotalCost() {
    return cartItems.reduce((total, item) => total + (getItemCount(item) * itemPrices[item]), 0);
  }

  onMount(() => 
    getFoods()
    .then(r => r.json())
    .then(foods => {
        // Set food names hash map
        foods.result.forEach(food => {
          itemNames[food.id] = food.name;
          itemPrices[food.id] = food.price;
        });
        // Build cart items display
        console.log($cart);
        cartItems = $cart.reduce((acc, id) => {
          if (acc.filter(i => i === id).length === 0) acc.push(id);
          return acc;
        }, []);
      }).catch(console.error)
    );

</script>

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
  }
</style>

<div class="content">
  {#if cartItems.length !== 0}
    <table>
      <tr>
        <th>Item</th>
        <th>Qty</th>
        <th>Price</th>
      </tr>
      {#each cartItems as item}
        <tr>
          <td>{itemNames[item]}</td>
          <td>{getItemCount(item)}</td>
          <td>${getItemCount(item) * itemPrices[item]}</td>
        </tr>
      {/each}
      <tr>
        <td></td>
        <td><strong>Total:</strong></td>
        <td>${getTotalCost()}</td>
      </tr>
    </table>
  {:else}
    <p> No items in cart! </p>
  {/if}
  <button on:click={makeOrder}>Make an Order</button>
</div>
