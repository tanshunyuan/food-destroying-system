<script>
  import Login from './views/Login';
  import Router from './views/Router';
  
  import { token, user } from './stores';
  
</script>

{#if $token && $user }
  <Router />
{:else}
  <Login />
{/if}

