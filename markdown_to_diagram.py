import os
import sys


def get_max_depth(fs):
    data = fs.read()
    lines = data.split('\n')
    max_depth = 0
    for line in lines:
        depth = len(line.split(' ')[0])
        if depth > max_depth:
            max_depth = depth
    return max_depth
        
def get_diagram(fs, depth):
    depth+= 1
    line = fs.readline()
    diagram_lines = '| ' * depth + '|\n' + '|:--- ' * depth + ' |'
    while line:
        if line != '':
            line_split = line.replace('\n', '').split(' ')
            # print('line', line)            
            index = len(line_split[0])
            print(index, '\n' + '| *** '*index + line_split[1] + ' |'* (depth-index))
            diagram_lines+= '\n' + '| *** '*(index-1) + '| ' + line_split[1] + ' |'* (depth-index+1)
            line = fs.readline()
    return diagram_lines
    #print(diagram_lines)
    
if __name__ == '__main__':
    file = sys.argv[1]
    with open(file, 'r') as fs:
        max_depth = get_max_depth(fs)
        fs.seek(0)
        print(max_depth)
        lines_to_save = get_diagram(fs, max_depth)
        fs = open('1.md', 'w')
        fs.write(lines_to_save)
        
        