<script>
import { Router, Link, Route } from "svelte-routing";

import Navbar from '../components/Navbar';
import Cart from './Cart';
import CreateCategory from './CreateCategory';
import CreateFoodItem from './CreateFoodItem';
import CreateSetMenu from './CreateSetMenu';
import Dashboard from './Dashboard';
import Menu from './Menu';
import ViewAllOrders from './ViewAllOrders';
import ViewMyOrders from './ViewMyOrders';
import ViewReceipt from './ViewReceipt';

let url = '/';

</script>

<style>
</style>

<div class="content">
  <Router url="{url}">
    <Navbar />
    <Route path="/" component="{Dashboard}" />
    <Route path="cart" component="{Cart}" />
    <Route path="createCategory" component="{CreateCategory}" />
    <Route path="createFoodItem" component="{CreateFoodItem}" />
    <Route path="createSetMenu" component="{CreateSetMenu}" />
    <Route path="menu" component="{Menu}" />
    <Route path="orders" component="{ViewAllOrders}" />
    <Route path="myOrders" component={ViewMyOrders} />
    <Route path="viewReceipt" component="{ViewReceipt}" />
  </Router>
</div>
