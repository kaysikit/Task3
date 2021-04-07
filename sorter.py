import click
import eyed3
import os
import shutil


@click.command()
@click.option('-s', '--src-dir', default='.', help='Source directory.', show_default=True)
@click.option('-d', '--dst-dir', default='.', help='Destination directory.', show_default=True)
def sorter(src_dir, dst_dir):
    while True:
        if os.path.isdir(src_dir):
            # Проверка пути
            try:
                # Получение файлов
                list_music = os.scandir(src_dir)
            except PermissionError as error:
                print(str(error))
                print('Введите другой путь или "q" для выхода.')
                src_dir = input('>>> ')
                if src_dir == 'q':
                    break
            else:
                with list_music:
                    # Проверка файлов в каталоге
                    for el in list_music:
                        if not el.name.startswith('.') and el.is_file() \
                                and el.name.lower().endswith('.mp3'):

                            try:
                                audiofile = eyed3.load(el)
                                # Название файлов
                                if not audiofile.tag.title:
                                    title = el.name
                                else:
                                    title = audiofile.tag.title.replace('/', ':')

                                # Артисты и альбом
                                if not audiofile.tag.artist or not audiofile.tag.album:
                                    print(f'Не хватает тегов для сортировки: {el.name}')
                                    continue
                                else:
                                    artist = audiofile.tag.artist.replace('/', ':')
                                    album = audiofile.tag.album.replace('/', ':')

                                audiofile.tag.save()
                            except AttributeError as error:
                                print(f'Файл неисправен: {el.name}')
                            except PermissionError as error:
                                print(f'Нет прав для изменения файлов: {el.name}')
                                continue
                            # Если файл впорядке
                            else:
                                new_file_name = f'{title} - {artist} - {album}.mp3'
                                if os.path.exists(os.path.join(dst_dir, artist, album)):
                                    shutil.move(os.path.join(src_dir, el.name),
                                                os.path.join(dst_dir, artist, album, new_file_name))

                                else:
                                    # Создаём новую папку, если получится
                                    try:
                                        os.makedirs(os.path.join(dst_dir, artist, album))
                                    except PermissionError as error:
                                        print(str(error))
                                        print('Введите другой путь или "q" для выхода.')
                                        dst_dir = input('>>> ')
                                        if dst_dir == 'q':
                                            break
                                    else:
                                        shutil.move(os.path.join(src_dir, el.name),
                                                    os.path.join(dst_dir, artist, album, new_file_name))
                                print(f'{os.path.join(src_dir, el.name)} '
                                      f'-> {os.path.join(dst_dir, artist, album, new_file_name)}')
                print('Done.')
                break
        # Введённый путь не найден
        else:
            print('Папка не найдена')
            print('Введите путь к каталогу или введите q для выхода.')
            src_dir = input('>>> ')
            if src_dir == 'q':
                break


if __name__ == '__main__':
    sorter()
