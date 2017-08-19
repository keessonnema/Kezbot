MatchPattern = '([a-z]+?:\/\/)*([a-z]*?[.])*youtu([.]be|be[.][a-z]+?)\/((watch[?]v=|v)*).+'
YoutubePattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.' \
                  r'(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'
RemoveWords = "\\b(ft|feat|HQ|HD|4k|lyrics|lyric|1080p)\\b"
KeepWords = ["remix", "edit"]
StringRegex = r'\[[^\]]*\]|\(\d+\)|“.*?”|".*?"|[.]|[&]|[,]|(#[A-Za-z0-9]+)'
