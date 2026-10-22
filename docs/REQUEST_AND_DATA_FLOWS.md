# Request and data flows

## Catalog and search

Browser requests `/` or `/store/` → root/app URL resolver → home/catalog view → ORM queries `Product` and related `Category`/`ReviewRating` → shared template renders HTML with navigation context. Category pages add a category slug filter and pagination; product detail adds reviews, gallery, cart state and purchase-history state. Search reads `keyword` from GET and filters available products by name/description.

## Registration and authentication

Registration POST binds `RegistrationForm`; valid input creates an inactive `Account` with hashed password and a `UserProfile`, then sends an activation link using Django's token generator. Link activation decodes the user key and validates the token before setting active. Login authenticates email/password, attempts to transfer anonymous session cart items, establishes Django authentication session and redirects. The local console email backend prints mail content for development. Password reset follows a signed token then stores a user id in session before accepting a new password.

## Cart and checkout

Anonymous cart requests establish a session key and `Cart`; signed-in lines attach to `Account`. Add requests match variation choices and create/increment `CartItem`. Cart context reports a count; cart and checkout calculate subtotal as price × quantity and tax as 2%. Checkout requires login, then order placement snapshots billing fields and server-calculated totals into an uncompleted `Order`. The local demo button POSTs only the pending order number. Server code verifies ownership and stock, creates a clearly labeled demo record, saves order lines, decrements stock and clears the cart atomically. No real payment is collected. Confirmation requires the signed-in owner and associated demo ID.

## Known failure paths

Missing category/product pages produce 404 through object lookup where used. Empty search now returns an empty-safe result set. Invalid forms re-render with validation errors. Invalid activation/reset token redirects with an error message. Invalid order/payment IDs in the completion view redirect home. Several cart/account/payment views still have broad catches, missing validation or unhandled lookups; see `ERROR_HANDLING_AND_SECURITY.md` before treating this as robust.
