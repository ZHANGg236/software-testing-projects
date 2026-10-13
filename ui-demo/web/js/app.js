const PRODUCTS = [
  {
    sku: "KB-001",
    name: "轻风机械键盘",
    category: "键盘",
    price: 299,
    description: "紧凑配列，适合办公和日常码字。",
    image: "assets/products/keyboard.svg"
  },
  {
    sku: "HP-002",
    name: "云听降噪耳机",
    category: "耳机",
    price: 499,
    description: "柔和配色，支持长时间舒适佩戴。",
    image: "assets/products/headphones.svg"
  },
  {
    sku: "MS-003",
    name: "星轨无线鼠标",
    category: "鼠标",
    price: 159,
    description: "轻量化设计，适合移动办公。",
    image: "assets/products/mouse.svg"
  }
];

const ACCOUNT = {
  username: "student",
  password: "123456"
};

const state = {
  cart: readCart(),
  keyword: "",
  category: "全部",
  user: localStorage.getItem("demoUser") || ""
};

const elements = {
  loginButton: document.querySelector("#login-button"),
  userArea: document.querySelector("#user-area"),
  userName: document.querySelector("#user-name"),
  logoutButton: document.querySelector("#logout-button"),
  loginModal: document.querySelector("#login-modal"),
  closeLoginButton: document.querySelector("#close-login-button"),
  loginForm: document.querySelector("#login-form"),
  usernameInput: document.querySelector("#username"),
  passwordInput: document.querySelector("#password"),
  loginError: document.querySelector("#login-error"),
  searchInput: document.querySelector("#search-input"),
  categorySelect: document.querySelector("#category-select"),
  productGrid: document.querySelector("#product-grid"),
  emptyResult: document.querySelector("#empty-result"),
  cartButton: document.querySelector("#cart-button"),
  cartCount: document.querySelector("#cart-count"),
  cartDrawer: document.querySelector("#cart-drawer"),
  cartBackdrop: document.querySelector("#cart-backdrop"),
  closeCartButton: document.querySelector("#close-cart-button"),
  cartItems: document.querySelector("#cart-items"),
  cartTotal: document.querySelector("#cart-total"),
  checkoutButton: document.querySelector("#checkout-button"),
  orderSuccess: document.querySelector("#order-success"),
  orderNo: document.querySelector("#order-no")
};

function readCart() {
  try {
    return JSON.parse(localStorage.getItem("demoCart")) || [];
  } catch {
    return [];
  }
}

function saveCart() {
  localStorage.setItem("demoCart", JSON.stringify(state.cart));
}

function formatMoney(value) {
  return Number(value).toFixed(2);
}

function cartItemCount() {
  return state.cart.reduce((sum, item) => sum + item.quantity, 0);
}

