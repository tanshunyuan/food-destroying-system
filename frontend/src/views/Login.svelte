<script>
  import { userLogin } from '../api';
  import { token, user } from '../stores';

  let email = '', password = '', error = '';
  function handleForgotPassword() {
    alert('Remember by yourself, boomer.');
  }
  function login(event) {
    event.preventDefault();
    userLogin(email, password)
      .then(response => {
        if (response.ok) return response.json();
         else error = "Wrong creds u loser";
      })
      .then(async r => {
        let t = r.user;
        token.set(t);
        console.info(r);
        user.set(r.user);
      })
      .catch(err => error = "Wrong creds u loser");
  }
</script>

<style>
  .login-container {
    margin: 7vh auto;
    display: flex;
  }

  #login-form {
    margin: auto;
    padding: 35px;
    min-height: 550px;
    margin: 10vh auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: left;
    border-radius: 5px;
    flex: 1;
    min-width: 300px;
  }
  
  .fade-in {
    animation-name: fadeIn;
    animation-duration: 3s;
  }

  .fly-in {
    animation-name: flyIn;
    animation-duration: 3s;
  }

  #login-form input {
    border: solid grey 1px;
    padding: 5px;
    margin-bottom: 10px;
  }

</style>

<div class="content">
   <div class="login-container">
     <form id="login-form" class="fade-in" on:submit={login}>
      <h1> Food Destroying System! </h1>
      <input name="email" type="text" placeholder="Email" bind:value={email}> <br/>
      <input name="password" type="password" placeholder="Password" bind:value={password}> <br/>
      <input type="submit" value="Login">
      <a href="#" on:click={handleForgotPassword}> Forgot Password? </a>
      <p style="color: red;">{error}</p>
     </form>
    </div>
</div>
