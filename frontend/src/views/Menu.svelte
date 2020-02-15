<script>
  import { getFoods } from "../api";
  import { Link, navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import { user } from "./../stores.js";

  let foods = [];
  let foodsDisplayed = [];
  let id = 0;

  let queryTextForFood = "";
  onMount(() => {
    getFoods()
      .then(r => r.json())
      .then(response => {
        foods = response.result;
        foodsDisplayed = response.result;
      });
  });
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
        {/if}
        <td>
          <div>
            {#if $user.role === 'customer'}
              <button>
                <img src="./../../public/cart.png" alt="Add to Cart" />
              </button>
            {/if}
            {#if $user.role === 'manager'}
              <button >
                <img src="./../../public/edit.png" alt="Update" />
              </button>
              <button>
                <img src="./../../public/bin.png" alt="Delete" />
              </button>
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
