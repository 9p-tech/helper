"""All WhatsApp reply template strings in one place."""

GREETING = (
    "👋 Hi! Welcome to *Snitch* support.\n\n"
    "Reply *REPLACE* to raise a replacement request.\n"
    "Reply *STATUS <order_id>* to check your order status."
)

ASK_ORDER_ID = (
    "Got it! Let's start your replacement request. 🛍️\n\n"
    "Please reply with your *Order ID*.\n"
    "Example: SN260509ABCD\n\n"
    "_(You'll find it in your order confirmation email.)_"
)

ORDER_NOT_FOUND = (
    "❌ Order *{order_id}* not found.\n\n"
    "Please double-check and send the correct Order ID."
)

PHONE_MISMATCH = (
    "❌ This order is not linked to your WhatsApp number.\n\n"
    "Please make sure you're messaging from the same number "
    "you used at checkout."
)

WINDOW_CLOSED = (
    "⏰ Sorry, the *{days}-day replacement window* for order "
    "*{order_id}* has already closed.\n\n"
    "Contact support@snitch.in for further help."
)

CLAIM_EXISTS = (
    "⚠️ A replacement request already exists for order *{order_id}*.\n\n"
    "Your Claim ID: *{claim_id}*\n"
    "Status: *{status}*"
)

ORDER_VERIFIED = (
    "✅ Order *{order_id}* verified!\n\n"
    "Please send a *clear photo of the damaged item*. 📸\n"
    "Make sure the damage is clearly visible."
)

NEED_DAMAGE_PHOTO = (
    "📸 Please send a *photo* of the damaged item.\n"
    "Text alone isn't enough — we need to see the damage."
)

DAMAGE_PHOTO_RECEIVED = (
    "📸 Damage photo received!\n\n"
    "Now please send a photo of the *invoice or packing slip* "
    "that came in the package. 📄"
)

NEED_INVOICE = (
    "📄 Please send a *photo of the invoice or packing slip* "
    "from inside the package.\n"
    "We need this to verify your order."
)

PROCESSING = "⏳ Processing your claim, please wait a moment..."

APPROVED = (
    "✅ *Replacement Approved!*\n\n"
    "Your replacement has been initiated. Our team will be in "
    "touch within 24 hours.\n\n"
    "🎫 Claim ID: *{claim_id}*\n\n"
    "Thank you for shopping with Snitch! 🙌"
)

REJECTED = (
    "❌ *Replacement Request Rejected*\n\n"
    "Reason: {reason}\n\n"
    "If you believe this is a mistake, email us at "
    "*support@snitch.in* with Claim ID: *{claim_id}*"
)

MANUAL_REVIEW = (
    "🔍 Your claim is under *manual review*.\n\n"
    "Our team will contact you within *24 hours*.\n\n"
    "🎫 Claim ID: *{claim_id}*\n\n"
    "Thank you for your patience!"
)

STATUS_FOUND = (
    "📦 Order *{order_id}*\n"
    "Status: *{status}*\n"
    "Items: {item_count}\n"
    "Total: ₹{total}"
)

STATUS_NOT_FOUND = (
    "❌ Order *{order_id}* not found.\n"
    "Please check the ID and try again."
)

ERROR_NO_ACTIVE_CLAIM = (
    "Something went wrong with your session. 😕\n\n"
    "Please type *REPLACE* to start again."
)
