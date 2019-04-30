import asyncio
import json

channels_to_MQ=None
async def my_background_task(client):
    global channels_to_MQ
    await client.wait_until_ready()
    
    channel_to_send = client.get_channel(568791671764942868) # channel ID goes here
    msg = await channel_to_send.send('starting...')
    #msg = await channel_to_send.fetch_message(572039983196536851)
    while True:
        categories={}
        channels_dict={}
        
        channels=client.get_all_channels()
        for channel in sorted(channels,key=lambda x:x.position):
            categories.setdefault(str(channel.category),[]).append(channel.name)
        for indx,i in enumerate(categories['None']):
            channels_dict['string_'+str(indx)]=('\t'.join(map(str,categories[i])).title())

        channels_to_MQ=json.dumps(channels_dict)
        await msg.edit(content ='\n\n**     Структура сервера проекта MLP для ознакомления**\n\n'+'\n\n'.join('%s\n     %s' %(i,j) for i,j in zip(categories['None'],(v for k,v in channels_dict.items()))))

        await asyncio.sleep(10) # task runs every 60 seconds
        yield channels_dict