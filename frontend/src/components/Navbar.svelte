<style>
  nav {
    height: 80px;
    padding: 15px;
    text-align: left;
    line-height: 80px;
  }
  #logo {
    font-size: 31px;
    font-weight: bold;
  }
  #controls {
     float: right;
  }
</style>

<script>

  import { token, user } from '../stores';
  import { navigate, Link } from 'svelte-routing';

  function logOut() {
    token.unset();
    user.unset();
    navigate('/', { replace: true });
  }
</script>

<nav>
   <Link to='/'>
     <span id="logo">Food Ordering System!</span>
   </Link>
   <small> &nbsp &nbsp Logged in as {$user.name} ({$user.role}) </small>
   <div id="controls"> 
    {#if $user.role === 'customer'}
      <Link to='/cart'>Cart</Link>
    {/if}
    <Link to='/' on:click={logOut}>Log out</Link>
   </div>
</nav>
