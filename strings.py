MatchPattern = '([a-z]+?:\/\/)*([a-z]*?[.])*youtu([.]be|be[.][a-z]+?)\/((watch[?]v=|v)*).+'
YoutubePattern = r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.' \
                  r'(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})'
RemoveWords = "\\b(official|videoclip|clip|video|mix|ft|feat|music|HQ|version|HD|original|extended|" \
              "unextended|vs|meets|anthem|12\"|rmx|lyrics|international|1080p)\\b"