from Telegram import Update, ReplyKeyboardMarkup
from Telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Define states for the conversation
VIEW_MENU, PLACE_ORDER, ORDER_SUMMARY, CANCEL_ORDER, CHECK_STATUS = range(5)

class FastFoodBot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.menu = {
            "Burger": 5.00,
            "Fries": 2.50,
            "Soda": 1.50,
            "Pizza": 7.00,
            "Salad": 4.00
        }
        self.orders = {}

        # Add command handlers
        self.add_handlers()

    # Add all handlers
    def add_handlers(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                VIEW_MENU: [CommandHandler('view_menu', self.view_menu)],
                PLACE_ORDER: [MessageHandler(Filters.text & ~Filters.command, self.place_order)],
                ORDER_SUMMARY: [CommandHandler('order_summary', self.order_summary)],
                CANCEL_ORDER: [CommandHandler('cancel_order', self.cancel_order)],
                CHECK_STATUS: [CommandHandler('check_status', self.check_status)],
            },
            fallbacks=[CommandHandler('exit', self.exit_bot)],
        )

        self.dispatcher.add_handler(conv_handler)

    # Start the bot
    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Welcome to the Fast Food Bot!\n\n"
            "You can type the following commands:\n"
            "/view_menu - See the menu\n"
            "/place_order - Place an order\n"
            "/order_summary - See your order summary\n"
            "/cancel_order - Cancel your order\n"
            "/check_status - Check the status of your order\n"
            "/exit - Exit the bot"
        )
        return VIEW_MENU

    # View the menu
    def view_menu(self, update: Update, context: CallbackContext):
        menu_str = "\n--- Menu ---\n"
        for item, price in self.menu.items():
            menu_str += f"{item}: ${price}\n"
        menu_str += "-------------------\n"
        update.message.reply_text(menu_str)
        return VIEW_MENU

    # Place an order
    def place_order(self, update: Update, context: CallbackContext):
        item = update.message.text.capitalize()
        if item in self.menu:
            quantity = 1  # Default to 1 for simplicity
            if item in self.orders:
                self.orders[item] += quantity
            else:
                self.orders[item] = quantity
            update.message.reply_text(f"Added {item} to your order. Type another item or type 'done' to finish.")
            return PLACE_ORDER
        elif item.lower() == "done":
            return self.order_summary(update, context)
        else:
            update.message.reply_text("Sorry, that item is not on the menu. Try again.")
            return PLACE_ORDER

    # Show the order summary
    def order_summary(self, update: Update, context: CallbackContext):
        if not self.orders:
            update.message.reply_text("You haven't placed any order yet!")
        else:
            summary = "\n--- Your Order ---\n"
            total_price = 0
            for item, quantity in self.orders.items():
                summary += f"{item} x{quantity} - ${self.menu[item] * quantity}\n"
                total_price += self.menu[item] * quantity
            summary += f"Total Price: ${total_price}\n"
            summary += "--------------------"
            update.message.reply_text(summary)
        return ConversationHandler.END

    # Cancel the order
    def cancel_order(self, update: Update, context: CallbackContext):
        if not self.orders:
            update.message.reply_text("You don't have an order to cancel!")
        else:
            self.orders.clear()
            update.message.reply_text("Your order has been canceled.")
        return ConversationHandler.END

    # Check order status
    def check_status(self, update: Update, context: CallbackContext):
        if not self.orders:
            update.message.reply_text("You haven't placed an order yet!")
        else:
            update.message.reply_text("Your order is being processed.")
        return CHECK_STATUS

    # Exit the bot
    def exit_bot(self, update: Update, context: CallbackContext):
        update.message.reply_text("Thank you for using the Fast Food Bot! Goodbye.")
        return ConversationHandler.END

    # Start the bot
    def run(self):
        self.updater.start_polling()
        self.updater.idle()

if __name__ == "__main__":
    TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot's token
    bot = FastFoodBot(TOKEN)
    bot.run()
