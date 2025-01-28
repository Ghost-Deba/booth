import discord
from discord import app_commands
import requests

# تعريف البوت
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# استبدال القيم في الـ API بالاسم الجديد
def transform_data(data, item_name):
    # نبحث عن العنصر المحدد (item_name) من البيانات
    transformed_data = []

    for item in data:
        # تأكد من أن العنصر الذي تم جلبه يتوافق مع اسم العنصر
        if item.get('id') == item_name:
            name = item.get('id', 'Unknown Name')
            class_name = item.get('category', 'Unknown Class')
            value = item.get('value', 0)

            transformed_data.append({
                "Item": name,
                "MaxPrice": value,
                "Class": class_name
            })

    return transformed_data

# جلب البيانات من الـ API
def fetch_data_from_api():
    api_url = 'https://biggamesapi.io/api/rap'  # حط رابط الـ API هنا
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()  # بيانات الـ JSON من الـ API
    else:
        return []

# تنسيق الرسالة المطلوبة
def generate_message(transformed_data):
    message = '''script_key="UR KEY HERE";
--Settings For Booths Sniper
_G.ZapHubBoothsSniperSettings = {
MinimumGems = 0,
Items = {'''
    
    for item in transformed_data:
        message += f'\n{{Item = "{item["Item"]}", MaxPrice = {item["MaxPrice"]}, Class = "{item["Class"]}"}},'

    message += '''
},
Extras = {
AnyItem = {Enabled = false, PercentageProfit = "10", MaxPrice = 500000000},
TitanicPet = {Enabled = false, PercentageProfit = "25", MaxPrice = 500000000},
HugePet = {Enabled = false, PercentageProfit = "0", MaxPrice = 28000000},
},
ServerHop = {
Enabled = true, -- true / false
},
Webhook = {
Enabled = true, -- true / false
WebhookURL = "UR WEBHOOK HERE",
},
}

loadstring(game:HttpGet('https://zaphub.xyz/ExecBoothSniper'))()
'''
    return message

# إضافة Slash Command للبوت
@tree.command(name="get", description="جلب بيانات عنصر معين من الـ API")
@app_commands.describe(item="اسم العنصر الذي ترغب في جلب بياناته")  # إضافة وصف للـ parameter
async def get_data(interaction: discord.Interaction, item: str):
    await interaction.response.defer()  # تأجيل الرد لإعطاء الوقت لتنفيذ الكود
    data = fetch_data_from_api()  # جلب البيانات من الـ API
    transformed_data = transform_data(data, item)  # تحويل البيانات بناءً على اسم العنصر
    if transformed_data:
        final_message = generate_message(transformed_data)  # توليد الرسالة
        await interaction.followup.send(final_message)  # إرسال الرسالة إلى القناة
    else:
        await interaction.followup.send(f"لم يتم العثور على بيانات للعنصر '{item}'.")

# عند تشغيل البوت
@client.event
async def on_ready():
    # نشر Slash Commands
    await tree.sync()
    print(f'We have logged in as {client.user}')

# استبدل 'YOUR_BOT_TOKEN' بالتوكن الخاص بك
client.run('MTMwNzQwMzE1ODk1MTE2NjAxNA.GHm8fI.CneTEpfDSGzsXt44WDumZHaKhAs2HOspyrCz0M')
