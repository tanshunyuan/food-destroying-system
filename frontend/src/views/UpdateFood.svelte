<script>
  import { writable, get } from "svelte/store";
  import { onMount } from "svelte";
  import { userMessage, user, selectedFood } from "./../stores.js";
  import { Link, navigate } from "svelte-routing";
  import { NotificationDisplay, notifier } from "@beyonk/svelte-notifications";
  import { postFood, getCategorys, postFoodToCategory } from "../api";
  import Select from "svelte-select";
  import axios from "axios";

  let foodName = get(selectedFood).name,
    foodDescription = get(selectedFood).description,
    foodPrice = get(selectedFood).price,
    foodUnit = get(selectedFood).unit,
    foodStatus = get(selectedFood).status,
    allCategories = [],
    errorMsg = "",
    selectedValue = undefined,
    n,
    items = [];

  onMount(() => {
    getCategorys()
      .then(r => r.json())
      .then(response => {
        allCategories = response.result;
        allCategories.forEach(element => {
          length = items.length;
          items[length] = {
            value: element["id"],
            label: element["name"]
          };
          if(get(selectedFood).category == element["id"]){
              selectedValue ={value: element["id"], label: element["name"]}
          }
        });
      });
  });

  function updateFood(event) {
    event.preventDefault();
    if (foodName != "") {
      if (foodDescription != "") {
        if (foodPrice > -1) {
          if (selectedValue != undefined) {
            if (foodUnit > 0) {
              axios
                .put(`${process.env.API_URL}api/food`, {
                  id: get(selectedFood).id,
                  name: foodName,
                  status: foodStatus,
                  price: foodPrice,
                  description: foodDescription,
                  unit: foodUnit
                })
                .then(
                  response => {
                    navigate("menu", { replace: true });
                  },
                  error => {
                    console.log(error);
                    errorMsg = "Food with the same name already exist";
                  }
                );
            } else {
              errorMsg = "Unit cannot be 0 or negative";
            }
          } else {
            errorMsg = "Add a category";
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
    <h2>Update Food Item</h2>
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
    Category:
    <br />
    <div class="Select">
      <Select {items} bind:selectedValue isDisabled/>
    </div>
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
      on:click={updateFood}>
      Submit
    </button>
  </div>
</div>
