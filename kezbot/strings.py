yt_match_pattern = '([a-z]+?:\/\/)*([a-z]*?[.])*youtu([.]be|be[.][a-z]+?)\/((watch[?]v=|v)*).+'
sp_match_pattern = '^(spotify:|https://[a-z]+\.spotify\.com/)'

youtube_pattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.' \
                  r'(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'
spotify_pattern = r'(?:https?:\/\/(?:embed\.|open\.)(?:spotify\.com\/)(?:track\/|\?uri=spotify:track:)((\w|-){22}))'

strips = [' - ', '- ', ' -', ' – ']
split = ' - |- | -| – '

remove_words = ' ft| feat|lyrics|lyric|vs'
keep_words = r'\b(remix|edit|rmx|rework)\b'
string_regex = r'\[[^\]]*\]|\(\d+\)|“.*?”|[.]|[&]|[,]'

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
    "I drink your beer!",
    "Go ahead, make my day.",
    "Hasta la vista, baby.",
    "I'll get you, my pretty, and your little dog, too!",
    "You can't handle the truth!",
    "Frankly, my dear, I don't give a damn.",
    "Ahoy hoy!",
    "He who laughs last, didn't get it.",
    "We live in an age where pizza gets to your home before you, so run faster!",
    "I’d like to help you out. Which way did you come in?",
    "The more people I meet, the more I like to see them run.",
    "Change is good, so get out."
)
