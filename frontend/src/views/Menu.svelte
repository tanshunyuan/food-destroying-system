<script>
  import { getFoods, deleteFood, getSetMenus, getSetItems,getCategorys } from "../api";
  import { Link, navigate } from "svelte-routing";
  import { onMount } from "svelte";
  import { user, selectedFood } from "./../stores.js";
  import { get, set } from "svelte/store";
  import axios from "axios";
  import { Confirm } from "svelte-confirm";

  let foods = [];
  let category = [];
  let categoryDisplayed = [];
  let setMenu = [];
  let foodsDisplayed = [];
  let setMenuDisplayed = [];
  let setItemDisplayed = [];
  let id = 0;
  let dialogOpen = false;
  let queryTextForSetmenu = "";

  let queryTextForCategory = "";
  onMount(() => {
    getFoods()
      .then(r => r.json())
      .then(response => {
        foods = response.result;
        foodsDisplayed = response.result;
      });
    getCategorys()
      .then(r => r.json())
      .then(response => {
        category = response.result;
        categoryDisplayed = response.result;
        console.log(response);
      });
    getSetMenus()
      .then(r => r.json())
      .then(response => {
        setMenu = response.result
        setMenuDisplayed = response.result;
        //console.log(setMenuDisplayed)
      });
     getSetItems()
      .then(r => r.json())
      .then(response => {
        setItemDisplayed = response;
        console.log(response)
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

  function searchCategory() {
    console.log(queryTextForCategory);
    if (queryTextForCategory === "") categoryDisplayed = category;
    else
      categoryDisplayed = category.filter(e =>
        e.name.toUpperCase().includes(queryTextForCategory.toUpperCase())
      );
  }

  function searchSetMenu() {
    console.log(queryTextForSetmenu);
    if (queryTextForSetmenu === "") setMenuDisplayed = setMenu;
    else
      setMenuDisplayed = setMenu.filter(e =>
        e.name.toUpperCase().includes(queryTextForSetmenu.toUpperCase())
      );
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

<h1>Food Menu</h1>
<div class="filter">
  <label for="name">Category Name:</label>
  <input
    type="text"
    on:keyup={searchCategory}
    placeholder="Search for Category.."
    title="Type in a Category"
    id="searchFood"
    bind:value={queryTextForCategory} />
</div>
<br>
<table id="foodTable">
  <tr>
    <th>Food Name</th>
    <th>Description</th>
    <th>Category</th>
    <th>Price</th>
    {#if $user.role === 'manager'}
      <th>Unit</th>
      <th>Status</th>
    {/if}
    <th>Action</th>
  </tr>
  {#if categoryDisplayed != []}
    {#each categoryDisplayed as cat}
    {#if foodsDisplayed != []}
      {#each foodsDisplayed as food}
      {#if food.category == cat.id}
      <tr>
        <td class="tableData">{food.name}</td>
        <td class="tableData">{food.description}</td>
        <td class="tableData">{cat.name}</td>
        <td class="tableData">${food.price}</td>
        {#if $user.role === 'manager'}
          <td class="tableData">{food.unit}</td>
          <td class="tableData">{food.status}</td>
        {/if}
        <td>
          <div>
            {#if $user.role === 'customer'}
              <button>
                <img src="./../../public/cart.png" alt="Add to Cart" />
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
      {/if}
    {/each}
  {:else}
    <tr>
      <td colspan="100%">
        <h5 class="text-center">There are no Foods.</h5>
      </td>
    </tr>
    {/if}
    {/each}
  {/if}

</table>

<h1>Set Menu</h1>
<div class="filter">
  <label for="name">Set Item Name:</label>
  <input
    type="text"
    on:keyup={searchSetMenu}
    placeholder="Search for Set Item.."
    title="Type in a Set Item name"
    id="searchSetItem"
    bind:value={queryTextForSetmenu} />
</div>
<br>
<table id="foodTable">
  <tr>
    <th>Set Name</th>
    <th>Set Items</th>
    <th>Price</th>
    <th>Size</th>
    <th>Action</th>
  </tr>
  {#if setMenuDisplayed != []}
    {#each setMenuDisplayed as setMenu}
      <tr>
        <td class="tableData">{setMenu.name}</td>
        
        {#each setItemDisplayed as setItem}
          {#if setItem.setmenu_id == setMenu.id}
          <td class="tableData">{setItem.name}<br></td>
          <td class="tableData">${setItem.totalPrice}</td>
          <td class="tableData">{setItem.size}</td>
          {/if}
        {/each}
        
        <td>
          <div>
            {#if $user.role === 'customer'}
              <button>
                <img src="./../../public/cart.png" alt="Add to Cart" />
              </button>
            {/if}
            {#if $user.role === 'manager'}
              <button>
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
                  >
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
        <h5 class="text-center">There are no set menus.</h5>
      </td>
    </tr>
  {/if}

</table>

