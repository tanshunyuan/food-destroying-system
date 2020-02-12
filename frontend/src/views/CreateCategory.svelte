<script>
  import { writable, get } from "svelte/store";
  import { onMount } from "svelte";
  import Select from "svelte-select";
  import { userMessage, user } from "./../stores.js";
  import { Link, navigate } from "svelte-routing";
  import { NotificationDisplay, notifier } from "@beyonk/svelte-notifications";
  import { postCategory } from "../api";

  let categoryName = "",
    errorMsg = "";


  function createCategory(event) {
    event.preventDefault();
    if (categoryName != "") {
            let newCategory = {
             "name": categoryName
            };
            postCategory(newCategory).then(
              response => {
                console.log(response);
                navigate("/", { replace: true });
              },
              error => {
                console.log(error);
                errorMsg = "Error with creation";
              }
            );
    } else {
      errorMsg = "Add a Category name";
    }
  }
</script>

<style>
  input {
    border: solid lightgray 1px;
    padding: 5px;
    margin-bottom: 10px;
    width: 98%;
    height: 32px;
    border-radius: 3px;
  }

  .radio {
    width: 5%;
  }

  .formButton {
    width: 100px;
    height: 32px;
  }
  .form {
    width: 30%;
    left: 35%;
    position: absolute;
  }

  .Select {
    color: black;
  }
</style>

<div class="content">
  <div class="form">
    <h2>Create Category</h2>
    Name:
    <br />
    <input
      name="category name"
      type="text"
      placeholder="Category Name"
      bind:value={categoryName} />
    <br />
    <p style="color: red;">{errorMsg}</p>
    <br />
    <Link to="/">
      <button class="formButton">Back</button>
    </Link>
    <button
      class="formButton"
      type="submit"
      value="Submit"
      on:click={createCategory}>
      Submit
    </button>
  </div>
</div>