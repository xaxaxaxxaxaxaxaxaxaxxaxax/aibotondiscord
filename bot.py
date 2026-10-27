import discord
from discord.ext import commands
from openai import OpenAI

# ВСТАВЛЯЕМ ТВОИ ТОКЕНЫ НАПРЯМУЮ В КОД
DISCORD_TOKEN = "MTU2NDQ2OTE1Mjk3MjgwNDE0Nw.GGWaaB.ZPbV_tUR-cn0jcN9pxMxakzm73p1ugeW4_dWrc"
TEAMO_API_KEY = "sk-teamo-31f5995635016d7816e9c92014ba7721ed3d791f6111920e"

# Настраиваем бесплатный ИИ DeepSeek напрямую
ai_client = OpenAI(
    api_key=TEAMO_API_KEY,
    base_url="https://teamorouter.cn"
)
DEEPSEEK_MODEL = "deepseek-chat"

# Настройка доступов Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"=========================================")
    print(f"{bot.user} успешно запущен!")
    print(f"Заходи в Discord и общайся с ним через @")
    print(f"=========================================")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        user_prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
        
        if not user_prompt:
            await message.reply("Привет! Задавай свой вопрос, я слушаю.")
            return

        async with message.channel.typing():
            try:
                response = ai_client.chat.completions.create(
                    model=DEEPSEEK_MODEL,
                    messages=[
                        {"role": "system", "content": "Ты полезный ИИ-ассистент в Discord. Отвечаешь на русском и не только языке, если человек пишет на другом языке, ответь на нем."},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=800
                )
                ai_text = response.choices.message.content
                if len(ai_text) > 2000:
                    ai_text = ai_text[:1990] + "..."
                await message.reply(ai_text)
            except Exception as e:
                print(f"Ошибка ИИ: {e}")
                await message.reply("Извини, бесплатный сервер сейчас занят. Попробуй еще раз через минуту!")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
