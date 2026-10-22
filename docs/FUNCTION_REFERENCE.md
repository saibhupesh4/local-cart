# Function reference

This reference covers the business logic identified in the repository; routine admin registrations and migrations are omitted. Signatures are summarized in readable form.

## Project and catalog

* `greatkart.views.home(request)` — loads available products ordered by creation time and renders `home.html`. It loops through products to set `reviews`, leaving only the last product's reviews in context; the template behavior should be verified and this is a candidate bug fix. No writes or explicit validation.
* `Category.get_url()` — reverses `products_by_category` using its slug. `menu_links(request)` context processor returns all categories for the shared navigation.
* `store.views.store(request, category_slug=None)` — optional category lookup, filters available products, paginates (currently 1/category or 3/all per page), and returns the store template with page and count. Invalid category yields 404.
* `Product.get_url()` — reverses detail route from category and product slugs. `averageReview()` and `countReview()` aggregate approved reviews; return numeric zero when empty. These methods each run an aggregate query.
* `store.views.product_detail(request, category_slug, product_slug)` — loads a product, tests whether it is in the current cart, checks whether the authenticated user has ordered it, and fetches approved reviews and gallery. The broad catch simply re-raises and adds no error handling; product lookup should use `get_object_or_404`.
* `store.views.search(request)` — searches product name/description using `icontains`, returns available matches newest first and a count. Empty input now safely returns available products (all); the UI's required field normally prevents empty submission.
* `submit_review(request, product_id)` — on POST updates the current user's existing review or validates `ReviewForm` and creates one with product/user/IP. Redirect target comes from the referrer. It should be protected with `login_required`, validate product existence, and avoid trusting arbitrary referrer targets.
* `ReviewForm` exposes subject, review and rating; the model form handles field-level validation but no custom range validation is present.

## Accounts

* `MyAccountManager.create_user(...)` — requires email and username, normalizes email, sets the supplied phone number (empty by default), hashes the password, and saves to the manager database. This phone field fix allows registration to save the account. `create_superuser(...)` adds staff/admin flags. The manager does not explicitly validate password strength or enforce all superuser flags.
* `Account.full_name`, `has_perm`, `has_module_perms` — display helper and admin permission hooks. `has_module_perms` always returns true; object permission policy is simplistic.
* `RegistrationForm.clean()` compares password/confirmation; it now returns `cleaned_data`, a required form contract. `UserForm` and `UserProfileForm` bind editable profile fields and assign CSS classes.
* `register(request)` — validates form, creates user/profile, sends activation email, redirects to login with a verification query. Local default email backend prints messages. Errors remain in form context.
* `login(request)` — authenticates email/password and attempts to merge anonymous cart lines, then logs in, reports success and redirects based on referrer query. Broad exceptions silently suppress cart merge errors; redirect parsing is fragile and should be replaced with Django's safe `next` handling.
* `logout(request)` — logs out and redirects; currently GET route and login required.
* `activate(request, uidb64, token)` — decodes user id, validates Django token, activates account or reports an invalid link.
* `dashboard(request)` — loads completed order count and profile for current account. Missing profile currently raises; registration normally creates one.
* `forgotPassword`, `resetpassword_validate`, `resetPassword` — send signed-token email, validate token into session, and update the password. Reset password should apply Django password validators and handle absent/expired session UID safely.
* `my_orders`, `edit_profile`, `change_password`, `order_detail` — signed-in account operations. Order detail now resolves only completed orders belonging to `request.user`, then totals order lines. Password change checks current password and matching values, but does not call password validators.

## Cart and orders

* `_cart_id(request)` — ensures a session key exists and returns it; session creation is a side effect.
* `add_cart(request, product_id)` — loads product, resolves submitted option values, then increments an identical line or creates a new one for account/session. Existing code swallows all variation lookup errors, prints debug output in anonymous flow, accepts non-POST requests and has duplicated branches. These are known refactor targets.
* `remove_cart` decrements or deletes a scoped line; `remove_cart_item` deletes it. Both redirect to cart. The former silently swallows all errors. Both currently mutate on GET.
* `cart` and `checkout` compute subtotal, 2% tax and grand total from database prices and quantity. Checkout requires login. Both repeat arithmetic and catch only `ObjectDoesNotExist`.
* `OrderForm` exposes billing fields as a model form. `place_order` rejects empty carts, computes totals server-side, saves billing/order data, builds a date+id order number, and renders the demo payment page. It does not create order lines until payment handling.
* `payments(request)` requires login and POST, parses the pending order number, verifies ownership and stock, then creates server-generated demo metadata and order lines, adjusts stock and clears the cart within a database transaction. It does not process or verify payment. Receipt email is sent after commit and can fail separately.
* `Order.full_name`, `full_address` format billing data. `order_complete` requires login and matches the signed-in user's order and associated demo ID before totaling lines; invalid details redirect home.

## Framework entry points

`manage.py` loads Django management; `greatkart.wsgi.application` and `greatkart.asgi.application` expose server entry points. Cart `counter` context processor counts active lines. Email templates build activation/reset/order messages. Side effects and failure cases above are derived from the current code; documented limitations should be revisited when implementation changes.