function cartTotal() {
  return state.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function filteredProducts() {
  return PRODUCTS.filter((product) => {
    const matchesKeyword = product.name.toLowerCase().includes(state.keyword.toLowerCase());
    const matchesCategory = state.category === "全部" || product.category === state.category;
    return matchesKeyword && matchesCategory;
  });
}

function renderProducts() {
  const products = filteredProducts();
  elements.productGrid.innerHTML = products.map((product) => `
    <article class="product-card" data-testid="product-card" data-sku="${product.sku}">
      <img class="product-image" src="${product.image}" alt="${product.name}">
      <div class="product-content">
        <div class="product-meta">
          <h2 class="product-name" data-testid="product-name">${product.name}</h2>
          <span class="product-category">${product.category}</span>
        </div>
        <p class="product-description">${product.description}</p>
        <div class="product-bottom">
          <span class="product-price" data-testid="product-price">¥${formatMoney(product.price)}</span>
          <button
            class="button button-primary"
            data-testid="add-to-cart-${product.sku}"
            data-sku="${product.sku}"
            type="button"
          >
            加入购物车
          </button>
        </div>
      </div>
    </article>
  `).join("");

  elements.emptyResult.hidden = products.length > 0;
}

function renderLoginState() {
  const loggedIn = Boolean(state.user);
  elements.loginButton.hidden = loggedIn;
  elements.userArea.hidden = !loggedIn;
  elements.userName.textContent = loggedIn ? state.user : "";
}

function renderCart() {
  elements.cartCount.textContent = cartItemCount();
  elements.cartTotal.textContent = formatMoney(cartTotal());

  if (state.cart.length === 0) {
    elements.cartItems.innerHTML = '<p class="cart-empty" data-testid="cart-empty">购物车还是空的</p>';
    return;
  }

  elements.cartItems.innerHTML = state.cart.map((item, index) => `
    <div class="cart-item" data-testid="cart-item" data-sku="${item.sku}">
      <span class="cart-item-name">${item.name}</span>
      <span class="cart-item-price">¥${formatMoney(item.price * item.quantity)}</span>
      <span class="cart-item-detail">
        单价 ¥${formatMoney(item.price)} × ${item.quantity}
        <button
          class="link-button remove-cart-item"
          data-index="${index}"
          data-testid="remove-${item.sku}"
          type="button"
        >
          移除
        </button>
      </span>
    </div>
  `).join("");
}

function addToCart(sku) {
  const product = PRODUCTS.find((item) => item.sku === sku);
  if (!product) {
    return;
  }

  const existing = state.cart.find((item) => item.sku === sku);
  if (existing) {
    existing.quantity += 1;
  } else {
    state.cart.push({
      sku: product.sku,
      name: product.name,
      price: product.price,
      quantity: 1
    });
  }

  saveCart();
  renderCart();
}

function openCart() {
  elements.orderSuccess.hidden = true;
  elements.cartDrawer.hidden = false;
  elements.cartBackdrop.hidden = false;
}

function closeCart() {
  elements.cartDrawer.hidden = true;
  elements.cartBackdrop.hidden = true;
}

function openLogin() {
  elements.loginError.hidden = true;
  elements.loginError.textContent = "";
  elements.loginForm.reset();
  elements.loginModal.hidden = false;
  elements.usernameInput.focus();
}

function closeLogin() {
  elements.loginModal.hidden = true;
}

elements.loginButton.addEventListener("click", openLogin);
elements.closeLoginButton.addEventListener("click", closeLogin);
elements.loginModal.addEventListener("click", (event) => {
  if (event.target === elements.loginModal) {
    closeLogin();
  }
});

elements.loginForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const username = elements.usernameInput.value.trim();
  const password = elements.passwordInput.value;

  if (username === ACCOUNT.username && password === ACCOUNT.password) {
    state.user = username;
    localStorage.setItem("demoUser", username);
    closeLogin();
    renderLoginState();
    return;
  }

  elements.loginError.textContent = "用户名或密码错误";
  elements.loginError.hidden = false;
});

elements.logoutButton.addEventListener("click", () => {
  state.user = "";
  localStorage.removeItem("demoUser");
  renderLoginState();
});

elements.searchInput.addEventListener("input", (event) => {
  state.keyword = event.target.value.trim();
  renderProducts();
});

elements.categorySelect.addEventListener("change", (event) => {
  state.category = event.target.value;
  renderProducts();
});

elements.productGrid.addEventListener("click", (event) => {
  const button = event.target.closest("[data-sku]");
  if (button) {
    addToCart(button.dataset.sku);
  }
});

elements.cartItems.addEventListener("click", (event) => {
  const button = event.target.closest(".remove-cart-item");
  if (!button) {
    return;
  }
  state.cart.splice(Number(button.dataset.index), 1);
  saveCart();
  renderCart();
});

elements.cartButton.addEventListener("click", openCart);
elements.closeCartButton.addEventListener("click", closeCart);
elements.cartBackdrop.addEventListener("click", closeCart);

elements.checkoutButton.addEventListener("click", () => {
  if (state.cart.length === 0) {
    return;
  }

  const orderNo = `ORD${Date.now()}`;
  state.cart = [];
  saveCart();
  renderCart();
  elements.orderNo.textContent = orderNo;
  elements.orderSuccess.hidden = false;
});

renderProducts();
renderLoginState();
renderCart();
