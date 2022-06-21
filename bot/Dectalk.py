import os, asyncio
import discord
VCID=962463272861331466
msg=r"[:nh]I'm gonna eat a pizza. [:dial386-317-4777] Hi, can i order a pizza? [:nv]no! [:nh]why? [:nv] cuz you are john madden![:np] [:phone on][jhah<800,13>nmae<800,15>deh<800,17>n][_<800,17>][jhah<800,17>nmae<800,18>deh<800,20>n][jhah<400,20>ah<800,25>ah<400,24>ah<400,25>ah<800,20>ah<400,18>ah<800,17>nmae<800,15>deh<800,13>n] ... Wow this is a really capable TTS![dah<600,20>][dah<600,20>][dah<600,20>][dah<500,16>][dah<130,23>][dah<600,20>][dah<500,16>][dah<130,23>][dah<600,20>][dah<600,27>][dah<600,27>][dah<600,27>][dah<500,28>][dah<130,23>][dah<600,19>][dah<500,16>][dah<130,23>][dah<600,20>] ... Uh, oh it's the communists![say<400,23>lxao<800,28>niy<600,23>duh<200,25>shiy<800,27>mih<400,20>][zh][reh<400,20>][s][pah<800,25>][blxiy<600,23>][k][s][vao<200,21>][bao<800,23>][d][nih<400,16>][jh][splow<400,16>][tiy<800,18>][laa<400,18>][naa<400,20>][veh<800,21>][kiy<400,18>][meh<400,23>][liy<800,25>][kay<400,27>][yxaa<400,28>][rao<800,30>][s][_<400,23>][daa<400,23>][z][draa<800,32>][v][styu<600,30>][eh<200,28>][t][saa<800,30>][z][dae<400,27>][nih<400,23>][jh][vow<800,28>][lxeh<400,27>][zh][naa<400,25>][row<800,27>][daa<400,20>][v][eh<400,20>][diy<800,25>][nih<400,23>][jh][mow<400,21>][guw<800,23>][chih<400,16>][jh][sow<400,16>][veh<800,28>][t][skiy<600,27>][say<200,25>][aa<1600,23>][z]"
def count(): # A function which counts up from zero
    i=0
    yield i
    while True:
        i+=1
        yield i
counter=count()
async def dectalk(client,message,guilds):
    try: # Make it speak
        count=str(counter.__next__())
        try:
            guilds.voice_client.cleanup()
        except:
            pass
        audiopath=os.path.dirname(os.path.realpath(__file__))+'\\audio'
        os.chdir(audiopath)
        print(message.content.lower().split('/dectalk',maxsplit=1))
        if len(message.content.lower().split('/dectalk',maxsplit=1))>=1 and '/dectalk ' in message.content.lower():
            process = await asyncio.create_subprocess_shell("say.exe -w "+count+'.wav "'+message.content.lower().split('/dectalk ',maxsplit=1)[-1]+'"', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,cwd=audiopath)
        else:
            process = await asyncio.create_subprocess_shell("say.exe -w "+count+'.wav "'+msg+'"', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,cwd=audiopath)
        vc = await guilds.get_channel(VCID).connect()
        await asyncio.sleep(1)
        stdout, stderr = await process.communicate()
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')
        else:
            vc.play(discord.FFmpegPCMAudio(count+'.wav',executable="ffmpeg.exe"))
            await asyncio.sleep(3)
            while vc.is_playing():
                await asyncio.sleep(1)
            # disconnect after the player has finished
            await asyncio.sleep(1)
            vc.stop()
            print(f"done playing {count}.wav")
        await vc.disconnect()
        vc.cleanup() # Cleanup
        try: #Delete the old file
            print ("Deleting original wav...")
            await asyncio.sleep(5)
            os.remove(audiopath+'\\'+count+".wav")
        except OSError as e:
            print(f"An exception occured while deleting {count}.wav:\n{e}")
            print(os.listdir())
    except Exception as e:
        print(f"An exception occured while creating/deleting DECTalk:\n{e}")
