@Bot.on_message(filters.command("total1") & filters.user(ADMINS))
async def total_users_channel1(client, message):
    db1 = JoinReqs1()
    total = await db1.get_all_users_count()
    await message.reply(f"Total Users in Channel 1: {total}")

@Bot.on_message(filters.command("total2") & filters.user(ADMINS))
async def total_users_channel2(client, message):
    db2 = JoinReqs2()
    total = await db2.get_all_users_count()
    await message.reply(f"Total Users in Channel 2: {total}")

@Bot.on_message(filters.command("total3") & filters.user(ADMINS))
async def total_users_channel3(client, message):
    db3 = JoinReqs3()
    total = await db3.get_all_users_count()
    await message.reply(f"Total Users in Channel 3: {total}")

@Bot.on_message(filters.command("total4") & filters.user(ADMINS))
async def total_users_channel4(client, message):
    db4 = JoinReqs4()
    total = await db4.get_all_users_count()
    await message.reply(f"Total Users in Channel 4: {total}")


@Bot.on_message(filters.command("clear1") & filters.user(ADMINS))
async def clear_users_channel1(client, message):
    db1 = JoinReqs1()
    await db1.delete_all_users()
    await message.reply("Cleared all users in Channel 1.")

@Bot.on_message(filters.command("clear2") & filters.user(ADMINS))
async def clear_users_channel2(client, message):
    db2 = JoinReqs2()
    await db2.delete_all_users()
    await message.reply("Cleared all users in Channel 2.")

@Bot.on_message(filters.command("clear3") & filters.user(ADMINS))
async def clear_users_channel2(client, message):
    db3 = JoinReqs3()
    await db3.delete_all_users()
    await message.reply("Cleared all users in Channel 3.")

@Bot.on_message(filters.command("clear4") & filters.user(ADMINS))
async def clear_users_channel4(client, message):
    db4 = JoinReqs4()
    await db4.delete_all_users()
    await message.reply("Cleared all users in Channel 4.")