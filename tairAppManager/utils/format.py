# -*- coding: utf-8 -*-

def cutline(line, count_per_line):
  lines = []
  n = 0
  while n < len(line):
    lines.append(line[n:n+count_per_line]) 
    n = n + count_per_line
  return '\n'.join(lines)

def removeComment(para):
  newlines = []
  lines = para.split('\n')
  for line in lines:
    if not line.strip().startswith('#'):
      newlines.append(line.strip()) 
  return '\n'.join(newlines)
