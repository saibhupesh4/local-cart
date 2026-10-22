# URL routing reference

Root routes in `greatkart/urls.py` mount admin honeypot at `/admin/`, actual Django admin at `/securelogin/`, home at `/`, and app routes under `/store/`, `/cart/`, `/accounts/`, `/orders/`. All routes use `path()` and app URL files; there are no namespaces. Templates generally reverse names with `{% url %}`.

| Method | URL pattern | Config → view | Result / access | Purpose |
|---|---|---|---|---|
| GET | `/` | root → `greatkart.views.home` | `home.html`, public | Featured products |
| GET | `/store/` | store → `store.store` | store template, public | Catalog |
| GET | `/store/category/<slug>/` | store → `store.store` | store template, public | Category products |
| GET | `/store/category/<slug>/<slug>/` | store → `store.product_detail` | product detail, public | Product and reviews |
| GET | `/store/search/` | store → `store.search` | store template, public | Search query `keyword` |
| POST | `/store/submit_review/<int>/` | store → `store.submit_review` | redirect, authentication expected by use | Create/update review |
| GET/POST | `/accounts/register/`, `/accounts/login/` | accounts → `register`, `login` | account templates | Registration/authentication |
| GET | `/accounts/logout/` | accounts → `logout` | redirect; login required | End session |
| GET | `/accounts/activate/<uid>/<token>/` | accounts → `activate` | redirect | Email activation |
| GET/POST | `/accounts/forgotPassword/`, `/accounts/resetPassword/` | accounts views | templates/redirect | Password reset |
| GET | `/accounts/resetpassword_validate/<uid>/<token>/` | accounts → `resetpassword_validate` | redirect | Validate reset token |
| GET | `/accounts/dashboard/`, `/accounts/` | accounts → `dashboard` | dashboard, login required | Account home |
| GET/POST | `/accounts/my_orders/`, `/accounts/edit_profile/`, `/accounts/change_password/` | accounts views | account templates, login required | User account management |
| GET | `/accounts/order_detail/<int>/` | accounts → `order_detail` | detail template, login required and owner-scoped | Order details |
| GET | `/cart/` | carts → `cart` | cart template, public/session scoped | View cart |
| GET/POST | `/cart/add_cart/<int>/` | carts → `add_cart` | redirect | Add/increment line |
| GET | `/cart/remove_cart/<int>/<int>/`, `/cart/remove_cart_item/<int>/<int>/` | carts views | redirect | Decrement/remove line |
| GET | `/cart/checkout/` | carts → `checkout` | checkout template, login required | Checkout preview |
| POST | `/orders/place_order/` | orders → `place_order` | payment template, login required | Create pending order |
| POST | `/orders/payments/` | orders → `payments` | JSON, login required | Complete local demo order; no payment |
| GET | `/orders/order_complete/` | orders → `order_complete` | completion template or redirect, login required | Order receipt |
| any | `/securelogin/` | Django admin | admin | Administrative site |

Methods listed are those observed in views/templates, not enforced route declarations: several mutation routes currently accept GET and need conversion to POST/CSRF-protected forms. `include()` strips the app prefix before matching. Dynamic slug and integer converters populate view arguments. Root project config serves uploaded media in development. No custom 404/500 handlers were found. For a new endpoint, trace root prefix → app pattern and name → view arguments → rendered template/redirect; use named reversal rather than hard-coded paths.
