<script>
  import { writable, get } from "svelte/store";
  import { onMount } from "svelte";
  import { userMessage, user } from "./../stores.js";
  import { Link, navigate } from "svelte-routing";
  import { NotificationDisplay, notifier } from "@beyonk/svelte-notifications";
  import { getSetMenus, getFoods, postFoodToSetitem, postSetitemToSetmenu} from "../api";
  import Select from "svelte-select";
  import axios from "axios";

  let setName = "",
    setTotalPrice = 0,
    setSize = 1,
    allFoods = [],
    allSetMenus = [],
    errorMsg = "",
    selectedSetMenuValues = undefined,
    selectedFoodValues= undefined,
    n,
    foods = [],
    setmenus = []

  onMount(() => {
    getFoods()
      .then(r => r.json())
      .then(response => {
        allFoods = response.result;
        allFoods.forEach(element => {
          console.log(element["id"].toString());
          length = foods.length;
          foods[length] = {
            value: element["id"],
            label: element["name"]
          };
        });
      });

    getSetMenus()
      .then(r => r.json())
      .then(response => {
        allSetMenus = response.result;
        allSetMenus.forEach(element => {
          console.log(element["id"].toString());
          length = setmenus.length;
          setmenus[length] = {
            value: element["id"],
            label: element["name"]
          };
        });
      });
  });

  function createSetItem(event) {
    //get location
    event.preventDefault();
    if (setName != "") {
      if (setTotalPrice > -1) {
        if (selectedFoodValues!= undefined) {
          if (setSize > 0) {
            axios
              .post(`${process.env.API_URL}api/setitem`, {
                name: setName,
                totalPrice: setTotalPrice,
                size: setSize,
              })
              .then(
                response => {
                  addFoodToSetitem(response.data["setitem_id"]);
                  addSetItemToSetMenu(response.data["setitem_id"])
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

  function addFoodToSetitem(setitem_id) {
    const food_ids = selectedFoodValues.map(objects => objects.value)
    var newAddition = {
      setitem_id: setitem_id,
      food_ids: food_ids
    };
    console.log(newAddition)

    postFoodToSetitem(newAddition).then(
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

  function addSetItemToSetMenu(setitem_id) {
    var newAddition = {
      setmenu_id:selectedSetMenuValues.value,
      setitem_id:setitem_id
    };

    postSetitemToSetmenu(newAddition).then(
      response => {
        console.log(response);
        navigate("/", { replace: true });
      },
      error => {
        console.log(error);
        errorMsg = "Error adding set item to set menu";
      }
    );
  }
  function handleFoodSelect(foods) {
    selectedFoodValues = foods.detail
  }
  function handleSetMenuSelect(setmenu) {
    selectedSetMenuValues = setmenu.detail
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
    <h2>Create Set Items</h2>
    Name:
    <br />
    <input
      name="food name"
      type="text"
      placeholder="Set Item Name"
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
      <Select items={foods} isMulti={true} on:select={handleFoodSelect}/>
    </div>
    <br />
    Set Menu:
    <br />
    <div class="Select">
      <Select items={setmenus} on:select={handleSetMenuSelect}/>
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
      on:click={createSetItem}>
      Submit
    </button>
  </div>
</div>
