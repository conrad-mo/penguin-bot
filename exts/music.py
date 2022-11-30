import interactions
from interactions import Channel
from interactions.ext.lavalink import VoiceClient, VoiceState, listener, Player
import lavalink

class Music(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @listener()
    async def on_track_start(self, event: lavalink.TrackStartEvent):
        """
        Fires when track starts
        """
        print("STARTED", event.track)

    @interactions.extension_listener()
    async def on_start(self):
        self.client.lavalink_client.add_node("127.0.0.1", 2333, "penguin-bot", "na")

    @interactions.extension_listener()
    async def on_voice_state_update(self, before: VoiceState, after: VoiceState):
        """
        Disconnect if bot is alone
        """
        if before and not after.joined:
            voice_states = self.client.get_channel_voice_states(before.channel_id)
            if len(voice_states) == 1 and voice_states[0].user_id == self.client.me.id:
                await self.client.disconnect(before.guild_id)

    @interactions.extension_command(name='play', description="Plays the audio of the first query on youtube given the search query")
    @interactions.option()
    async def play(self, ctx: interactions.CommandContext, query: str):
        await ctx.defer()

        # NOTE: ctx.author.voice can be None if you ran a bot after joining the voice channel
        voice: VoiceState = ctx.author.voice
        if not voice or not voice.joined:
            print(ctx.author.voice)
            return await ctx.send("You're not connected to the voice channel!")

        player: Player  # Typehint player variable to see their methods
        if (player := ctx.guild.player) is None:
            player = await voice.connect()

        tracks = await player.search_youtube(query)
        track = tracks[0]
        print(track)
        player.add(requester=int(ctx.author.id), track=track)

        if player.is_playing:
            return await ctx.send(f"Added to queue: `{track.title}`")
        await player.play()
        await ctx.send(f"Now playing: `{track.title}`")

    @interactions.extension_command(name='leave', description="Get's the bot to leave current voice channel")
    async def leave(self, ctx: interactions.CommandContext):
        await self.client.disconnect(ctx.guild_id)
        await ctx.send(f"Disconnected from vc")
    @interactions.extension_command(name='connect', description="Connects the bot to the provided voice channel")
    @interactions.option()
    async def connect(self, ctx:interactions.CommandContext, voice_channel: Channel):
        await ctx.send(f"Connected to {voice_channel}")
        await self.client.connect(int(ctx.guild_id), int(voice_channel.id))
    
def setup(client):
    Music(client)