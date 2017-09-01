MatchPattern = '([a-z]+?:\/\/)*([a-z]*?[.])*youtu([.]be|be[.][a-z]+?)\/((watch[?]v=|v)*).+'
YoutubePattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.' \
                  r'(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'

strips = [' - ', '- ', ' -', ': ', ' : ', ' :', ' – ']
split = ' - |- | -|: | : | :| – '

RemoveWords = ' ft| feat|lyrics|lyric'
KeepWords = r'\b(remix|edit|rmx)\b'
StringRegex = r'\[[^\]]*\]|\(\d+\)|“.*?”|".*?"|[.]|[&]|[,]'

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
    "You could also try /kickme, I hear thats fun.",
    "Go bother someone else, no-one here cares.",
    "I hear @MSFJarvis wants to hear more about you."
)
