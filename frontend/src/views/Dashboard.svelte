<script>
  import { onMount } from "svelte";
  import { Link } from "svelte-routing";
  import { user } from "./../stores.js";
</script>

<div class="content">
  <!-- <h1>Food Menu</h1>
  <h1>My Orders</h1>
  <h1>Order History</h1> -->
  {#if $user.role === 'manager'}
    <h1>Orders</h1>
    <Link to="orders">
      <div class="button">View All Orders</div>
    </Link>
    <h1>Menu Management</h1>
    <Link to="menu">
      <div class="button">View Menu</div>
    </Link>
    <Link to="createCategory">
      <div class="button">Create Food Category</div>
    </Link>
    <Link to="createFoodItem">
      <div class="button">Create Food Item</div>
    </Link>
    <Link to="createSetMenu">
      <div class="button">Create Set Menu</div>
    </Link>
  {/if}

  {#if $user.role === 'employee'}
     <h1>Orders</h1>
    <Link to="orders">
      <div class="button">View All Orders</div>
    </Link>
  {/if}

  {#if $user.role === 'dispatcher'}
     <h1>Orders</h1>
    <Link to="orders">
      <div class="button">View All Orders</div>
    </Link>
  {/if}

  {#if $user.role === 'customer'}
      <Link to="menu">
      <div class="button">View Menu</div>
    </Link>
    <Link to="cart">
      <div class="button">My Cart</div>
    </Link>
    <Link to="myOrders">
      <div class="button">View Order History</div>
    </Link>
  {/if}

</div>
