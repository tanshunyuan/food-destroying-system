<script>
  import { getFoods, deleteFood } from "../api";
  import { Link, navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import { user, selectedFood, cart } from "./../stores.js";
  import { get, set } from "svelte/store";
  import axios from "axios";
  import { Confirm } from "svelte-confirm";

  let foods = [];
  let foodsDisplayed = [];
  let id = 0;
  let dialogOpen = false;

  let queryTextForFood = "";
  onMount(() => {
    getFoods()
      .then(r => r.json())
      .then(response => {
        foods = response.result;
        foodsDisplayed = response.result;
      });
  });

  function updateFood(food) {
    selectedFood.set(food);
    navigate("UpdateFoodItem", { replace: true });
  }

  function deactiveFoodItem(food) {
    axios
      .put(`${process.env.API_URL}api/food`, {
        id: food.id,
        name: food.name,
        status: false,
        price: food.price,
        description: food.description,
        unit: food.unit
      })
      .then(response => {
        navigate("/", { replace: true });
      });
  }

  function addToCart(food) {
    cart.set([...$cart, food.id]);
    console.info($cart);
  }
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

<h1>Menu</h1>
<table id="eventTable">
  <tr>
    <th>food Name</th>
    <th>description</th>
    <th>price</th>
    {#if $user.role === 'manager'}
      <th>unit</th>
      <th>status</th>
    {/if}
    <th>action</th>
  </tr>
  {#if foodsDisplayed != []}
    {#each foodsDisplayed as food}
      <tr>
        <td class="tableData">{food.name}</td>
        <td class="tableData">{food.description}</td>
        <td class="tableData">{food.price}</td>
        {#if $user.role === 'manager'}
          <td class="tableData">{food.unit}</td>
          <td class="tableData">{food.status}</td>
        {/if}
        <td>
          <div>
            {#if $user.role === 'customer'}
              <button on:click={() => addToCart(food)}>
                + Add to Cart
              </button>
            {/if}
            {#if $user.role === 'manager'}
              <button on:click={() => updateFood(food)}>
                <img src="./../../public/edit.png" alt="Update" />
              </button>
              <Confirm
                confirmTitle="Delete"
                cancelTitle="Cancel"
                let:confirm={confirmThis}>
                <svg
                  style="width:24px;height:24px"
                  viewBox="0 0 24 24"
                  class="delete-icon"
                  on:click={() => confirmThis(deactiveFoodItem, food)}>
                  <path
                    fill="hsl(200, 40%, 20%)"
                    d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0
                    8,21H16A2,2 0 0,0 18,19V7H6V19Z" />
                </svg>
                <span slot="title">Delete this item?</span>
                <span slot="description">
                  You won't be able to revert this!
                </span>
              </Confirm>
            {/if}
          </div>
        </td>
      </tr>
    {/each}
  {:else}
    <tr>
      <td colspan="100%">
        <h5 class="text-center">There are no Foods.</h5>
      </td>
    </tr>
  {/if}

</table>
