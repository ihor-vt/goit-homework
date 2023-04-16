import os
import shutil


def normalize(names):
    name = ''
    domen = ''
    if names.count('.') > 1:
        c = names.rfind('.')
        name = names[:c]
        domen = names[c + 1:]
    else:
        name, domen = names.split('.')
    translit_dict = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D',
                     1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I',
                     1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N',
                     1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T',
                     1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH',
                     1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '',
                     1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'u', 1071: 'U', 1108: 'ja', 1028: 'JA', 1110: 'je',
                     1030: 'JE', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'}

    transl = name.translate(translit_dict)
    temp = ''
    for s in transl:
        if s in '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM':
            temp += s
        else:
            temp += '_'
    new_name = f'{temp}.{domen}'

    return new_name


# Створення папок з словника
def create_folders_from_list(folder_path, folder_names):
    for folder in folder_names:
        if not os.path.exists(f'{folder_path}\\{folder}'):
            os.mkdir(f'{folder_path}\\{folder}')


def get_subfolder_paths(folder_path):  # Пути подпапок
    subfolder_paths = []

    for current_dir, dirs, files in os.walk(folder_path):
        for file in files:
            subfolder_paths.append(f'{current_dir}\\{file}')
        for dir in dirs:
            get_subfolder_paths(dir)

    return subfolder_paths


def sort_files(folder_path):
    for folder in get_subfolder_paths(folder_path):
        ext_list = list(extensions.items())
        extension = folder.split('.')[-1]
        file_name = folder.split('\\')[-1]
        norm_file_name = normalize(file_name)
        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                try:
                    print(
                        f'Moving {file_name} in {ext_list[dict_key_int][0]} new name: {norm_file_name} folder\n')
                    shutil.move(
                        folder, f'{main_path}\\{ext_list[dict_key_int][0]}\\{norm_file_name}')
                except FileNotFoundError:
                    continue


def remove_empty_folders(folder_path):

    for d in os.listdir(folder_path):

        a = os.path.join(folder_path, d)

        if os.path.isdir(a):

            remove_empty_folders(a)

            if not os.listdir(a):

                os.rmdir(a)

                print(a, 'удалена')


def seach_archive(folder):  # Пошук архівів

    folder_archive = f'{main_path}\\{folder}'
    list_file_arch = []
    file_arch = os.listdir(folder_archive)
    if len(file_arch) > 0:
        for f in file_arch:
            list_file_arch.append(f'{folder_archive}\\{f}')
        unpack_arc(list_file_arch, folder_archive)
    else:
        None


def re_name(folder):  # Файл без розширення
    a = folder.split('\\')[3]
    b = a.replace('.zip', '')
    return b


def unpack_arc(archives, folder_archive):  # Створення папок і распаковки архива

    for folder in archives:

        if not os.path.exists(f'{folder_archive}\\{folder}'):

            fold = re_name(folder)

            os.mkdir(f'{folder_archive}\\{fold}')

    for filename in archives:

        fold = re_name(filename)

        shutil.unpack_archive(filename, f'{folder_archive}\\{fold}')


def sort_name(list_files):

    for i in list_files:

        norm_i = normalize(i)

        end_file = norm_i[norm_i.rfind('.') + 1:]
        if end_file in ['jpef', 'png', 'jpg', 'svg']:
            dict_all_group['image'].append(norm_i)
        elif end_file in ['avi', 'mp4', 'mov', 'mkv']:
            dict_all_group['video'].append(norm_i)
        elif end_file in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
            dict_all_group['documents'].append(norm_i)
        elif end_file in ['mp3', 'ogg', 'wav', 'amr']:
            dict_all_group['music'].append(norm_i)
        elif end_file in ['zip', 'gz', 'tar']:
            dict_all_group['archive'].append(norm_i)
        else:
            dict_all_group['others'].append(norm_i)


def end_file_group(path, file):
    all_end = ['jpef', 'png', 'jpg', 'svg', 'avi', 'mp4', 'mov', 'mkv', 'doc', 'docx', 'txt',
               'pdf', 'xlsx', 'pptx', 'mp3', 'ogg', 'wav', 'amr', 'zip', 'gz', 'tar']
    for f in file:
        end_file = f[f.rfind('.') + 1:]
        if end_file in all_end:
            if path in end_group:
                end_group[path].append(end_file)
            else:
                end_group[path] = [end_file]
        else:
            end_other.append(end_file)


def seach_file(path):
    for current_dir, dirs, files in os.walk(path):
        end_file_group(current_dir, files)
        sort_name(files)


main_path = input('Вкажіть адрес папки? ')  # Вказати шлях до папки

extensions = {
    'images': ['jpef', 'png', 'jpg', 'svg'],
    'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'ppt'],
    'audio': ['mp3', 'ogg', 'wav', 'amr', 'm4a'],
    'video': ['avi', 'mp4', 'mov', 'mkv'],
    'archives': ['zip', 'gz', 'tar'],
}

create_folders_from_list(main_path, extensions)  # Створення папок з словника
sort_files(main_path)  # Сортування файлів по папкам
seach_archive('archives')
remove_empty_folders(main_path)  # Видалення пустих папок

# Сортування файлів по категоріям
dict_all_group = {
    'image': [],
    'video': [],
    'documents': [],
    'music': [],
    'archive': [],
    'others': []
}

end_group = {}  # Папки з їхніми розширенями

end_other = []  # Невідомі розширення

seach_file(main_path)

print(f'Сортування файлів по категоріям: {dict_all_group}', end='\n')
print(f'Папки з їхніми розширенями: {end_group}', end='\n')
print(f'Невідомі розширення: {end_other}')
