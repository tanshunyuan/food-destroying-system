<script>
import { Router, Link, Route } from "svelte-routing";

import Navbar from '../components/Navbar';
import Dashboard from './Dashboard';

let url = '/';

</script>

<style>
</style>

<div class="content">
  <Router url="{url}">
    <Navbar />
    <Route path="/" component="{Dashboard}" />
  </Router>
</div>
