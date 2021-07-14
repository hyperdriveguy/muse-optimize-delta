import util_funcs


def remove_stereopanning(song):
    
    def panning_filter(line):
        if util_funcs.get_root_command(line) == 'stereopanning':
            return False
        return True

    return tuple(filter(panning_filter, song))


def convert_loopchannel(song):

    def insert_jump(line):
        if util_funcs.get_root_command(line) == 'loopchannel':
            split_command = line.split(' ')
            if split_command[1] == '0,':
                return f'\tjumpchannel {split_command[2].strip()}\n'
        return line
    
    return tuple(map(insert_jump, song))