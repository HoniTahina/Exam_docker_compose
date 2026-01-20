const API_URL = "http://localhost:5000/api/items";

async function loadItems() {
  const res = await fetch(API_URL);
  const items = await res.json();

  const list = document.getElementById("items");
  list.innerHTML = "";

  items.forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `
      <input type="text" value="${item.name}" id="item-${item.id}">
      <button onclick="updateItem(${item.id})">Modifier</button>
      <button onclick="deleteItem(${item.id})">Supprimer</button>
    `;
    list.appendChild(li);
  });
}

async function addItem() {
  const name = document.getElementById("name").value;
  if (!name) return;

  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  });

  document.getElementById("name").value = "";
  loadItems();
}

async function updateItem(id) {
  const name = document.getElementById(`item-${id}`).value;

  await fetch(`${API_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name })
  });

  loadItems();
}

async function deleteItem(id) {
  await fetch(`${API_URL}/${id}`, {
    method: "DELETE"
  });

  loadItems();
}

loadItems();
