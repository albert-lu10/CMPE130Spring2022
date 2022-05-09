var itemList = [];

var sort_map = ["quicksort", "mergesort", "insertionsort", "heapsort", "radixsort", "hybridsort"]
var sort_by_type_map = ["name", "price"]

function generate_product_card(data, index)
{
    // Create the card of a product (display feature)
    return `
        <div class="col-md-4">
            <div class="card h-100">
                <img class="card-img-top" style="height: 10rem; object-fit: contain;" src="${data[index]['image']}" alt="Card image cap">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${data[index]['name']}</h5>
                    <div class="card-text mt-auto">
                        <h3>$${data[index]['price']}</h3>
                        <button id="${data[index]['id']}" class="add-button"> Add </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

var current_select = 'Default (1x)';

function clearResults() {
    // Clear the results box
    var dataset_loaded_element = document.getElementById('dataset_loaded');
    dataset_loaded_element.innerHTML = "";

    var e_time_element = document.getElementById('e_time');
    e_time_element.innerHTML = "";

}

var loaded_dataset = false;

function reload() {

    // Select type of sort
    var dataset_type_element = document.getElementById('dataset_type');
    var dataset_type = dataset_type_element.options[dataset_type_element.selectedIndex].value;

    clearResults();

    // Call Python code in the backend
    $.ajax({
        url: "/reload?by=" + dataset_type,
        type: "POST",
        dataType: 'json',
        success: function(response){
            // Sorted list is returned from the Python code
            console.log(response);

            var dataset_loaded_element = document.getElementById('dataset_loaded');
            dataset_loaded_element.innerHTML = "Dataset: " + dataset_type + "x with: " + response['data'].length + " elements";
            
            document.getElementById('results_data').style.display = "block";

            allItems = response['data']
            console.log(allItems)

            loaded_dataset = true;

            $('#pagination-container').pagination({
                dataSource: response['data'],
                pageSize: 9,
                callback: function(data, pagination) {
                    // template method of yourself
                    html = ''
                    for(var i = 0; i < data.length; i = i + 3)
                    {
                        console.log(data);
                        html += `<div class = "row mt-3">`
                        html += generate_product_card(data, i);
                        if(i + 1 < data.length) {
                            console.log(data[i + 1]['image'])
                            html += generate_product_card(data, i + 1);
                        }
                        if(i + 2 < data.length) {
                            console.log(data[i + 2]['image'])
                            html += generate_product_card(data, i + 2);
                        }
                        html += `</div>`;
                    }
                    $('#data-container').html(html);
                    addButtonHandlers();
                }
            });
        },
        error: function(error) {
            console.log("Error!");
        }
    });
}

function sort_data() {

    if(!loaded_dataset)
    {
        alert("Load dataset first!");
        return;
    }

    // Select type of sort
    var sort_types_options = document.getElementById('sort-types');
    var sort_type = sort_types_options.options[sort_types_options.selectedIndex].value;
    console.log(sort_type)

    // Select what to sort by
    var sort_by_options = document.getElementById('sort-by');
    var sort_by = sort_by_options.options[sort_by_options.selectedIndex].value;
    console.log(sort_by)

    // Call Python code in the backend
    $.ajax({
        url: "/sort?type=" + sort_map[sort_type] + "&by=" + sort_by_type_map[sort_by],
        type: "POST",
        dataType: 'json',
        success: function(response){
            // Sorted list is returned from the Python code
            console.log(response);
            
            var e_time_element = document.getElementById('e_time');
            e_time_element.innerHTML = sort_map[sort_type].charAt(0).toUpperCase() + sort_map[sort_type].slice(1)  + " by " + sort_by_type_map[sort_by] + ": " + (response['time'] / 1000000.0) + " ms (" + response['time'] + " ns)";
            
            $('#pagination-container').pagination({
                dataSource: response['data'],
                pageSize: 9,
                callback: function(data, pagination) {
                    // template method of yourself
                    html = ''
                    for(var i = 0; i < data.length; i = i + 3)
                    {
                        console.log(data);
                        html += `<div class = "row mt-3">`
                        html += generate_product_card(data, i);
                        if(i + 1 < data.length) {
                            console.log(data[i + 1]['image'])
                            html += generate_product_card(data, i + 1);
                        }
                        if(i + 2 < data.length) {
                            console.log(data[i + 2]['image'])
                            html += generate_product_card(data, i + 2);
                        }
                        html += `</div>`;
                    }
                    $('#data-container').html(html);
                    addButtonHandlers();
                }
            });
            

            },
            error: function(error) {
                console.log("Error!");
            }
        });
    return false;
}

function addButtonHandlers() {
    const buttonList = document.querySelectorAll('.add-button');

    buttonList.forEach((button) => {
        button.addEventListener('click', () => {
            document.getElementById("cart").hidden = false;
            
            let itemId = parseInt(button.getAttribute("id"));
            let index = allItems.findIndex(x => x.id === itemId);
            let itemPrice = parseFloat(allItems[index]['price']);
            let itemName = allItems[index]['name'];
            let itemImage = allItems[index]['image'];

            let itemInTable = itemList.find(x => x.id === itemId);

            if (itemInTable == undefined) {
                // Add item to cart
                var item_t = {"id": itemId, "name": itemName, "quantity": 1, "price": itemPrice, "image": itemImage};
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
}

// Checkout Functions
function addNewItem(item) {
    const newItem = document.createElement("tr");
    newItem.setAttribute("id", "table_id" + item.id);
    newItem.innerHTML = `
        <td scope='row'> <img src="${item.image}" style="width: auto; height: 5em;" alt="${item.name}"> </td>
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
    sessionStorage.setItem("cart", JSON.stringify(itemList));
}

function placeorder()
{
    alert ('Your order has been placed successfully!!!')
    form.submit();
    
}
