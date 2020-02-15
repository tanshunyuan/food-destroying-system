<script>
  import { writable, get } from "svelte/store";
  import { onMount } from "svelte";
  import { userMessage, user } from "./../stores.js";
  import { Link, navigate } from "svelte-routing";
  import { NotificationDisplay, notifier } from "@beyonk/svelte-notifications";
  import { getFoods } from "../api";
  import Select from "svelte-select";
  import axios from "axios";

  let setName = "",
    setTotalPrice = 0,
    setSize = 1,
    allFoods = [],
    errorMsg = "",
    selectedValue = undefined,
    n,
    items = [];

  onMount(() => {
    getFoods()
      .then(r => r.json())
      .then(response => {
        allFoods = response.result;
        allFoods.forEach(element => {
          console.log(element["id"].toString());
          length = items.length;
          items[length] = {
            value: element["id"],
            label: element["name"]
          };
        });
      });
  });

  function createFood(event) {
    //get location
    event.preventDefault();
    if (setName != "") {
      if (setTotalPrice > -1) {
        if (selectedValue != undefined) {
          if (setSize > 0) {
            axios
              .post(`${process.env.API_URL}api/setmenu`, {
                name: setName,
                totalPrice: setTotalPrice,
                size: setSize,
              })
              .then(
                response => {
                  addFoodItems(response.data["setitem_id"]);
                  //navigate("/", { replace: true });
                },
                error => {
                  console.log(error);
                  errorMsg = "set menu with the same name already exist";
                }
              );
          } else {
            errorMsg = "Size cannot be 0 or negative";
          }
        } else {
          errorMsg = "Set has to contain food";
        }
      } else {
        errorMsg = "Price cannot be negative";
      }
    } else {
      errorMsg = "Add a food name";
    }
  }

  function addFoodItems(setid) {
    var newAddition = {
      food_id: foodid,
      category_id: selectedValue.value
    };

    postFoodToCategory(newAddition).then(
      response => {
        console.log(response);
        navigate("/", { replace: true });
      },
      error => {
        console.log(error);
        errorMsg = "Error adding food to category";
      }
    );
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
    Price:
    <input name="food price" type="number" bind:value={setTotalPrice} />
    <br />
    Size:
    <input name="sizes" type="number" bind:value={setSize} />
    <br />
    Food:
    <br />
    <div class="Select">
      <Select {items} isMulti={true} bind:selectedValue />
    </div>
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
      on:click={createFood}>
      Submit
    </button>
  </div>
</div>
