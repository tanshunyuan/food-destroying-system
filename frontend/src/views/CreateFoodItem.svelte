<script>
  import { writable, get } from "svelte/store";
  import { onMount } from "svelte";
  import { userMessage, user } from "./../stores.js";
  import { Link, navigate } from "svelte-routing";
  import { NotificationDisplay, notifier } from "@beyonk/svelte-notifications";
  import { postFood } from "../api";

  let foodName = "",
    foodDescription = "",
    foodPrice = 0,
    foodUnit = 1,
    foodStatus = true,
    errorMsg = "",
    n;

  function createFood(event) {
    //get location
    event.preventDefault();
    if (foodName != "") {
      if (foodDescription != "") {
        if (foodPrice > -1) {
          if (foodUnit > 0) {
            let newFood = {name: foodName,
              status: foodStatus,
              price: foodPrice,
              description: foodDescription,
              unit: foodUnit
            }
            console.log(JSON.stringify(newFood))
            postFood(newFood)
              .then(
                response => {
                  console.log(response);
                  //navigate("/", { replace: true });
                },
                error => {
                  console.log(error);
                  errorMsg = "Error with creation";
                }
              );
          } else {
            errorMsg = "Unit cannot be 0 or negative";
          }
        } else {
          errorMsg = "Price cannot be negative";
        }
      } else {
        errorMsg = "Add a description";
      }
    } else {
      errorMsg = "Add a food name";
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
    <h2>Create Food Item</h2>
    Name:
    <br />
    <input
      name="food name"
      type="text"
      placeholder="Food Name"
      bind:value={foodName} />
    <br />
    Description:
    <input
      name="food description"
      type="text"
      placeholder="Description"
      bind:value={foodDescription} />
    <br />
    Price:
    <input name="food price" type="number" bind:value={foodPrice} />
    <br />
    Unit:
    <input name="units" type="number" bind:value={foodUnit} />
    <br />
    Status:
    <br />
    <label>
      Active
      <input type="radio" bind:group={foodStatus} value={true} />
    </label>
    <label>
      Inactive
      <input type="radio" bind:group={foodStatus} value={false} />
    </label>
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
