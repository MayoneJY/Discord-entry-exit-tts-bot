import discord
import asyncio
from gtts import gTTS
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
channel = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
  

@client.event
async def on_voice_state_update(member, before, after):
    if member.bot == True:
        return
    if before.channel is None and after.channel is not None:
        # 이미 봇이 들어갔는지 확인
        if not after.channel.guild.voice_client:
            await after.channel.connect()
        else:
            # 봇이 있는 채널과 같을 경우에만
            if after.channel.guild.voice_client.channel != after.channel:
                return
            
            nickname = member.nick if member.nick != None else member.name
            # 파일이 없을 경우
            if not os.path.isfile("./name/{}_join.mp3".format(nickname)):
                tts = gTTS(text="{}님이 접속했습니다.".format(nickname), lang='ko')  # 영어 음성 변환
                tts.save("./name/{}_join.mp3".format(nickname))  # mp3로 저장
                
            voice_client = after.channel.guild.voice_client

            if voice_client is not None:
                await asyncio.sleep(1)
                voice_client.stop()
                voice_client.play(discord.FFmpegPCMAudio("./name/{}_join.mp3".format(nickname)))
            
    elif before.channel is not None and after.channel is None:
        voice_channel = before.channel
        
        if not voice_channel.guild.voice_client:
            await voice_channel.connect()
        else:
            # 봇이 있는 채널과 같을 경우에만
            if before.channel.guild.voice_client.channel != before.channel:
                return
            
            if len(voice_channel.members) <= 1:  # 멤버가 봇 뿐인지 확인
                # 봇이 채널에 연결되어 있다면
                if voice_channel.guild.voice_client:
                    await voice_channel.guild.voice_client.disconnect()  # 채널에서 퇴장
                    return
            nickname = member.nick if member.nick != None else member.name
            
            # 파일이 없을 경우
            if not os.path.isfile("./name/{}_leave.mp3".format(nickname)):
                tts = gTTS(text="{}님이 퇴장했습니다.".format(nickname), lang='ko')
                tts.save("./name/{}_leave.mp3".format(nickname))
            
            voice_client = voice_channel.guild.voice_client
            
            if voice_client is not None:
                voice_client.stop()
                voice_client.play(discord.FFmpegPCMAudio("./name/{}_leave.mp3".format(nickname)))
            

client.run('token')
