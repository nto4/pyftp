#! /usr/bin/python

import ftplib
import sys
import re
from getpass import getpass


class pyftp(ftplib.FTP):
  def __init__(self,  srv):
    try:
      ftplib.FTP.__init__(self, srv)
    except Exception as e:
      print e
      sys.exit()


  def auth(self,  user, passwd):
    '''Login'''
    try:
      self.login(user, passwd)
    except Exception:
      print "Bad login"
      sys.exit()


  def mkdir(self, name):
    '''Creates new directory'''
    try:
      print "Creating {0}{1}".format(ftp.pwd(), name)
      self.mkd(name)
    except Exception as e:
      print(e)


  def rmdir(self, name):
    '''Removes directory'''
    return self.rmd(name)


  def cd(self, name):
    '''Changes directory'''
    try:
      ftp.cwd(name)
    except Exception as e:
      print e


  def rm(self, param, start_path = ''):
    '''Removes a file

    Flags: -R [-r] deletes folder and everything inside
    '''
    index = max(map((lambda x: param.rfind(x)), ['-R', '-r']))
    path = reduce((lambda x, y: x.replace(y, '')), [param, '-R', '-r', ' '])
    if index == -1:
      self.delete(path)
    else:
      if path[-1] != '/':
        path += '/'
      path = path.replace('./', '')
      self.delAll(path)


  def delAll(self, path):
    '''Removes all files in `path` directory'''
    print 'Removing ' + self.pwd() + '/' + path
    map(self.delete, map(lambda x: path + x, self.getFilesByType(path)))
    for directory in self.getFilesByType(path, 'd'):
      self.delAll(path + directory + '/')
      self.rmdir(path + directory)


  def getFilesByType(self, path = './', type = '-'):
    '''Retrieves all files in `path` directory'''
    filenames = []

    def isFile(line):
      if line[0] == type:
        filenames.append(line)
        
    def extractFilename(line):
      return line.split()[8]

    self.retrlines('LIST ' + path, isFile)
    return map(extractFilename, filenames)
    

  def ls(self, name= ''):
    '''Lists directory'''
    print (self.retrlines('LIST ' + name ))


  def getDir(self, path = ''):
    '''Retrieves array of filenames from path'''
    print self.nlst(path)

if __name__ == "__main__":
  if (len(sys.argv) > 1):
    srv  = sys.argv[1]
  else:
    srv = raw_input("Server: ")

  if (len(sys.argv) > 2):
    user = sys.argv[2]
  else:
    user = raw_input("Username: ")

  passwd = getpass("Password: ")
  ftp = pyftp(srv)
  ftp.auth(user, passwd)

  print(ftp.getwelcome())

  while (1):
    cmd = raw_input("> ").split(' ', 1)
    if (cmd[0] == "quit" or cmd[0] == "exit"):
      break;

    try:
      getattr(ftp, cmd[0])(cmd[1])
    except IndexError:
      getattr(ftp, cmd[0])()
    except Exception as e:
      print(e)

  try:
    ftp.quit()
  except Exception as e:
    print(e)
