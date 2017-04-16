import subprocess
class VLC(object):
   def play(self, stop=1, movie=""):
      if stop == 1:
        subprocess.Popen(["cvlc", movie, '--play-and-exit', '--fullscreen', '--stop-time','300'], shell=False)
      else:
        print "shhh"
