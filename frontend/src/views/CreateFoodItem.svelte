<script>
  import { writable, get } from "svelte/store";
  import { onMount } from "svelte";
  import { userMessage, user } from "./../stores.js";
  import { Link, navigate } from "svelte-routing";
  import { NotificationDisplay, notifier } from "@beyonk/svelte-notifications";
  import { postFood, getCategorys, postFoodToCategory } from "../api";
  import Select from "svelte-select";
  import axios from "axios";

  let foodName = "",
    foodDescription = "",
    foodPrice = 0,
    foodUnit = 1,
    foodStatus = true,
    allCategories = [],
    errorMsg = "",
    selectedValue = undefined,
    n,
    items = [];

  var Iterator = function(iteratorItems) {
    this.index = 0;
    this.iteratorItems = iteratorItems;
  };

  Iterator.prototype = {
    first: function() {
      this.reset();
      return this.next();
    },
    next: function() {
      return this.iteratorItems[this.index++];
    },
    hasNext: function() {
      return this.index <= this.iteratorItems.length;
    },
    reset: function() {
      this.index = 0;
    },
    each: function(callback) {
      for (var item = this.first(); this.hasNext(); item = this.next()) {
        callback(item);
      }
    }
  };
  function run() {
    var iter = new Iterator(allCategories);
    iter.each(function(item) {
      length = items.length;
      items[length] = {
        value: item["id"],
        label: item["name"]
      };
    });
  }
  onMount(() => {
    getCategorys()
      .then(r => r.json())
      .then(response => {
        allCategories = response.result;
        run()
        // allCategories.forEach(element => {
        //   console.log(element["id"].toString());
        //   length = items.length;
        //   items[length] = {
        //     value: element["id"],
        //     label: element["name"]
        //   };
        // });
      });
  });

  function createFood(event) {
    //get location
    event.preventDefault();
    if (foodName != "") {
      if (foodDescription != "") {
        if (foodPrice > -1) {
          if (selectedValue != undefined) {
            if (foodUnit > 0) {
              axios
                .post(`${process.env.API_URL}api/food`, {
                  name: foodName,
                  status: foodStatus,
                  price: foodPrice,
                  description: foodDescription,
                  unit: foodUnit
                })
                .then(
                  response => {
                    addCategory(response.data["food_id"]);
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

  function addCategory(foodid) {
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
    Category:
    <br />
    <div class="Select">
      <Select {items} bind:selectedValue />
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
      on:click={createFood}>
      Submit
    </button>
  </div>
</div>
