var itemList = [];

$(function() {
    // Call Python code to sort when clicked
    $('#sort-by-price').on('click', function(e) {
        e.preventDefault()
        $.ajax({
            url:"/sortbyprice",
            type:"POST",
            dataType: 'json',
            success: function(response){
                // Sorted list is returned from the Python code
                console.log(response);
                document.getElementById("display-items").innerHTML = "";
                // Loop through sorted list to display items
                response['data'].forEach(function(item) {
                    document.getElementById("display-items").innerHTML += 
                    `
                        <div class="card mb-3" style="max-width:100%;">
                            <div class="row no-gutters">
                                <div class="col-md-4">
                                    <img src="${item.image}" class="card-img-top img-responsive" alt="${item.name}">
                                </div>
                                <div class="col-md-8">
                                    <div class="card-body">
                                        <h5 class="card-title">${item.name}</h5>
                                        <p>${item.price}</p>
                                        <button id="${item.id}" class="add-button"> Add </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                });

                const buttonList = document.querySelectorAll('.add-button');

                buttonList.forEach((button) => {
                        button.addEventListener('click', () => {
                            document.getElementById("cart").hidden = false;
                            
                            let itemId = parseInt(button.getAttribute("id"));
                            let itemPrice = parseFloat(allItems[itemId - 1]['price']);
                            let itemName = allItems[itemId - 1]['name'];

                            let itemInTable = itemList.find(x => x.id === itemId);

                            if (itemInTable == undefined) {
                                // Add item to cart
                                var item_t = {"id": itemId, "name": itemName, "quantity": 1, "price": itemPrice};
                                itemList.push(item_t);
                                addNewItem(item_t);
                            } else {
                                // Update quantity, price, and total price if item is already in cart (adding the same item multiple times)
                                itemInTable.quantity += 1;
                                itemInTable.price = +itemPrice * +itemInTable.quantity;
                                updateItem(itemInTable);

                            }
                            console.log(itemList);
                        });
                    });
                },
                error: function(error) {
                    console.log("error");
                }
            });
        return false;
    });
});


function addNewItem(item) {
    const newItem = document.createElement("tr");
    newItem.setAttribute("id", "table_id" + item.id);
    newItem.innerHTML = `
        <td scope='row'> <img src="${allItems[item.id - 1]['image']}" style="width: auto; height: 5em;" alt="${item.name}"> </td>
        <td class="name" scope='row'>${item.name}</td>
        <td class="quantity" scope='row'>${item.quantity}</td>
        <td class="price" scope='row'>${item.price}</td>
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
        document.getElementById("cart").hidden = true;
    }
}

