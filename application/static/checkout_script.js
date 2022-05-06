var itemList;

$(function() {
    itemList = JSON.parse(sessionStorage.getItem("cart"));
    console.log(itemList);
    for(var i = 0; i < itemList.length; i++) {
        console.log(itemList[i]);
        addNewItem(itemList[i]);
    }
});

// Checkout Functions
function addNewItem(item) {
    const newItem = document.createElement("tr");
    newItem.setAttribute("id", "table_id" + item.id);
    newItem.innerHTML = `
        <td scope='row'> <img src="${item.image}" style="width: auto; height: 5em;" alt="${item.name}"> </td>
        <td class="name" scope='row'>${item.name}</td>
        <td class="quantity" scope='row'>${item.quantity}</td>
        <td class="price" scope='row'>${item.price.toFixed(2)}</td>
        <td scope='row'> <button class="delete-button"> Delete </button> </td>
    `;
    document.querySelector("#cart table tbody").append(newItem);

    let removeButton = newItem.querySelector("button");
    removeButton.addEventListener('click', () => {
        let index = itemList.indexOf(item);
        itemList.splice(index, 1);
        removeButton.parentElement.parentElement.remove();
        updateTotalPrice();
    }, false);
    updateTotalPrice();
};

function updateItem(item) {
    const currentItem = document.getElementById("table_id" + item.id);
    console.log(currentItem);
    currentItem.querySelector(".quantity").innerText = item.quantity.toString();
    currentItem.querySelector(".price").innerText = (item.price.toFixed(2)).toString();
    updateTotalPrice();
}

function updateTotalPrice() {
    let price = 0;
    for (let i = 0; i < itemList.length; i++) {
        price += itemList[i].price;
    }
    document.getElementById("price").innerHTML = `Total: $${price.toFixed(2)}`;
    if (itemList.length == 0) {
        alert("Cart removed!");
        window.location.replace("/");
    }
    sessionStorage.setItem("cart", JSON.stringify(itemList));
}

