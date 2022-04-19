import os, asyncio
from pydub import AudioSegment
count=0
message="\"[:nh]I'm gonna eat a pizza. [:dial386-317-4777] Hi, can i order a pizza? [:nv]no! [:nh]why? [:nv] cuz you are john madden![:np] [:phone on][jhah<800,13>nmae<800,15>deh<800,17>n][_<800,17>][jhah<800,17>nmae<800,18>deh<800,20>n][jhah<400,20>ah<800,25>ah<400,24>ah<400,25>ah<800,20>ah<400,18>ah<800,17>nmae<800,15>deh<800,13>n] ... Wow this is a really capable TTS![dah<600,20>][dah<600,20>][dah<600,20>][dah<500,16>][dah<130,23>][dah<600,20>][dah<500,16>][dah<130,23>][dah<600,20>][dah<600,27>][dah<600,27>][dah<600,27>][dah<500,28>][dah<130,23>][dah<600,19>][dah<500,16>][dah<130,23>][dah<600,20>] ... Uh, oh it's the communists![say<400,23>lxao<800,28>niy<600,23>duh<200,25>shiy<800,27>mih<400,20>][zh][reh<400,20>][s][pah<800,25>][blxiy<600,23>][k][s][vao<200,21>][bao<800,23>][d][nih<400,16>][jh][splow<400,16>][tiy<800,18>][laa<400,18>][naa<400,20>][veh<800,21>][kiy<400,18>][meh<400,23>][liy<800,25>][kay<400,27>][yxaa<400,28>][rao<800,30>][s][_<400,23>][daa<400,23>][z][draa<800,32>][v][styu<600,30>][eh<200,28>][t][saa<800,30>][z][dae<400,27>][nih<400,23>][jh][vow<800,28>][lxeh<400,27>][zh][naa<400,25>][row<800,27>][daa<400,20>][v][eh<400,20>][diy<800,25>][nih<400,23>][jh][mow<400,21>][guw<800,23>][chih<400,16>][jh][sow<400,16>][veh<800,28>][t][skiy<600,27>][say<200,25>][aa<1600,23>][z]\""
os.system("audio\\say.exe -w"+count+".wav "+message+"&")
vc= await client.join_voice_channel(voice_channel)
player = vc.create_ffmpeg_player("audio\\"+count+'.wav', after=lambda: print('done playing ',count,'.wav'))
player.start()
while not player.is_done():
    await asyncio.sleep(1)
# disconnect after the player has finished
player.stop()
await vc.disconnect()
print "Deleting original wav..."
os.remove("audio\\"+count+".wav")