from modules import settings
import main


@bot.command(usage="orders [page]", description="Show all orders", help=f"Get a list of all orders.")
async def orders(ctx, page: int = 1):
    orders = requests.get(f"{settings.base_url()}/orders?page={page}",
                          headers=settings.shoppy_api_key()).json()
    message_output = f"*{bot.command_prefix}orders [page]* | Change orders page\n*{bot.command_prefix}order <order_id>* | Manage order\n\n"
    for order in orders:
        order_id = order["id"]
        order_email = order["email"]
        order_product = order["product"]["title"]
        message_output += f"**{bot.command_prefix}order {order_id}**\n"
    message = await ctx.send(embed=discord.Embed(description=message_output, color=settings.hex_color()).set_footer(icon_url=settings.footer_icon_url(), text=f"{settings.footer()} | Page {page}").set_thumbnail(url=settings.thumbnail_image()).set_author(name="All orders", url=f"https://shoppy.gg/orders?page={page}"))
    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")

    def check(reaction, user):
        return reaction.message.id == message.id and user == ctx.author
    global paginator
    paginator = True
    while paginator:
        reaction, _ = await bot.wait_for('reaction_add', check=check)
        if reaction.emoji == "➡️":
            await message.remove_reaction(reaction.emoji, ctx.author)
            page += 1
            orders = requests.get(f"{settings.base_url()}/orders?page={page}",
                                  headers=settings.shoppy_api_key()).json()
            message_output = f"*{bot.command_prefix}orders [page]* | Change orders page\n*{bot.command_prefix}order <order_id>* | Manage order\n\n"
            for order in orders:
                order_id = order["id"]
                order_email = order["email"]
                order_product = order["product"]["title"]
                message_output += f"**{bot.command_prefix}order {order_id}**\n"
            await message.edit(embed=discord.Embed(description=message_output, color=settings.hex_color()).set_footer(icon_url=settings.footer_icon_url(), text=f"{settings.footer()} | Page {page}").set_thumbnail(url=settings.thumbnail_image()).set_author(name="All orders", url=f"https://shoppy.gg/orders?page={page}"))
        elif reaction.emoji == "⬅️":
            await message.remove_reaction(reaction.emoji, ctx.author)
            if page > 1:
                page -= 1
                orders = requests.get(f"{settings.base_url()}/orders?page={page}",
                                      headers=settings.shoppy_api_key()).json()
                message_output = f"*{bot.command_prefix}orders [page]* | Change orders page\n*{bot.command_prefix}order <order_id>* | Manage order\n\n"
                for order in orders:
                    order_id = order["id"]
                    order_email = order["email"]
                    order_product = order["product"]["title"]
                    message_output += f"**{bot.command_prefix}order {order_id}**\n"
                await message.edit(embed=discord.Embed(description=message_output, color=settings.hex_color()).set_footer(icon_url=settings.footer_icon_url(), text=f"{settings.footer()} | Page {page}").set_thumbnail(url=settings.thumbnail_image()).set_author(name="All orders", url=f"https://shoppy.gg/orders?page={page}"))
        else:
            pass


@bot.command(usage="order <order_id>", description="Show specific order", help="Get more information about a specific order")
async def order(ctx, order_id):
    order_data = requests.get(
        f"{settings.base_url()}/orders/{order_id}", headers=settings.shoppy_api_key()).json()
    product_id = order_data["product_id"]
    price = order_data["price"]
    currency = order_data["currency"]
    email = order_data["email"]
    quantity = order_data["quantity"]
    paid_at = order_data["paid_at"]
    if paid_at is None:
        paid_at = "Not paid"
    else:
        paid_at = datetime.strptime(
            paid_at, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d, %H:%M:%S")
    created_at = order_data["created_at"]
    created_at = datetime.strptime(
        created_at, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d, %H:%M:%S")
    delivered = ""
    for acc in order_data["accounts"]:
        delivered += f'{acc["account"]} '
    if delivered is None or delivered == " " or delivered == "":
        delivered = "Not paid"
    product_title = order_data["product"]["title"]
    product_img = order_data["product"]["image"]["url"]
    gateway = order_data["gateway"]
    crypto_address = order_data["crypto_address"]
    crypto_amount = order_data["crypto_amount"]
    ip_address = order_data["agent"]["geo"]["ip"]
    iso_code = order_data["agent"]["geo"]["iso_code"]
    country = order_data["agent"]["geo"]["country"]
    city = order_data["agent"]["geo"]["city"]
    continent = order_data["agent"]["geo"]["continent"]
    return await ctx.send(embed=discord.Embed(description=f"PRODUCT INFO\nProduct title: **{product_title}**\nProduct ID: **{product_id}**\nPrice: **{price} {currency}**\nGateway: **{gateway}**\nAddress: **{crypto_address}**\nAmount: **{crypto_amount}**\nDelivered: **{delivered}**\nQuantity: **{quantity}**\nCreated at: **{created_at}**\nPaid at: **{paid_at}**\n\nUSER INFO\nEmail: **{email}**\nIP: **{ip_address}**\nContinent: **{continent}**\nCountry: **{country}**\nISO code: **{iso_code}**\nCity: **{city}**", color=settings.hex_color()).set_footer(icon_url=settings.footer_icon_url(), text=settings.footer()).set_thumbnail(url=product_img).set_author(name=order_id, url=f"https://shoppy.gg/orders/{order_id}"))
