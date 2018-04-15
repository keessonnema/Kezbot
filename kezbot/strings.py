YTMatchPattern = '(?:https?:\/\/)?(?:i\.|www\.|img\.)?(?:youtu\.be\/|youtube\.com\/|ytimg\.com\/)(?:embed\/|v\/|vi\/|' \
                 'vi_webp\/|watch\?v=|watch\?.+&v=)((\w|-){11})(?:\S+)?'
SPMatchPattern = '^(spotify:|https://[a-z]+\.spotify\.com/)'

YoutubePattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.' \
                  r'(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'
SpotifyPattern = r'(?:https?:\/\/(?:embed\.|open\.)(?:spotify\.com\/)(?:track\/|\?uri=spotify:track:)((\w|-){22}))'

strips = [' - ', '- ', ' -', ' – ']
split = ' - |- | -| – '

RemoveWords = ' ft| feat|lyrics|lyric|vs'
KeepWords = r'\b(remix|edit|rmx|rework)\b'
StringRegex = r'\[[^\]]*\]|\(\d+\)|“.*?”|[.]|[&]|[,]'

run_strings = (
    "Where do you think you're going?",
    "Huh? what? did he get away?",
    "ZZzzZZzz... Huh? what? oh, just him again, nevermind.",
    "Get back here!",
    "Not so fast...",
    "Look out for the wall!",
    "Don't leave me alone with them!!",
    "You run, you die.",
    "Run fatboy, run!",
    "Jokes on you, I'm everywhere",
    "You're gonna regret that...",
    "Go bother someone else, no-one here cares.",
    "I hear @MSFJarvis wants to hear more about you.",
    "If you let my daughter go now, that'll be the end of it. I will not look for you, I will not pursue you. \
    But if you don't, I will look for you, I will find you, and I will kill you.",
    "I drink your milkshake!",
    "Go ahead, make my day.",
    "Hasta la vista, baby.",
    "I'll get you, my pretty, and your little dog, too!",
    "You can't handle the truth!",
    "Frankly, my dear, I don't give a damn."
)
