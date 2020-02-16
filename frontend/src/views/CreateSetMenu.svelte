<script>
  import { writable, get } from "svelte/store";
  import { onMount } from "svelte";
  import { userMessage, user } from "./../stores.js";
  import { Link, navigate } from "svelte-routing";
  import { NotificationDisplay, notifier } from "@beyonk/svelte-notifications";
  import { getSetItems, postSetitemToSetmenu, postSetMenu} from "../api";
  import Select from "svelte-select";
  import axios from "axios";

  let setName = "",
    allSetItems= [],
    errorMsg = "",
    selectedValue = undefined,
    n,
    items = [];

  onMount(() => {
    getSetItems()
      .then(r => r.json())
      .then(response => {
        allSetItems= response;
        allSetItems.forEach(element => {
          console.log(element["id"].toString());
          length = items.length;
          items[length] = {
            value: element["id"],
            label: element["name"]
          };
        });
      });
  });

  function createSetMenu(event) {
    event.preventDefault();
    if (setName != "") {
            let newSetmenu = {
             "name": setName
            };
            postSetMenu(newSetmenu).then(
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
      errorMsg = "Add a Setmenu name";
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
    <h2>Create Set Menu</h2>
    Name:
    <br />
    <input
      name="food name"
      type="text"
      placeholder="Set Name"
      bind:value={setName} />
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
      on:click={createSetMenu}>
      Submit
    </button>
  </div>
</div>
