This is the dir watcher project; this program takes any given directory as an arguement 
and searches for magic words within the files. Upon program start-up it searches for a 
specified directory, if that directory is not found; it continues to look after logging
an error. If the directory is found it will filter through files to look for .text files.
After that this program then iterates through those text files and searches for magic words.
This process is endless until the user ends the search.